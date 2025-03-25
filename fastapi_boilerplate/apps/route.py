"""Apps Route module.

Description:
- This module is used to create routes for application.

"""

from fastapi import APIRouter

from .api_v1.route import router as v1_router

router = APIRouter()


# Include all file routes
router.include_router(router=v1_router)
