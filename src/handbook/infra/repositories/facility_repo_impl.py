from sqlalchemy import Double, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import raiseload, selectinload

from domain.entities.facility import Facility
from domain.exceptions.base import DomainResourceNotFoundError
from domain.repositories.facility_repository import FacilityRepository
from domain.val_objs.coords import Coordinates
from domain.val_objs.ids import FacilityId
from infra.db.models.facility import FacilityModel
from infra.repositories.mappers.facility_mapper import FacilityMapper


class FacilityRepositoryImpl(FacilityRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, id: FacilityId) -> Facility:
        stmt = (
            select(FacilityModel)
            .where(FacilityModel.id == id.value)
            .options(
                selectinload(FacilityModel.organizations),
                raiseload("*"),
            )
        )
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if not model:
            raise DomainResourceNotFoundError
        return FacilityMapper.to_domain(model)

    async def list_all(self):
        stmt = select(FacilityModel).options(
            selectinload(FacilityModel.organizations),
            raiseload("*"),
        )
        result = await self._session.execute(stmt)
        return [FacilityMapper.to_domain(m) for m in result.scalars().all()]

    async def save(self, facility: Facility) -> None:
        model = FacilityMapper.to_model(facility)
        self._session.add(model)

    async def delete(self, facility: Facility) -> None:
        model = FacilityMapper.to_model(facility)
        await self._session.delete(model)

    async def list_in_radius(self, center: Coordinates, radius_meters: float):
        EARTH_RADIUS_M = 6371000
        lat0, lon0 = center.lat, center.lon

        lat_col = cast(FacilityModel.lat, Double)
        lon_col = cast(FacilityModel.lon, Double)

        distance_expr = EARTH_RADIUS_M * func.acos(
            func.cos(func.radians(lat0))
            * func.cos(func.radians(lat_col))
            * func.cos(func.radians(lon_col) - func.radians(lon0))
            + func.sin(func.radians(lat0)) * func.sin(func.radians(lat_col))
        )

        stmt = (
            select(FacilityModel)
            .where(distance_expr <= radius_meters)
            .options(
                selectinload(FacilityModel.organizations),
                raiseload("*"),
            )
        )

        result = await self._session.execute(stmt)
        return [FacilityMapper.to_domain(m) for m in result.scalars().all()]

    async def list_in_rectangle(self, p1: Coordinates, p2: Coordinates):
        min_lat = min(p1.lat, p2.lat)
        min_lon = min(p1.lon, p2.lon)
        max_lat = max(p1.lat, p2.lat)
        max_lon = max(p1.lon, p2.lon)

        lat_col = cast(FacilityModel.lat, Double)
        lon_col = cast(FacilityModel.lon, Double)

        stmt = (
            select(FacilityModel)
            .where(lat_col >= min_lat)
            .where(lat_col <= max_lat)
            .where(lon_col >= min_lon)
            .where(lon_col <= max_lon)
            .options(
                selectinload(FacilityModel.organizations),
                raiseload("*"),
            )
        )
        result = await self._session.execute(stmt)
        return [FacilityMapper.to_domain(m) for m in result.scalars().all()]
