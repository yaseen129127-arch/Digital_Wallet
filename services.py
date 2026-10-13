from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from tables import Account,Transaction, Ledger, ExternalPayments, Ldirection, Ttype, Tstatus, Otype, Estatus,Currency,Astatus

DATABASE_URL = ("postgresql+psycopg2://postgres:hanoyaseen@localhost:60000/wallet")

engine = create_engine(DATABASE_URL)

def charge(user):
    """ Insert the balance to wallet account without connect to Strip tools"""
    """Create the relationships between tables"""
    
    with Session(engine) as session :
        
    
        current_account = session.scalar(select(Account).where(Account.user_id == user.user_id,Account.currency == Currency.USD))

        if current_account is None:
            print("USD wallet not found")
            return
        
        external_transaction = Transaction(
            initiated_by_user_id = user.user_id,
                    transaction_type = Ttype.TOPUP,
                        status = Tstatus.COMPLETED,
                            currency = Currency.USD,
                                amount = 100000
                                )
        session.add(external_transaction)
        session.flush()
        
        

        external_balance = ExternalPayments(
            transaction_id = external_transaction.transaction_id,
                provider = "stripe",
                    external_reference = "A123",
                        operation_type = Otype.DEPOSIT,
                            status = Estatus.SUCCEEDED
                            )
       
    
        wallet_balance = Ledger(
            account_id = current_account.account_id,
                transaction_id = external_transaction.transaction_id,
                    direction = Ldirection.CREDIT,
                        amount =external_transaction.amount
                        )
        
        session.add_all([current_account,external_transaction,external_balance, wallet_balance])
        session.commit()
        ledger_entry = session.scalar(select(Ledger))
    print("Vaultix Charged Successful")
    print (ledger_entry.direction.value,ledger_entry.amount,ledger_entry.created_at)
        
        

def transfer():
    pass    


def cash():
    pass

def report():
    pass
