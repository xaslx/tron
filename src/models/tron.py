from src.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func



class TronRequest(Base):
    __tablename__ = 'tron_requests'

    address: Mapped[str]
    timestamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())