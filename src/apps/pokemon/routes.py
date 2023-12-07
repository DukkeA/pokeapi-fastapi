from fastapi import APIRouter

from .controllers import pokemon_detailed, pokemon_general

router: APIRouter = APIRouter(prefix='/pokemon')

router.get('')(pokemon_general)
router.get('/{id}')(pokemon_detailed)
