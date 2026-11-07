import uuid, enum, datetime
from sqlalchemy import Boolean, text
from sqlalchemy import  func, DateTime, BigInteger, VARCHAR, LargeBinary,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base




class Currency(enum.Enum):
    USD="USD"      
class TransactionType(enum.Enum): 
    DEPOSIT="DEPOSIT"
    WITHDRAWAL="WITHDRAWAL"
    TRANSFER="TRANSFER"
    
class LedgerAccountType(enum.Enum):
    USER_WALLET="USER_WALLET"
    PROVIDER_ESCROW="PROVIDER_ESCROW"
    PLATFORM_REVENUE="PLATFORM_REVENUE"

class TransactionStatus(enum.Enum):
    SUCCESS="SUCCESS"
    FAILED="FAILED"  
    PENDING="PENDING"

class User(Base):
    __tablename__="users"
    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=func.uuidv7())
    first_name: Mapped[str] = mapped_column(VARCHAR(50), nullable=True)
    last_name: Mapped[str] = mapped_column(VARCHAR(50), nullable=True)
    email_address: Mapped[str] = mapped_column(VARCHAR(255), unique=True, nullable=True)
    phone_number: Mapped[str] = mapped_column(VARCHAR(30), unique=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(LargeBinary, nullable=True) 
    currency: Mapped[Currency] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean,default=True,server_default="true", nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    closed_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True),nullable=True)
    payment_methods: Mapped[list["ExternalPayments"]] = relationship(back_populates="user", lazy="raise")
    transaction: Mapped[list["Transaction"]] = relationship(back_populates="user", lazy="raise")
    ledger_entries: Mapped[list["Ledger"]] = relationship(back_populates="user", lazy="raise")

class Transaction(Base):
    __tablename__="transactions"
    transaction_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=func.uuidv7())
    initiated_by_user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"),nullable=False)
    ext_pay_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("external_payments.external_payment_id"),nullable=True)
    transaction_type: Mapped[TransactionType] = mapped_column(nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(nullable=False)
    provider_tx_id: Mapped [ str] = mapped_column(VARCHAR(255), nullable=True)
    amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    user: Mapped["User"] = relationship(back_populates="transaction", lazy="raise")
    ledger_entries: Mapped[list["Ledger"]] = relationship(back_populates="transaction", lazy="raise")
    payment_methods: Mapped["ExternalPayments | None"] = relationship(back_populates="transaction", lazy="raise")    

class Ledger(Base):
    __tablename__="ledger_entry"
    entry_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=func.uuidv7())
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"),nullable=False)
    transaction_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("transactions.transaction_id"),nullable=False)
    account_type: Mapped[LedgerAccountType] = mapped_column(nullable=False)
    balance: Mapped[int] = mapped_column(BigInteger, nullable=False)
    amount: Mapped[int] = mapped_column(BigInteger, nullable=False)
    credit: Mapped[int] = mapped_column(BigInteger, nullable=True)
    debit: Mapped[int] = mapped_column(BigInteger, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    transaction: Mapped["Transaction"] = relationship(back_populates="ledger_entries")
    user: Mapped["User"] = relationship(back_populates="ledger_entries", lazy="raise")


class ExternalPayments(Base):
    __tablename__="external_payments"
    external_payment_id:Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=func.uuidv7())
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.user_id"),nullable=False)
    provider: Mapped[str] = mapped_column(VARCHAR(50),nullable=False)
    external_reference: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    card_info: Mapped[str] = mapped_column(VARCHAR(255), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    transaction: Mapped["Transaction"] = relationship(back_populates="payment_methods", lazy="raise")
    user: Mapped["User"] = relationship(back_populates="payment_methods", lazy="raise")


    


