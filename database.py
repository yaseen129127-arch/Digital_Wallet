from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase




# 1. Construct the psycopg2 URL
# Format: postgresql+psycopg2://user:pass@host:port/dbname
DATABASE_URL = "postgresql+psycopg2://postgres:hanoyaseen@localhost:60000/wallet"

# 2. Create the engine
engine = create_engine(DATABASE_URL, echo=True)

class Base (DeclarativeBase):
    pass
