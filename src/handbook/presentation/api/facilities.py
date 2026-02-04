from uuid import UUID

from fastapi import APIRouter, Depends, Path
from presentation.dependencies import get_facility_by_id_uc, get_facility_repo
from presentation.DTOs.facility_dto import FacilityDTO

router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get(
    "/",
    response_model=list[FacilityDTO],
    summary="List all facilities",
    description="Returns a complete list of all facilities stored in the system.",
    responses={
        404: {
            "description": "No facilities found",
            "content": {
                "application/json": {"example": {"detail": "No facilities found"}}
            },
        },
    },
)
async def list_all(repo=Depends(get_facility_repo)):
    facilities = await repo.list_all()

    return [FacilityDTO.from_domain(f) for f in facilities]


@router.get(
    "/{facility_id}",
    response_model=FacilityDTO,
    summary="Get facility by ID",
    description="Fetch a single facility by its UUID.",
    responses={
        404: {
            "description": "Facility not found",
            "content": {
                "application/json": {"example": {"detail": "Facility not found"}}
            },
        },
        422: {
            "description": "Invalid UUID format",
            "content": {
                "application/json": {"example": {"detail": "Invalid UUID format"}}
            },
        },
    },
)
async def get_facility_by_id(
    facility_id: UUID = Path(
        ...,
        description="Facility UUID",
        examples=["11111111-1111-1111-1111-111111111111"],
    ),
    uc=Depends(get_facility_by_id_uc),
):
    facility = await uc.execute(facility_id=facility_id)
    return FacilityDTO.from_domain(facility)
