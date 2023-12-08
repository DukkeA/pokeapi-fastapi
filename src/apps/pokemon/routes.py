from fastapi import APIRouter

from .controllers import get_pokemon_detailed, get_pokemon_general

router: APIRouter = APIRouter(prefix="/pokemon")

router.get("")(get_pokemon_general)
router.get("/{id}")(get_pokemon_detailed)
