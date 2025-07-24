from dataclasses import dataclass

from src.repositories.tron import BaseTronRepository
from src.schemas.pagination import PaginationOut
from src.schemas.tron import TronRequestOut


@dataclass
class ListRequestsUseCase:
    
    _tron_repository: BaseTronRepository

    async def execute(self, skip: int, limit: int) -> PaginationOut[TronRequestOut]:
        total, items = await self._tron_repository.get_paginated_list(skip, limit)
        return PaginationOut(total=total, items=[TronRequestOut.model_validate(i) for i in items])