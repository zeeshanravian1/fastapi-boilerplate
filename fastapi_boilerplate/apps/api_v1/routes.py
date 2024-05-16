"""
FastAPI V1 Route module

Description:
- This module is used to create v1 routes for application.

"""

from fastapi import APIRouter

from .role.route import router as role_router
from .user.route import router as user_router

router = APIRouter(prefix="/v1")


# Include all file routes
router.include_router(role_router)
router.include_router(user_router)
