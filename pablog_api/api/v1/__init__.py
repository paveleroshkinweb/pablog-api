from .utils import router as utils_router

from fastapi import APIRouter


router = APIRouter(prefix="/v1")

router.include_router(utils_router)
