from decimal import Decimal

from domain.entities.facility import Facility
from domain.val_objs.address import Address
from domain.val_objs.coords import Coordinates
from domain.val_objs.ids import FacilityId
from infra.db.models.facility import FacilityModel


class FacilityMapper:
    @staticmethod
    def to_domain(model: FacilityModel) -> Facility:
        return Facility(
            id_=FacilityId(model.id),
            address=Address(model.address),
            coordinates=Coordinates(
                lat=Decimal(model.lat),
                lon=Decimal(model.lon),
            ),
        )

    @staticmethod
    def to_model(entity: Facility) -> FacilityModel:
        return FacilityModel(
            id=entity.id.value,
            address=entity.address.address,
            lat=str(entity.coordinates.lat),
            lon=str(entity.coordinates.lon),
        )
