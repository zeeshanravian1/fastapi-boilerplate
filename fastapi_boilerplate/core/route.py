"""
FastAPI Route module

Description:
- This module is used to create routes for application.

"""

from fastapi import APIRouter

from ..apps.api_v1.routes import router as v1_routers
from ..apps.auth.route import router as auth_router

router = APIRouter()


# Include all file routes
router.include_router(v1_routers)
router.include_router(auth_router)
router.include_router(auth_router)
