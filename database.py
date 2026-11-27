# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
DATABASE_URL="postgresql+asyncpg://postgres:hanoyaseen@localhost:60000/wallet"
engine=create_async_engine(DATABASE_URL, echo=False,pool_size=5,max_overflow=10,pool_timeout=30,pool_recycle=1800,pool_pre_ping=True)
AsyncSessionLocal = async_sessionmaker(bind=engine,autoflush=True, expire_on_commit=False)

class Base (AsyncAttrs,DeclarativeBase):
    pass
async def init_db():
    """initialize the database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)    
async def get_db():
    async with AsyncSessionLocal() as session:
         yield session
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
       await db.close()


