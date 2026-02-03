from fastapi import APIRouter
from presentation.api.busines_types import router as bt_router
from presentation.api.facilities import router as facility_router
from presentation.api.organization import router as org_router

api_router = APIRouter()
api_router.include_router(org_router)
api_router.include_router(facility_router)
api_router.include_router(bt_router)
