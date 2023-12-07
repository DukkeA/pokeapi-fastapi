from fastapi import APIRouter

from src.apps.pokemon.routes import router as pokemon_router

router: APIRouter = APIRouter(prefix='/api/v1')

router.include_router(pokemon_router)
