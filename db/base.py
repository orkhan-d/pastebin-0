from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from settings import settings

engine = create_async_engine(settings.DATABASE_URL)
SessionFactory = async_sessionmaker(bind=engine)
