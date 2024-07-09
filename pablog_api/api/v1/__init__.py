from .monitoring import router as monitoring_router

from fastapi import APIRouter


router = APIRouter(prefix="/v1")

router.include_router(monitoring_router)
