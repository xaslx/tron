from dishka import Provider, Scope, provide, from_context
from src.config import Config
from fastapi import Request
from src.database.postgres import new_session_maker
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import AsyncIterable
from tronpy import Tron
from tronpy.providers import HTTPProvider
from src.use_cases.get_all_requests import ListRequestsUseCase
from src.use_cases.get_tron_info import GetTronInfoUseCase
from src.repositories.tron import BaseTronRepository, SQLAlchemyTronRepository


class AppProvider(Provider):

    config = from_context(provides=Config, scope=Scope.APP)
    request: Request = from_context(provides=Request, scope=Scope.REQUEST)


    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.APP)
    def get_tron_client(self, config: Config) -> Tron:
        provider = HTTPProvider(
            endpoint_uri=config.trongrid_url,
            api_key=config.trongrid_api,
        )
        return Tron(provider=provider)
    
    @provide(scope=Scope.REQUEST)
    def get_tron_repository(self, session: AsyncSession) -> BaseTronRepository:
        return SQLAlchemyTronRepository(_session=session)
    
    @provide(scope=Scope.REQUEST)
    def get_tron_info_use_case(self, tron_client: Tron, tron_repo: BaseTronRepository) -> GetTronInfoUseCase:
        return GetTronInfoUseCase(_tron_client=tron_client, _tron_repository=tron_repo)
    
    @provide(scope=Scope.REQUEST)
    def get_all_tron_requests_use_case(self, tron_repo: BaseTronRepository) -> ListRequestsUseCase:
        return ListRequestsUseCase(_tron_repository=tron_repo)