from fastapi import APIRouter

from . import career


router = APIRouter()
router.include_router(career.router)
