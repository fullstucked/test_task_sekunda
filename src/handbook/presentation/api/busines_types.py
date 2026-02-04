from uuid import UUID
from fastapi import APIRouter, Depends, Path

from presentation.dependencies import get_bt_by_id_uc, get_bt_repo
from presentation.DTOs.business_types_dto import BusinessTypeDTO

router = APIRouter(prefix="/business-types", tags=["Business Types"])


@router.get(
    "/",
    response_model=list[BusinessTypeDTO],
    summary="List all business types",
    description="Returns all business types available in the system.",
)
async def list_all(repo=Depends(get_bt_repo)):
    bts = await repo.list_all()
    return [BusinessTypeDTO.from_domain(bt) for bt in bts]


@router.get(
    "/{bt_id}",
    response_model=BusinessTypeDTO,
    summary="Get business type by ID",
    description="Fetch a single business type by its UUID.",
    responses={
        404: {
            "description": "Business type not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Business type not found"}
                }
            },
        },
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
    bt = await uc.execute(bt_id)
    return BusinessTypeDTO.from_domain(bt)
