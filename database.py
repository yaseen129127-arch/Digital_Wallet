from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL="postgresql+psycopg2://postgres:@localhost:60000/wallet"
engine=create_engine(DATABASE_URL, echo=True)

class Base (DeclarativeBase):
    pass
