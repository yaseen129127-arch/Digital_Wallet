from sqlalchemy import create_engine, select,func
from sqlalchemy.orm import Session
from tables import User,Transaction, Ledger, ExternalPayments,TransactionType,TransactionStatus,LedgerAccountType

DATABASE_URL = ("postgresql+psycopg2://postgres:hanoyaseen@localhost:60000/wallet")

engine = create_engine(DATABASE_URL)

from sqlalchemy import create_engine, select,func
from sqlalchemy.orm import Session
from tables import User,Transaction, Ledger, ExternalPayments,TransactionType,TransactionStatus,LedgerAccountType

DATABASE_URL = ("postgresql+psycopg2://postgres:hanoyaseen@localhost:60000/wallet")

engine = create_engine(DATABASE_URL)

def charge(user):
    """ Insert the balance to wallet account without connect to Strip tools"""
    """Check the current user after login """
    """Create CREDIT and DEBIT financial role Double-entry book keeping """
    
    amount = int(input("charge amount by external provider : "))
    with Session(engine) as session :
        current_user = session.scalar(select(User).where (User.user_id == user.user_id,))
        if current_user is None:
            #print("User wallet not found")
            raise ValueError("User clearing account not found")
            
        payment = ExternalPayments(
            user_id = current_user.user_id,
                provider = "stripe",
                    external_reference = "A123",
                        card_info = " visa")
        session.add(payment)
        session.flush()
            
        transaction = Transaction(
            initiated_by_user_id = user.user_id,
                ext_pay_id = payment.external_payment_id,
                    transaction_type = TransactionType.DEPOSIT,
                        status = TransactionStatus.SUCCESS,
                            provider_tx_id = payment.external_reference,
                                amount = amount)
        session.add(transaction)
        session.flush()
        
        ledger_credit = Ledger(
            user_id = current_user.user_id,
                transaction_id = transaction.transaction_id,
                    account_type = LedgerAccountType.USER_WALLET,
                        amount = amount,
                            credit = amount)
        
        ledger_debit = Ledger(
                user_id = current_user.user_id,
                    transaction_id = transaction.transaction_id,
                        account_type = LedgerAccountType.PROVIDER_ESCROW,
                            amount = amount,
                                debit = amount)
        
        credit = session.scalar(select(func.sum(Ledger.credit))
                                        .where(Ledger.user_id == current_user.user_id,
                                            Ledger.account_type == LedgerAccountType.USER_WALLET)) or 0
        
        debit =  session.scalar(select(func.sum(Ledger.debit))
                                        .where(Ledger.user_id == current_user.user_id,
                                            Ledger.account_type == LedgerAccountType.USER_WALLET)) or 0        
        total_balance = credit - debit 
        session.add_all([ledger_credit,ledger_debit])

        ledger_entry = session.scalar(select(Ledger).where (Ledger.transaction_id == transaction.transaction_id))
        print("Vaultix Charged Successful")
        charged_money = ledger_entry.amount
        charged_time = ledger_entry.created_at
        print (charged_money,charged_time)
        print(f"Vaultix Balance : {total_balance}")
        
        session.commit()
   
   
def transfer(user):
    """Transfer money between two user in the same wallet"""
    """Make the transfer inside one transaction operation success or failed"""
    
    with Session(engine) as session : 
        sender_user = session.scalar(select(User).where (User.user_id == user.user_id))
        if sender_user is None:
            #print("User Account not found")
            raise ValueError("User Account not found")
        # sender_balance = session.scalar(select(Ledger).where(Ledger.user_id == sender_user.user_id,
                                                            #  Ledger.balance == sender_balance))
        sender_credit = session.scalar(select(func.sum(Ledger.credit))
                                                .where(Ledger.user_id == sender_user.user_id,
                                                    Ledger.account_type == LedgerAccountType.USER_WALLET)) or 0       
        sender_debit =  session.scalar(select(func.sum(Ledger.debit))
                                                .where(Ledger.user_id == sender_user.user_id,
                                                    Ledger.account_type == LedgerAccountType.USER_WALLET)) or 0
        
        total_sender_balance =  sender_credit - sender_debit

        transfer_amount = int(input("Insert The Transfer Amount :"))
        if transfer_amount <= 0 :
            raise ValueError (" The amount should be a positive")
        if total_sender_balance - transfer_amount < 0 :
            raise ValueError("Insufficient balance")
        total_sender_balance =  sender_credit - sender_debit - transfer_amount

        
        transfer_transaction = Transaction(initiated_by_user_id = sender_user.user_id,
                                        transaction_type = TransactionType.TRANSFER,
                                            status = TransactionStatus.PENDING,
                                                amount = transfer_amount
                                                )
        session.add_all([sender_user, transfer_transaction])
        session.flush()
        
        print("Please fill in the details below :")
        print("___________________________________\n")
        receiver_email = input("Beneficiary Account :")
        receiver_phone = input("Beneficiary phone : ")
        
        receiver_user = session.scalar(select(User)
                                    .where(User.email_address == receiver_email,
                                            User.phone_number == receiver_phone))
        if receiver_user is None:
            print("User Account not Existing")
            return
        receiver_credit = session.scalar(select(func.sum(Ledger.credit))
                                                .where(Ledger.user_id == receiver_user.user_id,
                                                    Ledger.account_type == LedgerAccountType.USER_WALLET)) or 0       
        receiver_debit =  session.scalar(select(func.sum(Ledger.debit))
                                                .where(Ledger.user_id == receiver_user.user_id,
                                                    Ledger.account_type == LedgerAccountType.USER_WALLET)) or 0 
        total_receiver_balance = receiver_credit - receiver_debit + transfer_amount
        session.add(receiver_user)
        session.flush()
        
        ledger_debit = Ledger( user_id = sender_user.user_id,
                                transaction_id = transfer_transaction.transaction_id,                                   
                                    account_type = LedgerAccountType.USER_WALLET,
                                            balance = total_sender_balance,
                                                amount = transfer_amount,
                                                    debit = transfer_amount)
        ledger_credit = Ledger( user_id = receiver_user.user_id,
                                transaction_id = transfer_transaction.transaction_id,     
                                    account_type = LedgerAccountType.USER_WALLET,
                                        balance = total_receiver_balance,
                                            amount = transfer_amount,
                                                credit = transfer_amount)
        session.add_all([ledger_debit, ledger_credit])
        session.flush()
        
        transfer_transaction = Transaction(initiated_by_user_id = sender_user.user_id,
                                                transaction_type = TransactionType.TRANSFER,
                                                    status = TransactionStatus.SUCCESS,
                                                        amount = transfer_amount
                                                        )
        session.add(transfer_transaction)
    
        sender = sender_user.first_name
        reciver = receiver_user.first_name
        transfer_type = ledger_debit.account_type.value
        amount = transfer_transaction.amount
        print(amount, transfer_type, sender,reciver )
        print(f"Your Current balance : {total_receiver_balance}")
        session.commit()
                                            
                                     






def cash():
    pass

def report():
    
    pass
