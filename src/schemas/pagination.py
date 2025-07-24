from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')

class PaginationOut(BaseModel, Generic[T]):
    total: int
    items: list[T]