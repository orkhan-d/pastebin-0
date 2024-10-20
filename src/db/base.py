from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func
from sqlalchemy.types import UUID as SA_UUID
from uuid import UUID, uuid4

from settings import settings

engine = create_async_engine(settings.DATABASE_URL)
SessionFactory = async_sessionmaker(bind=engine)


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),
                                                 server_onupdate=func.now())


class BaseWithIntPK:
    id: Mapped[int] = mapped_column(primary_key=True)


class BaseWithUUIDPK:
    id: Mapped[UUID] = mapped_column(type_=SA_UUID,
                                     default=uuid4,
                                     primary_key=True)


async def get_db_session():
    async with SessionFactory() as session:
        yield session
