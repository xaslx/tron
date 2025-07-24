import pytest_asyncio
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.pool import StaticPool

from src.models.base import Base
from src.repositories.tron import SQLAlchemyTronRepository, BaseTronRepository
from src.main import create_app
from src.config import Config

from fastapi import FastAPI
from httpx import AsyncClient

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from src.ioc import AppProvider
from dishka import make_async_container
from httpx import ASGITransport
from src.models.tron import TronRequest
from sqlalchemy import text


TEST_DB_URL = 'sqlite+aiosqlite:///:memory:'


@pytest_asyncio.fixture(scope='session')
async def test_engine():
    engine = create_async_engine(
        TEST_DB_URL,
        echo=False,
        future=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    session_maker = async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.rollback()


@pytest_asyncio.fixture
async def sample_tron_requests(db_session: AsyncSession):
    tron_req1 = TronRequest(address='T1234567890abcdef')
    tron_req2 = TronRequest(address='Tabcdef1234567890')
    
    db_session.add_all([tron_req1, tron_req2])
    await db_session.commit()

    await db_session.refresh(tron_req1)
    await db_session.refresh(tron_req2)

    yield [tron_req1, tron_req2]
    
    await db_session.execute(text('DELETE FROM tron_requests'))
    await db_session.commit()


@pytest_asyncio.fixture
async def tron_repo(db_session: AsyncSession) -> BaseTronRepository:
    return SQLAlchemyTronRepository(_session=db_session)


@pytest_asyncio.fixture
async def test_app(tron_repo: BaseTronRepository) -> FastAPI:

    config = Config()

    context = {
        Config: config,
        BaseTronRepository: tron_repo,
    }

    provider = AppProvider()
    container: AsyncContainer = make_async_container(provider, context=context)

    app = create_app()
    setup_dishka(container=container, app=app)
    return app


@pytest_asyncio.fixture
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url='http://127.0.0.1:8000') as client:
        yield client
