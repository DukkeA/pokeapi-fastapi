from fastapi import APIRouter

from src.apps.pokemon.routes import router as pokemon_router
from src.apps.healthcheck.routes import router as healthcheck_router

router: APIRouter = APIRouter(prefix="/api/v1")

router.include_router(pokemon_router)
router.include_router(healthcheck_router)
