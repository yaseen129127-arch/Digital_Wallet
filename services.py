import datetime, bcrypt
from decimal import Decimal
from sqlalchemy import create_engine, select,func,delete
from sqlalchemy.orm import Session,joinedload,selectinload
from tables import User,Transaction, Ledger, ExternalPayments,TransactionType,TransactionStatus,LedgerAccountType,Currency

DATABASE_URL=("postgresql+psycopg2://postgres:@localhost:60000/wallet")
engine=create_engine(DATABASE_URL)


def deposit(user_id):
    """#Check the deposit money.
    #Check the current user as reciver.
    # Insert the external payments data and make the transaction.
    # Add the balance to user , save the ledger and update the transaction status."""    
    try:
        amount=int(input("Deposit amount in cents: "))
    except ValueError:
        print("Invalid value. Insert Number Only.")
        return
    if amount <= 0:
        print("Amount must be greater than zero.")
        return
    deposit_fee=amount * Decimal("0.02")
    total_deposit_amount= amount - deposit_fee
    try:
        with Session(engine)as session:
            with session.begin():
                current_user=session.scalar(select(User).where(User.user_id == user_id).with_for_update())
                if current_user is None:
                    raise ValueError("User not found.")
                payment_transaction=session.scalar(select(ExternalPayments).where(ExternalPayments.user_id == current_user.user_id))
                print(f"\n Your Provider : {payment_transaction.provider} "  
                    f" Reference : {payment_transaction.external_reference} " 
                        f" Card Info.: {payment_transaction.card_info}\n")
                transaction=Transaction(initiated_by_user_id=user_id,
                                        ext_pay_id=payment_transaction.external_payment_id,
                                            transaction_type=TransactionType.DEPOSIT,
                                                status=TransactionStatus.PENDING,
                                                    provider_tx_id=payment_transaction.external_reference,
                                                        amount=amount)
                session.add(transaction)
                session.flush()
                wallet_credit=Ledger(user_id=current_user.user_id,
                                    transaction_id=transaction.transaction_id,
                                        account_type=LedgerAccountType.USER_WALLET,
                                            amount=amount,
                                                credit=total_deposit_amount,
                                                    debit=0)
                provider_debit=Ledger(user_id=current_user.user_id,
                                    transaction_id=transaction.transaction_id,
                                        account_type=LedgerAccountType.PROVIDER_ESCROW,
                                            amount=amount,
                                                credit=0,
                                                    debit=amount)
                platform_credit=Ledger(user_id=current_user.user_id,
                                                    transaction_id=transaction.transaction_id,
                                                        account_type=LedgerAccountType.PLATFORM_REVENUE,
                                                            amount=amount,
                                                                credit=deposit_fee,
                                                                    debit=0)
                transaction.status=TransactionStatus.SUCCESS
                session.add_all([wallet_credit, provider_debit, platform_credit])
            total_credit=session.scalar(select(func.coalesce(func.sum(Ledger.credit),0))
                                        .where(Ledger.user_id == current_user.user_id,
                                            Ledger.account_type == LedgerAccountType.USER_WALLET))
            total_debit=session.scalar(select(func.coalesce(func.sum(Ledger.debit),0))
                                        .where(Ledger.user_id == current_user.user_id,
                                            Ledger.account_type == LedgerAccountType.USER_WALLET))
            total_balance=total_credit - total_debit
            currency=current_user.currency.value
            print(f"MEMO: {LedgerAccountType.PROVIDER_ESCROW.value} ")
            print(f"VoLTiX Deposit Successful: {amount / 100:.2f} {currency}")
            print(f"Provider: {payment_transaction.provider}")
            print(f"Deposit Transaction Reference: {transaction.transaction_id}")
            print(f"{transaction.created_at}")
            print(f"\nCurrent VoLTiX Balance: {total_balance / 100:.2f} {currency}")
    except Exception as e:
        return (f"Deposit Failed..{e}")


def transfer(user_id):
    """#Transfer money between two user in the same wallet.
    #Ensure that the entire transaction either succeeds in its entirety or fails in its entirety.
    #Check the current user as sender.
    #Check current user balance. 
    #Make the transaction for sender user.
    #Check the ricever user and reduce the balance from sender.
    # Save the ledger of the transaction."""
    with Session(engine)as session: 
        try:
            with session.begin():
                user=session.scalar(select(User).where(User.user_id == user_id).with_for_update())
                if user is None:
                    raise KeyError("User Account not found")
                sender_credit=session.scalar(select(func.coalesce(func.sum(Ledger.credit),0))
                                                        .where(Ledger.user_id == user.user_id,
                                                            Ledger.account_type == LedgerAccountType.USER_WALLET))     
                sender_debit=session.scalar(select(func.coalesce(func.sum(Ledger.debit),0))
                                                        .where(Ledger.user_id == user.user_id,
                                                            Ledger.account_type == LedgerAccountType.USER_WALLET))
                user_balance=sender_credit - sender_debit
                try:
                    transfer_amount=int(input("Insert Transfer Amount In Cents:"))
                except ValueError:
                    raise ValueError("Invalid Value. Insert Number Only.")
                if transfer_amount <= 0:
                    print(" The amount should be a positive")
                    return
                if user_balance - transfer_amount < 0:
                    print(" Insufficient balance")
                    return
                user_total_balance=user_balance - transfer_amount
                transfer_transaction=Transaction(initiated_by_user_id=user.user_id,
                                                transaction_type=TransactionType.TRANSFER,
                                                    status=TransactionStatus.PENDING,
                                                        amount=transfer_amount)
                session.add(transfer_transaction)
                session.flush()
                print("Enter transfer details:")
                receiver_email=input("Beneficiary Account :")
                receiver_phone=input("Beneficiary phone : ")
                receiver_user=session.scalar(select(User)
                                            .where(User.email_address == receiver_email,
                                                    User.phone_number == receiver_phone)
                                            .with_for_update())
                if receiver_user is None:
                    print("User Account not Existing. Transfer Failed..!!")
                    return
                choice = input("To Confirm Enter Your Password : ")
                choice_byte = choice.encode("utf-8")
                if not bcrypt.checkpw(choice_byte, user.password_hash):
                    print("The Password Is Not Match. Transfer Failed..!!")
                    return
                receiver_credit=session.scalar(select(func.coalesce(func.sum(Ledger.credit),0))
                                                        .where(Ledger.user_id == receiver_user.user_id,
                                                            Ledger.account_type == LedgerAccountType.USER_WALLET))       
                receiver_debit=session.scalar(select(func.coalesce(func.sum(Ledger.debit),0))
                                                        .where(Ledger.user_id == receiver_user.user_id,
                                                            Ledger.account_type == LedgerAccountType.USER_WALLET))
                receiver_total_balance=receiver_credit - receiver_debit + transfer_amount
                ledger_debit=Ledger(user_id=user.user_id,
                                        transaction_id=transfer_transaction.transaction_id,                                   
                                            account_type=LedgerAccountType.USER_WALLET,
                                                    balance=user_total_balance,
                                                        amount=transfer_amount,
                                                            credit=0,
                                                                debit=transfer_amount)
                ledger_credit=Ledger(user_id=receiver_user.user_id,
                                        transaction_id=transfer_transaction.transaction_id,     
                                            account_type=LedgerAccountType.USER_WALLET,
                                                balance=receiver_total_balance,
                                                    amount=transfer_amount,
                                                        credit=transfer_amount,
                                                            debit=0)
                transfer_transaction.status=TransactionStatus.SUCCESS
                session.add_all([ledger_debit, ledger_credit])
            sender=f" {user.first_name} {user.last_name}"
            reciver=f"{receiver_user.first_name} {receiver_user.last_name}"
            transfer_type=ledger_debit.account_type.value
            amount=transfer_transaction.amount
            currency=user.currency.value
            print(f"\nTransfer VoLTiX  {transfer_type} {transfer_transaction.status.value}  {amount/100:.2f} {currency}")
            print(f"From: {sender}  To:  {reciver}  VoLTiX {transfer_type}")
            print(f"Transfer Transaction Reference: {transfer_transaction.transaction_id}")
            print(f"{transfer_transaction.created_at}")
            print(f"\nYour Current VoLTiX balance : {user_total_balance/100 :f} {currency}\n")
        except Exception as e:
            raise (f"Transfer Failed..{e}")
                                                
                                     
def withdrawal(user_id):
    """#Check the user and balance.
    #Insert the external or gatway data.
    # Make the transaction for the user.
    # Reduce the user balance ,save the ledger and update the transaction status."""
    try:
        with Session(engine)as session:
            with session.begin():
                user=session.scalar(select(User).where(User.user_id == user_id).with_for_update())
                if user is None:
                    raise ValueError("User account not found")
                user_credit=session.scalar(select(func.coalesce(func.sum(Ledger.credit),0))
                                                     .where(Ledger.user_id == user.user_id,
                                                        Ledger.account_type == LedgerAccountType.USER_WALLET))
                user_debit=session.scalar(select(func.coalesce(func.sum(Ledger.debit),0))
                                                    .where(Ledger.user_id == user.user_id,
                                                        Ledger.account_type == LedgerAccountType.USER_WALLET))
                user_balance=user_credit - user_debit
                try:
                    amount=int(input("Insert amount in cents  :"))
                except ValueError:
                    raise ValueError("Invalid value, enter Number Only")
                if amount <= 0:
                    print(" The amount should be a positive")
                    return
                withdrawal_fee=amount * Decimal("0.02")
                total_withdrawl_amount=amount + withdrawal_fee
                if user_balance - total_withdrawl_amount < 0:
                    print(" Insufficient balance")
                    return
                total_user_balance=user_balance - total_withdrawl_amount
                user_external_payment=session.scalars(select(ExternalPayments)
                                                             .where(ExternalPayments.user_id ==user.user_id)).first()
                if user_external_payment is None:
                    raise KeyError("ERROR..!! No External Payment Four User Found")
                print(f"\n Your Provider : {user_external_payment.provider} "  
                    f" Reference : {user_external_payment.external_reference} " 
                        f" Card Info.: {user_external_payment.card_info}\n")
                choice=input("To Confirm Enter Your Password : ")
                choice_byte = choice.encode("utf-8")
                if not bcrypt.checkpw(choice_byte, user.password_hash):
                    print("The Password Is Not Match..!!")
                    return
                withdrawal_transaction=Transaction(initiated_by_user_id=user.user_id,
                                                    ext_pay_id=user_external_payment.external_payment_id,
                                                        transaction_type=TransactionType.WITHDRAWAL,
                                                            status=TransactionStatus.PENDING,
                                                                provider_tx_id=user_external_payment.external_reference,
                                                                    amount=amount)
                session.add(withdrawal_transaction)
                session.flush()
                wallet_debit=Ledger(user_id=user.user_id,
                                        transaction_id=withdrawal_transaction.transaction_id,
                                            account_type=LedgerAccountType.USER_WALLET,
                                                amount=amount,
                                                    credit=0,
                                                        debit=total_withdrawl_amount)    
                provider_credit=Ledger(user_id=user.user_id,
                                        transaction_id=withdrawal_transaction.transaction_id,
                                            account_type=LedgerAccountType.PROVIDER_ESCROW,
                                                amount=amount,
                                                    credit=amount,
                                                        debit=0)
                platform_credit=Ledger(user_id=user.user_id,
                                        transaction_id=withdrawal_transaction.transaction_id,
                                            account_type=LedgerAccountType.PLATFORM_REVENUE,
                                                amount=amount,
                                                    credit=withdrawal_fee,
                                                        debit=0)
                withdrawal_transaction.status=TransactionStatus.SUCCESS
                session.add_all([wallet_debit, provider_credit, platform_credit])
                currency=user.currency.value
                external_gate_way=user_external_payment.card_info
            print(f"MEMO: {LedgerAccountType.PROVIDER_ESCROW.value}")
            print(f"\nVoLTiX Withdrawal Successful: {amount/100:.2f} {currency}")
            print(f"PROVIDER_ESCROW: {external_gate_way}")
            print(f"Withdrawal Transaction Reference: {withdrawal_transaction.transaction_id}")
            print(f"{withdrawal_transaction.created_at}")
            print(f"\nCurrent VoLTiX Balance: {total_user_balance/100:.2f} {currency}")
    except Exception as e:
        raise (f"Withdrawal Failed..{e}")
    
        
def transaction_report(user_id):
    """Showing user transaction saved in ledger """
    with Session(engine)as session:
        try:
            with session.begin():
                user=session.get(User, user_id)
                if user is None:
                    raise KeyError("User Account not found")
                user_credit=session.scalar(select(func.coalesce(func.sum(Ledger.credit),0))
                                                     .where(Ledger.user_id == user.user_id,
                                                        Ledger.account_type == LedgerAccountType.USER_WALLET))
                user_debit=session.scalar(select(func.coalesce(func.sum(Ledger.debit),0))
                                                    .where(Ledger.user_id == user.user_id,
                                                        Ledger.account_type == LedgerAccountType.USER_WALLET))        
                user_balance=user_credit - user_debit
                currency=user.currency.value
                report_stmt = (select(Ledger).where(Ledger.user_id == user.user_id)
                                .options(joinedload(Ledger.user),joinedload(Ledger.transaction)
                                    .options(joinedload(Transaction.payment_methods),selectinload(Transaction.ledger_entries).joinedload(Ledger.user)))
                    .order_by(Ledger.created_at.asc()))                      
                ledger_entries = session.scalars(report_stmt).all()
                for ledger in ledger_entries:
                    transaction = ledger.transaction
                    user = ledger.user
                    externalPayments = transaction.payment_methods
                    if transaction.transaction_type == TransactionType.DEPOSIT:
                        if ledger.account_type == LedgerAccountType.USER_WALLET:
                            print(f"\n MEMO: {LedgerAccountType.PROVIDER_ESCROW.value}")
                            print(f" TYPE: {TransactionType.DEPOSIT.value}")
                            print(f" AMOUNT: {(ledger.amount)/100:.2f} {Currency.USD.value}")
                            print(f" ACCOUNT: {user.first_name} {user.last_name}" 
                                    f"      USER CREDIT: {ledger.credit/100:.2f} {currency}"
                                        f"       DEBIT: {ledger.debit/100:.2f} {currency}")
                        elif ledger.account_type == LedgerAccountType.PROVIDER_ESCROW:
                            print(f" PAYMENT PROVIDER: {externalPayments.provider}"     
                                    f"    PAYMENT CREDIT: {ledger.credit/100:.2f} {currency}"   
                                        f"      DEBIT: {ledger.debit/100:.2f} {currency}")
                        elif ledger.account_type == LedgerAccountType.PLATFORM_REVENUE:
                            print(f" DEPOSIT FEE 2%: {LedgerAccountType.PLATFORM_REVENUE.value}"     
                                    f"    PAYMENT CREDIT: {ledger.credit/100:.2f} {currency}"   
                                        f"      DEBIT: {ledger.debit/100:.2f} {currency}")
                            print(f" PAYMENT REFERENCE: {externalPayments.external_reference}")
                            print(f" DEPOSIT Transaction REFERENCE: {transaction.transaction_id}")
                            print(f" DATE: {transaction.created_at}")
                    elif transaction.transaction_type == TransactionType.TRANSFER: 
                        if ledger.account_type == LedgerAccountType.USER_WALLET:
                            print(f"\n MEMO: {LedgerAccountType.USER_WALLET.value}")
                            print(f" TYPE: {TransactionType.TRANSFER.value}")
                            print(f" AMOUNT: {(ledger.amount)/100:.2f} {Currency.USD.value}")
                            print(f" ACCOUNT: {user.first_name} {user.last_name}" 
                                    f"      USER CREDIT: {ledger.credit/100:.2f} {currency}"
                                        f"       DEBIT: {ledger.debit/100:.2f} {currency}")
                        for reciver_ledger in transaction.ledger_entries:
                            if reciver_ledger.user_id != user.user_id and reciver_ledger.account_type == LedgerAccountType.USER_WALLET:
                                reciver_user = reciver_ledger.user
                                if reciver_user:
                                    print(f" ACCOUNT: {reciver_user.first_name} {reciver_user.last_name}" 
                                            f"      USER CREDIT: {reciver_ledger.credit/100:.2f} {currency}"
                                            f"       DEBIT: {reciver_ledger.debit/100:.2f} {currency}")
                            print(f" TRANSFER Transaction REFERENCE: {transaction.transaction_id}")
                            print(f" DATE: {transaction.created_at}")
                    elif transaction.transaction_type == TransactionType.WITHDRAWAL:    
                        if ledger.account_type == LedgerAccountType.USER_WALLET:
                            print(f"\n MEMO: {LedgerAccountType.PROVIDER_ESCROW.value}")
                            print(f" TYPE: {TransactionType.WITHDRAWAL.value}")
                            print(f" AMOUNT: {(ledger.amount)/100:.2f} {Currency.USD.value}")
                            print(f" ACCOUNT: {user.first_name} {user.last_name}" 
                                    f"      USER CREDIT: {ledger.credit/100:.2f} {currency}"
                                        f"       DEBIT: {ledger.debit/100:.2f} {currency}")
                        elif ledger.account_type == LedgerAccountType.PROVIDER_ESCROW:
                            print(f" PAYMENT PROVIDER: {externalPayments.provider}"     
                                                            f"    PAYMENT CREDIT: {ledger.credit/100:.2f} {currency}"   
                                                                f"      DEBIT: {ledger.debit/100:.2f} {currency}")
                        elif ledger.account_type == LedgerAccountType.PLATFORM_REVENUE:
                            print(f" WITHDRAWAL FEE 2%: {LedgerAccountType.PLATFORM_REVENUE.value}"     
                                                            f"    PAYMENT CREDIT: {ledger.credit/100:.2f} {currency}"   
                                                                f"      DEBIT: {ledger.debit/100:.2f} {currency}")
                            print(f" PAYMENT REFERENCE: {externalPayments.external_reference}")
                            print(f" WITHDRAWAL Transaction REFERENCE: {transaction.transaction_id}")
                            print(f" DATE: {transaction.created_at}")      
                print("\n-----------------------")
                print(f" CURRENT VoLTiX BALANCE: {user_balance/100:.2f} {currency}")
                print("-------------------------\n")          
        except Exception as e:
            print(f"Report error: {e}")
            raise
    
            
def delete_account(user_id):
    """Delete user account and his external payments"""    
    with Session(engine) as session:
        try:
            with session.begin():
                user = session.scalar(select(User).where(User.user_id == user_id).with_for_update())
                if user is None:
                    raise ValueError("User account not found")
                if not user.is_active:
                    raise ValueError("Account is already closed")
                total_debit = session.scalar(select(func.coalesce(func.sum(Ledger.debit), 0))
                                            .where(Ledger.user_id == user.user_id,
                                                Ledger.account_type == LedgerAccountType.USER_WALLET))
                total_credit = session.scalar(select(func.coalesce(func.sum(Ledger.credit), 0))
                                                    .where(Ledger.user_id == user.user_id,
                                                        Ledger.account_type == LedgerAccountType.USER_WALLET))
                balance = total_credit - total_debit
                if balance != 0:
                    raise ValueError(
                        f"Please empty your balance before closing your account. "
                        f"Current balance: {balance}"
                        )
                password = input("Enter your password to confirm: ")
                password_byte = password.encode("utf-8")
                if not bcrypt.checkpw(password_byte, user.password_hash):
                    raise ValueError("Password mismatch")
                payment_records = session.scalars(select(ExternalPayments).where(ExternalPayments.user_id == user.user_id)
                                                .with_for_update()).all()
                for payment in payment_records:
                    payment.card_info = None
                user.is_active = False
                user.closed_at = datetime.datetime.now(datetime.timezone.utc)
                user.first_name = None
                user.last_name = None
                user.email_address = None
                user.phone_number = None
                user.password_hash = None
                payment.card_info = None
            print("Your account has been successfully closed.")
        except Exception as e:
            print(f"Account closure error: {e}")
            raise

    