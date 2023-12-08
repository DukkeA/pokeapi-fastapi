from fastapi import APIRouter

from .controllers import health_check

router: APIRouter = APIRouter(prefix="/healthcheck")

router.get("/")(health_check)
