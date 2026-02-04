from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from presentation.dependencies import (
    get_org_by_id_uc,
    get_orgs_in_proximity,
    get_orgs_in_rect,
    list_orgs_by_bt_rec_uc,
    list_orgs_by_facility_uc,
    search_org_by_name_uc,
)
from presentation.DTOs.organization_dto import OrganizationDTO
from presentation.schemas.circle_schema import ProximityQuery
from presentation.schemas.rect_schema import RectangleQuery
from presentation.schemas.search_by_name import SearchByNameQuery

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get(
    "/search",
    response_model=list[OrganizationDTO],
    summary="Search organizations by name",
    responses={
        404: {
            "description": "No organizations found",
            "content": {
                "application/json": {"example": {"detail": "No organizations found"}}
            },
        },
    },
)
async def search_by_name(
    q: SearchByNameQuery = Query(...),
    uc=Depends(search_org_by_name_uc),
):
    orgs = await uc.execute(q.q)

    return [OrganizationDTO.from_domain(o) for o in orgs]


@router.get(
    "/facility/{facility_id}",
    response_model=list[OrganizationDTO],
    summary="List organizations by facility ID",
    responses={
        404: {
            "description": "No organizations found for this facility",
            "content": {
                "application/json": {
                    "example": {"detail": "No organizations found for this facility"}
                }
            },
        },
    },
)
async def list_by_facility(
    facility_id: UUID = Path(...),
    uc=Depends(list_orgs_by_facility_uc),
):
    orgs = await uc.execute(facility_id)

    return [OrganizationDTO.from_domain(o) for o in orgs]


@router.get(
    "/business/{bt_id}",
    response_model=list[OrganizationDTO],
    summary="List organizations by business type (recursive)",
    responses={
        404: {
            "description": "No organizations found for this business type",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "No organizations found for this business type"
                    }
                }
            },
        },
    },
)
async def list_by_business_type_recursive(
    bt_id: UUID = Path(...),
    uc=Depends(list_orgs_by_bt_rec_uc),
):
    orgs = list(set(await uc.execute(bt_id)))

    return [OrganizationDTO.from_domain(o) for o in orgs]


@router.get(
    "/in-proximity",
    response_model=list[OrganizationDTO],
    summary="Search organizations in proximity",
    responses={
        404: {
            "description": "No organizations found in this radius",
            "content": {
                "application/json": {
                    "example": {"detail": "No organizations found in this radius"}
                }
            },
        },
    },
)
async def search_in_proximity(
    q: ProximityQuery = Query(...),
    uc=Depends(get_orgs_in_proximity),
):
    orgs = await uc.execute(
        lat=q.lat,
        lon=q.lon,
        radius_meters=q.radius_meters,
    )

    return [OrganizationDTO.from_domain(o) for o in orgs]


@router.get(
    "/in-zone",
    response_model=list[OrganizationDTO],
    summary="List organizations in rectangle zone",
    responses={
        404: {
            "description": "No organizations found in this area",
            "content": {
                "application/json": {
                    "example": {"detail": "No organizations found in this area"}
                }
            },
        },
    },
)
async def list_orgs_in_rectangle(
    rect: RectangleQuery = Query(...),
    uc=Depends(get_orgs_in_rect),
):
    orgs = await uc.execute(
        lat1=rect.lat1,
        lon1=rect.lon1,
        lat2=rect.lat2,
        lon2=rect.lon2,
    )

    return [OrganizationDTO.from_domain(o) for o in orgs]


@router.get(
    "/{org_id}",
    response_model=OrganizationDTO,
    summary="Get organization by ID",
    responses={
        404: {
            "description": "Organization not found",
            "content": {
                "application/json": {"example": {"detail": "Organization not found"}}
            },
        },
    },
)
async def get_org_by_id(
    org_id: UUID = Path(...),
    uc=Depends(get_org_by_id_uc),
):
    org = await uc.execute(org_id)

    return OrganizationDTO.from_domain(org)
