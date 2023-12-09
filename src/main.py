from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request

from src.apps.pokemon.services import init_pokemons
from src.lib.logger import setup_logging
from src.routes import router
from src.settings import settings
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Administrador de contexto de ciclo de vida de la aplicación.

    Este administrador de contexto se utiliza para gestionar el ciclo de vida de
    una aplicación FastAPI. Inicializa un cliente asíncrono para realizar solicitudes
    HTTP, realiza una inicialización específica de la aplicación (como la inicialización
    de datos de Pokémon), y cierra el cliente al final del ciclo de vida de la aplicación.

    Args:
        - app (FastAPI): La instancia de la aplicación FastAPI.
    """
    setup_logging()
    app.requests = httpx.AsyncClient()  # type: ignore
    await init_pokemons(app=app)
    yield
    await app.requests.aclose()  # type: ignore


app: FastAPI = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    dependencies=[],
)

app.include_router(router)


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )


@app.exception_handler(RequestValidationError)
async def exception_handler1(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "message": f"""{exc.errors()[0].get("type")} {exc.errors()[0].get("msg").lower()}"""
        },
    )
