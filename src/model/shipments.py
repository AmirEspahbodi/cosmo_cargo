
from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import BIGINT

from src.core.connection.postgres import Base


class Shipment(Base):
    __tablename__ = "shipments"

    id: Mapped[int] = mapped_column(
        BIGINT,
        primary_key=True,
        autoincrement=True,
    )

