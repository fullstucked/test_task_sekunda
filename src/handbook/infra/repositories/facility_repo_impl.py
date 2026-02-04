from sqlalchemy import Double, cast, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import raiseload, selectinload
from sqlalchemy import case

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

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------

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

        if model is None:
            raise DomainResourceNotFoundError(
                "Facility not found",
                context={"facility_id": str(id.value)},
            )

        return FacilityMapper.to_domain(model)

    async def list_all(self):
        stmt = (
            select(FacilityModel)
            .options(
                selectinload(FacilityModel.organizations),
                raiseload("*"),
            )
        )
        result = await self._session.execute(stmt)
        return [FacilityMapper.to_domain(m) for m in result.scalars().all()]

    async def save(self, facility: Facility) -> None:
        model = FacilityMapper.to_model(facility)
        await self._session.merge(model)

    async def delete(self, facility: Facility) -> None:
        db_model = await self._session.get(FacilityModel, facility.id.value)
        if db_model is not None:
            await self._session.delete(db_model)

    # ---------------------------------------------------------
    # Geographic queries
    # ---------------------------------------------------------

    async def list_in_radius(self, center: Coordinates, radius_meters: float):
        EARTH_RADIUS_M = 6371000

        lat0 = float(center.lat)
        lon0 = float(center.lon)

        lat_col = cast(FacilityModel.lat, Double)
        lon_col = cast(FacilityModel.lon, Double)



        acos_arg = (
            func.cos(func.radians(lat0))
            * func.cos(func.radians(lat_col))
            * func.cos(func.radians(lon_col) - func.radians(lon0))
            + func.sin(func.radians(lat0)) * func.sin(func.radians(lat_col))
        )

        clamped = case(
            (acos_arg < -1.0, -1.0),
            (acos_arg > 1.0, 1.0),
            else_=acos_arg,
        )

        distance_expr = EARTH_RADIUS_M * func.acos(clamped)

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
        min_lat = float(min(p1.lat, p2.lat))
        max_lat = float(max(p1.lat, p2.lat))
        min_lon = float(min(p1.lon, p2.lon))
        max_lon = float(max(p1.lon, p2.lon))

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
