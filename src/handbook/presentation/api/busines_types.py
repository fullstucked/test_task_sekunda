from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, status

from presentation.dependencies import get_bt_by_id_uc, get_bt_repo
from presentation.DTOs.business_types_dto import BusinessTypeDTO
from presentation.schemas.error_schema import ErrorResponse

router = APIRouter(prefix="/business-types", tags=["Business Types"])


@router.get(
    "/",
    response_model=list[BusinessTypeDTO],
    summary="List all business types",
    description="Returns all business types available in the system.",
    responses={
        200: {"description": "List of business types returned"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
async def list_all(repo=Depends(get_bt_repo)):
    """
    Retrieve all business types.
    """
    bts = await repo.list_all()
    if not bts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No business type found",
        )
    return [BusinessTypeDTO.from_domain(bt) for bt in bts]


@router.get(
    "/{bt_id}",
    response_model=BusinessTypeDTO,
    summary="Get business type by ID",
    description="Fetch a single business type by its UUID.",
    responses={
        200: {"description": "Business type found"},
        404: {"model": ErrorResponse, "description": "Business type not found"},
        422: {"model": ErrorResponse, "description": "Invalid UUID format"},
    },
)
async def get_by_id(
    bt_id: UUID = Path(
        ...,
        description="Business type UUID",
        examples=["aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"],
    ),
    uc=Depends(get_bt_by_id_uc),
):
    """
    Retrieve a business type by its unique identifier.
    """
    bt = await uc.execute(bt_id)
    if not bt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No business type found",
        )
    return BusinessTypeDTO.from_domain(bt)
