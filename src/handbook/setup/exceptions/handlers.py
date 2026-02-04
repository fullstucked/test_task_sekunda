from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from domain.exceptions.business_type_err import BusinessTypeTypeError,  BusinessTypeHierarchyError
from domain.exceptions.facility_err import  FacilityInvariantError
from domain.exceptions.org_err import  OrganizationTypeError, OrganizationInvariantError
from domain.exceptions.base import DomainResourceNotFoundError


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(BusinessTypeTypeError)
    @app.exception_handler(BusinessTypeHierarchyError)
    @app.exception_handler(FacilityInvariantError)
    @app.exception_handler(OrganizationInvariantError)
    @app.exception_handler(OrganizationTypeError)
    async def input_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc) or "Bad request!"},
        )
    @app.exception_handler(DomainResourceNotFoundError)
    async def not_found_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc) or "Resource not found!"},
        )
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(Exception)
    async def generic_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )
