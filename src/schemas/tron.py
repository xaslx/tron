from pydantic import BaseModel, ConfigDict
from datetime import datetime
from decimal import Decimal


class TronInfo(BaseModel):
    bandwidth: int
    energy: int
    balance: Decimal

    model_config = ConfigDict(from_attributes=True)

class TronRequestOut(BaseModel):
    id: int
    address: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)