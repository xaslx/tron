from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.config import Config
from src.ioc import AppProvider
from src.routers.tron import router
from dishka import AsyncContainer, make_async_container
from dishka.integrations import fastapi as fastapi_integration



@asynccontextmanager
async def lifespan(app: FastAPI):

    yield



def create_app() -> FastAPI:

    config: Config = Config()
    container: AsyncContainer = make_async_container(AppProvider(), context={Config: config})
    
    app: FastAPI = FastAPI()
    fastapi_integration.setup_dishka(container=container, app=app)
    app.include_router(router, prefix='/api', tags=['Tron'])

    return app