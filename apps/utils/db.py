from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import func, MetaData
from uuid import uuid4, UUID



class UUIDMixin:
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        unique=True,
        default=uuid4,
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class TimeStampBase:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(),
                                                 onupdate=func.now(),
                                                 nullable=False)


class TimeStampMixin(DeclarativeBase, UUIDMixin, TimeStampBase):
    """
        Declare Base class for ORM
        """
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
