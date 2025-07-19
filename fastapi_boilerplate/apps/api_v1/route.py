"""API V1 Route module.

Description:
- This module is used to create v1 routes for application.

"""

from fastapi import APIRouter

from fastapi_boilerplate.core.config import settings

from .role.route import router as role_router
from .user.route import router as user_router

router = APIRouter(prefix=settings.API_V1_STR)


# Include all file routes
router.include_router(router=role_router)
router.include_router(router=user_router)
