import os
import dotenv
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import MetaData


dotenv.load_dotenv()
metadata = MetaData()
Base = declarative_base(metadata=metadata)

db_url = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

print(db_url + ' все ништяк')
engine = create_async_engine(db_url, echo=True)

async def get_session():
    try:
        session = async_sessionmaker(engine,class_ = AsyncSession)()
        yield session
    except Exception as exc:
        print(exc)
        await session.rollback()
    finally:
        await session.commit()
        await session.close()

async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)