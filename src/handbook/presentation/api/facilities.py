from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status

from presentation.dependencies import get_facility_by_id_uc, get_facility_repo
from presentation.DTOs.facility_dto import FacilityDTO
from presentation.schemas.error_schema import ErrorResponse

router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get(
    "/",
    response_model=list[FacilityDTO],
    summary="List all facilities",
    description="Returns a complete list of all facilities stored in the system.",
    responses={
        200: {"description": "List of facilities successfully returned"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def list_all(repo=Depends(get_facility_repo)):
    """
    Retrieve all facilities.
    """
    facilities = await repo.list_all()
    if not facilities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No facilities found",
        )

    return [FacilityDTO.from_domain(f) for f in facilities]


@router.get(
    "/{facility_id}",
    response_model=FacilityDTO,
    summary="Get facility by ID",
    description="Fetch a single facility by its UUID.",
    responses={
        200: {"description": "Facility found"},
        404: {"model": ErrorResponse, "description": "Facility not found"},
        422: {"model": ErrorResponse, "description": "Invalid UUID format"},
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
    """
    Retrieve a facility by its unique identifier.
    """
    facility = await uc.execute(facility_id=facility_id)
    if not facility:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No facility found",
        )
    return FacilityDTO.from_domain(facility)
