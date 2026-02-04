from fastapi import Depends

from application.use_cases.business_types.get_bt_by_id import GetBusinessTypeByIdUseCase
from application.use_cases.facilities.get_facility_by_id import GetFacilityByIdUseCase
from application.use_cases.orgs.get_org_by_id import GetOrganizationByIdUseCase
from application.use_cases.orgs.list_orgs_by_bt import (
    ListOrganizationsByBusinessTypeUseCase,
)
from application.use_cases.orgs.list_orgs_by_bt_rec import (
    ListOrganizationsByBusinessTypeRecursiveUseCase,
)
from application.use_cases.orgs.list_orgs_by_facility import (
    ListOrganizationsByFacilityUseCase,
)
from application.use_cases.orgs.list_orgs_by_rad import ListOrganizationsInRadiusUseCase
from application.use_cases.orgs.list_orgs_in_rect import (
    ListOrganizationsInRectangleUseCase,
)
from application.use_cases.orgs.search_org_by_name import (
    SearchOrganizationByNameUseCase,
)
from infra.db.dependency import (
    get_bt_repo,
    get_facility_repo,
    get_org_repo,
)

# ------------------------------------------------------------------
# Organization Use Case Providers
# ------------------------------------------------------------------


def get_org_by_id_uc(
    org_repo=Depends(get_org_repo),
):
    """
    Provide a use case for retrieving an organization by its ID.

    Dependencies:
        - org_repo: Repository for organization persistence.

    Returns:
        GetOrganizationByIdUseCase
    """
    return GetOrganizationByIdUseCase(org_repo=org_repo)


def list_orgs_by_facility_uc(
    org_repo=Depends(get_org_repo),
    facility_repo=Depends(get_facility_repo),
):
    """
    Provide a use case for listing organizations associated with a facility.

    Dependencies:
        - org_repo: Repository for organizations.
        - facility_repo: Repository for facilities.

    Returns:
        ListOrganizationsByFacilityUseCase
    """
    return ListOrganizationsByFacilityUseCase(
        org_repo=org_repo,
        facility_repo=facility_repo,
    )


def list_orgs_by_bt_uc(
    org_repo=Depends(get_org_repo),
    bt_repo=Depends(get_bt_repo),
):
    """
    Provide a use case for listing organizations by business type.

    Dependencies:
        - org_repo: Repository for organizations.
        - bt_repo: Repository for business types.

    Returns:
        ListOrganizationsByBusinessTypeUseCase
    """
    return ListOrganizationsByBusinessTypeUseCase(
        org_repo=org_repo,
        bt_repo=bt_repo,
    )


def list_orgs_by_bt_rec_uc(
    org_repo=Depends(get_org_repo),
    bt_repo=Depends(get_bt_repo),
):
    """
    Provide a use case for recursively listing organizations by business type.

    This includes organizations belonging to child business types.

    Dependencies:
        - org_repo: Repository for organizations.
        - bt_repo: Repository for business types.

    Returns:
        ListOrganizationsByBusinessTypeRecursiveUseCase
    """
    return ListOrganizationsByBusinessTypeRecursiveUseCase(
        org_repo=org_repo,
        bt_repo=bt_repo,
    )


def list_orgs_by_radius_uc(
    facility_repo=Depends(get_facility_repo),
    org_repo=Depends(get_org_repo),
):
    """
    Provide a use case for listing organizations within a geographic radius.

    Dependencies:
        - facility_repo: Repository for facility geolocation data.
        - org_repo: Repository for organizations.

    Returns:
        ListOrganizationsInRadiusUseCase
    """
    return ListOrganizationsInRadiusUseCase(
        facility_repo=facility_repo,
        org_repo=org_repo,
    )


def list_orgs_in_rect_uc(
    facility_repo=Depends(get_facility_repo),
    org_repo=Depends(get_org_repo),
):
    """
    Provide a use case for listing organizations within a rectangular area.

    Dependencies:
        - facility_repo: Repository for facility geolocation data.
        - org_repo: Repository for organizations.

    Returns:
        ListOrganizationsInRectangleUseCase
    """
    return ListOrganizationsInRectangleUseCase(
        facility_repo=facility_repo,
        org_repo=org_repo,
    )


def search_org_by_name_uc(
    org_repo=Depends(get_org_repo),
):
    """
    Provide a use case for searching organizations by name.

    Dependencies:
        - org_repo: Repository for organizations.

    Returns:
        SearchOrganizationByNameUseCase
    """
    return SearchOrganizationByNameUseCase(org_repo)


# ------------------------------------------------------------------
# Business Type Use Case Providers
# ------------------------------------------------------------------


def get_bt_by_id_uc(
    bt_repo=Depends(get_bt_repo),
):
    """
    Provide a use case for retrieving a business type by its ID.

    Dependencies:
        - bt_repo: Repository for business types.

    Returns:
        GetBusinessTypeByIdUseCase
    """
    return GetBusinessTypeByIdUseCase(bt_repo=bt_repo)


# ------------------------------------------------------------------
# Facility Use Case Providers
# ------------------------------------------------------------------


def get_facility_by_id_uc(
    facility_repo=Depends(get_facility_repo),
):
    """
    Provide a use case for retrieving a facility by its ID.

    Dependencies:
        - facility_repo: Repository for facilities.

    Returns:
        GetFacilityByIdUseCase
    """
    return GetFacilityByIdUseCase(facility_repo=facility_repo)


def get_orgs_in_proximity(
    facility_repo=Depends(get_facility_repo),
    orgs_repo=Depends(get_org_repo),
):
    """
    Provide a use case for listing organizations near a given facility.

    Dependencies:
        - facility_repo: Repository for facility geolocation data.
        - orgs_repo: Repository for organizations.

    Returns:
        ListOrganizationsInRadiusUseCase
    """
    return ListOrganizationsInRadiusUseCase(
        facility_repo=facility_repo,
        org_repo=orgs_repo,
    )


def get_orgs_in_rect(
    facility_repo=Depends(get_facility_repo),
    orgs_repo=Depends(get_org_repo),
):
    """
    Provide a use case for listing organizations inside a rectangular area.

    Dependencies:
        - facility_repo: Repository for facility geolocation data.
        - orgs_repo: Repository for organizations.

    Returns:
        ListOrganizationsInRectangleUseCase
    """
    return ListOrganizationsInRectangleUseCase(
        facility_repo=facility_repo,
        org_repo=orgs_repo,
    )
