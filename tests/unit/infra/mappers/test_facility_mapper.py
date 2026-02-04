from domain.val_objs.address import Address
from uuid import uuid4
from domain.val_objs.ids import FacilityId
from domain.val_objs.coords import Coordinates
import uuid
from decimal import Decimal

from infra.db.models.facility import FacilityModel
from infra.repositories.mappers.facility_mapper import FacilityMapper
from domain.entities.facility import Facility


def test_facility_to_domain():
    model = FacilityModel(
        id=uuid.uuid4(),
        address="Somewhere",
        lat="0",
        lon="0",
    )

    fac = FacilityMapper.to_domain(model)

    assert fac.address.address == "Somewhere"
    assert fac.coordinates.lat == Decimal("0")
    assert fac.coordinates.lon == Decimal("0")


def test_facility_to_model():
    fac = Facility(
        id_=FacilityId(uuid4()),
        address=Address("Amsterdam"),
        coordinates=Coordinates(Decimal(0),Decimal(0))
    )

    model = FacilityMapper.to_model(fac)

    assert model.id == fac.id.value
    assert model.address == "Amsterdam"
    assert model.lat == "0"
    assert model.lon == "0"
