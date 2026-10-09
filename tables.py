import uuid, enum, datetime
from sqlalchemy import  func, DateTime, BigInteger, VARCHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base



class Currency(enum.Enum):
    USD = "USD"
    EUR = "EUR"
class Astatus(enum.Enum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
class Ldirection(enum.Enum):
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"
class Ttype(enum.Enum):
    INTERNAL = "INTERNAL"
    TOPUP = "TOPUP"
class Tstatus(enum.Enum):
    COMPLETED = "COMPLETED"
    FAILURE = "FAILURE"
class Otype(enum.Enum):
    DEPOSIT = "DEPOSIT"
    CASHOUT = "CASHOUT"
class Estatus(enum.Enum):
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"  
      
class User(Base):
    __tablename__ = "users"
    user_id : Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=func.uuidv7())
    first_name : Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    last_name : Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    email_address : Mapped[str] = mapped_column(VARCHAR(255), unique=True, nullable=False)
    phone_number : Mapped[str] = mapped_column(VARCHAR(30), unique=True, nullable=False)
    password_hash : Mapped[str] = mapped_column(VARCHAR(255), nullable=False) 
    created_at : Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    account : Mapped[list["Account"]] = relationship(back_populates="user")
    transaction : Mapped[list["Transaction"]] = relationship(back_populates="user")
    def __repr__(self):
        return f"User(user_id={self.user_id}, first_name='{self.first_name}', last_name='{self.last_name}',email_address='{self.email_address}', email_address='{self.email_address}', password_hash='{self.password_hash}')"
class Account(Base):
    __tablename__ = "accounts"
    account_id : Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=func.uuidv7())
    user_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"))
    currency : Mapped[Currency]
    account_status : Mapped[Astatus] 
    created_at : Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    user : Mapped["User"] = relationship(back_populates="account")
    ledger_entries : Mapped[list["Ledger"]] = relationship(back_populates="account")

class Transaction(Base):
    __tablename__ = "transactions"
    transaction_id : Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=func.uuidv7())
    initiated_by_user_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"))
    idempotency_key : Mapped[uuid.UUID]
    transaction_type : Mapped[Ttype]
    status : Mapped[Tstatus]
    currency : Mapped[Currency]
    amount : Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at : Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    user : Mapped["User"] = relationship(back_populates="transaction")
    ledger_entries : Mapped[list["Ledger"]] = relationship(back_populates="transaction")
    external_payment : Mapped["ExternalPayments|None"] = relationship(back_populates="transaction")    

class Ledger(Base):
    __tablename__ = "ledger_entry"
    entry_id : Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=func.uuidv7())
    account_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("accounts.account_id"))
    transaction_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("transactions.transaction_id"))
    direction : Mapped[Ldirection] 
    amount : Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at : Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    account : Mapped["Account"] = relationship(back_populates="ledger_entries")
    transaction : Mapped["Transaction"] = relationship(back_populates="ledger_entries")

class ExternalPayments(Base):
    __tablename__ = "external_payments"
    external_payment_id : Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=func.uuidv7())
    transaction_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("transactions.transaction_id"))
    provider : Mapped[str] = mapped_column(VARCHAR(50),nullable=False)
    external_reference : Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    operation_type : Mapped[Otype] 
    status : Mapped[Estatus]
    created_at : Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    transaction : Mapped["Transaction"] = relationship(back_populates="external_payment")

    
#Base.metadata.create_all(engine)


