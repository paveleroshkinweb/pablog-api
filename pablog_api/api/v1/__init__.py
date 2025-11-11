from pablog_api.apps.auth.router import router as auth_router
from pablog_api.apps.monitoring.router import router as monitoring_router

from fastapi import APIRouter


router = APIRouter(prefix="/v1")

router.include_router(monitoring_router)
router.include_router(auth_router)
