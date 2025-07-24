from abc import ABC, abstractmethod
from src.models.tron import TronRequest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BaseTronRepository(ABC):

    @abstractmethod
    async def log(self, address: str) -> TronRequest:
        ...

    @abstractmethod
    async def get_paginated_list(self, skip: int = 0, limit: int = 10) -> tuple[int, list[TronRequest]]:
        ...


@dataclass
class SQLAlchemyTronRepository(BaseTronRepository):
    
    _session: AsyncSession

    async def log(self, address: str) -> TronRequest:
        obj = TronRequest(address=address)
        self._session.add(obj)
        await self._session.commit()
        await self._session.refresh(obj)
        return obj

    async def get_paginated_list(self, skip: int = 0, limit: int = 10) -> tuple[int, list[TronRequest]]:
        query = select(TronRequest).order_by(TronRequest.timestamp.desc()).offset(skip).limit(limit)
        result = await self._session.execute(query)
        items = result.scalars().all()
        total = (await self._session.execute(select(func.count(TronRequest.id)))).scalar_one()
        return total, items