import datetime, bcrypt, asyncio,random,uuid
from decimal import Decimal
from sqlalchemy import select,func
from database import AsyncSessionLocal
from sqlalchemy.orm import joinedload,selectinload
from models import User,Transaction, Ledger, ExternalPayments,TransactionType,TransactionStatus,LedgerAccountType,Currency,Provider
# from schemas import RejisterRequest


async def rejister():
    """Create account """
    
    first_name = input("First Name : ")
    last_name = input ("Last Name : ")
    email_address = input("Email Address : ")
    phone_number = input("Phone Number : ")
    card_info = input("Insert The Card Number : ")
    password = input("Password : ")
    re_type_password = input("Re-type your password : ")
    
    async with AsyncSessionLocal()as session:
        async with session.begin():
            password_byet = password.encode("utf-8")
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password_byet, salt)
            password_byet_re_type = re_type_password.encode("utf-8")
            re_type_hased = bcrypt.hashpw(password_byet_re_type, salt)
            if hashed != re_type_hased:
                raise ValueError("Miss match password")
            existing_email = await session.scalar(select(User).where(User.email_address == email_address))
            if existing_email:
                raise ValueError("\n Email Address is Already Used")
            existing_phone = await session.scalar(select(User).where(User.phone_number == phone_number))
            if existing_phone:
                raise ValueError("\n Phone Number is Already Used")
            new_user = User(first_name=first_name,
                            last_name=last_name, 
                                email_address=email_address, 
                                    phone_number=phone_number,
                                        card_info=card_info,
                                        password=hashed,
                                            currency=Currency.USD)
            new_payment = ExternalPayments(user=new_user,
                            provider=Provider.STRIPE)
            session.add_all([new_payment,new_user])
            print("\nAccount Created Successfully"
            f"\nplease login")
        
             

async def login():
    """ Login to user account"""
    
    email=input("User Email : ")
    password=input("Password : ") 
    
    async with AsyncSessionLocal()as session:
        async with session.begin():
            statement = select(User).where(User.email_address == email,
                                        User.is_active.is_(True))
            user = await session.scalar(statement)
            if user is None or not user.is_active:
                print("Invalide email")
                return None
            password_byte = password.encode("utf-8")       
            password_stored=user.password
            if password_stored is None:
                raise ValueError("Password is missing")
            if bcrypt.checkpw(password_byte,password_stored):
                print("login successful")
                print("\n VoLtiX Wallet")
                print(f"  Wellcome {user.first_name} {user.last_name}")
                print("---------------------------------------------------\n")
                return user.user_id
            else:
                raise ValueError("Invalide password")   
        
        
async def menu_wallet(user_id:uuid.UUID):
    """Internal menu wallet"""
    
    # print("1. Deposit Account")
    # print("2. Transfer Money")
    # print("3. Cash Out")
    # print("4. Transaction Report")
    # print("5. Remove Account")
    # print("6. Logout")
    # choose=input("\nChoose an option: ")
    while True:
        print("1. Deposit Account")
        print("2. Transfer Money")
        print("3. Cash Out")
        print("4. Transaction Report")
        print("5. Remove Account")
        print("6. Logout")
        choose=input("\nChoose an option: ")
        if choose =="1":
            await deposit(user_id)
        elif choose == "2":
            await transfer(user_id)
        elif choose == "3":
            await withdrawal(user_id)
        elif choose == "4":
            await transaction_report(user_id)
        elif choose == "5":
            await delete_account(user_id)
            print("Account removed successful")
            break
        elif choose =="6":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice..! Please Choose A Number From The Menu \n")
        # except Exception as e:
            # raise ValueError(f"login failed {e}")

# bank_balance = 1000000            
async def bank_simulated():
    """ bank simulated the response that send to the system for deposit or withdrwal """
    # if bank_balance < amount:
    #     banck_re_sponse = {}
    
    feed_back = ["SUCCESS","FAILED"]
    weights = [80,20] 
    choice = random.choices(feed_back, weights=weights, k=1).pop()
    return choice
 
# async def stripe_simulated():
#     """ the simulated provider send key request to the bank for the transaction"""
#     stripe_key = request_key
 
    
async def deposit(user_id:uuid.UUID):
    """#Check the deposit money.
    #Check the current user as reciver.
    # Insert the external payments data and make the transaction.
    # Add the balance to user , save the ledger and update the transaction status."""    
    
    try:
        amount = int(input("Deposit amount in cents: "))
    except ValueError:
        print("Invalid value. Insert Number Only.")
        return
    if amount <= 0:
        print("Amount must be greater than zero.")
        return
    
    async with AsyncSessionLocal()as session:
        async with session.begin():
            
            
            task = asyncio.create_task(bank_simulated())
            
            
            current_user = await session.scalar(select(User).where(User.user_id == user_id).with_for_update())
            if current_user is None:
                raise ValueError("User not found.")
            deposit_fee = amount * Decimal("0.02")
            total_deposit_amount = amount - deposit_fee
            payment_transaction = await session.scalar(select(ExternalPayments).where(ExternalPayments.provider == Provider.STRIPE,
                                                                                      ExternalPayments.user_id == current_user.user_id))
            if payment_transaction is None:
                raise ValueError("Payment method not found.")
            transaction = Transaction(initiated_by_user_id=user_id,
                                    ext_pay_id=payment_transaction.external_payment_id,
                                        transaction_type=TransactionType.DEPOSIT,
                                            status=TransactionStatus.PENDING,
                                                    amount=amount)
            
            # request_key = uuid.uuid7()
            # request_deposit={current_user.card_info,request_key,ExternalPayments.external_reference}
            # await asyncio.sleep(3)
            
            
            return_value = await task 
            if return_value == "FAILED":
                raise ValueError(f"Deposit couldn't be completed"
                    f"Your bank declined this transaction. No money was taken from your account." 
                      f"\nTry again or use a different payment method.")
                
                
                # raise ValueError(f"Deposit couldn't be completed"
                #     f"Your bank declined this transaction. No money was taken from your account." 
                #       f"\nTry again or use a different payment method.")
                
                
            print(f"\n Your Provider : {payment_transaction.provider.value} "  
                f" Reference : {payment_transaction.external_reference} " 
                    f" Card Info.: {current_user.card_info}\n")
            session.add(transaction)
            await session.flush()
            wallet_credit = Ledger(user_id=current_user.user_id,
                                transaction_id=transaction.transaction_id,
                                    account_type=LedgerAccountType.USER_WALLET,
                                        amount=amount,
                                            credit=total_deposit_amount,
                                                debit=0)
            provider_debit = Ledger(user_id=current_user.user_id,
                                transaction_id=transaction.transaction_id,
                                    account_type=LedgerAccountType.PROVIDER_ESCROW,
                                        amount=amount,
                                            credit=0,
                                                debit=amount)
            platform_credit = Ledger(user_id=current_user.user_id,
                                                transaction_id=transaction.transaction_id,
                                                    account_type=LedgerAccountType.PLATFORM_REVENUE,
                                                        amount=amount,
                                                            credit=deposit_fee,
                                                                debit=0)
            transaction.status = TransactionStatus.SUCCESS
            session.add_all([wallet_credit, provider_debit, platform_credit])
            await session.flush()
            total_credit = await session.scalar(select(func.coalesce(func.sum(Ledger.credit),0))
                                        .where(Ledger.user_id == current_user.user_id,
                                            Ledger.account_type == LedgerAccountType.USER_WALLET))
            total_debit = await session.scalar(select(func.coalesce(func.sum(Ledger.debit),0))
                                        .where(Ledger.user_id == current_user.user_id,
                                            Ledger.account_type == LedgerAccountType.USER_WALLET))
            total_balance = (total_credit or 0) - (total_debit or 0)
            currency = current_user.currency.value
            print(f"MEMO: {LedgerAccountType.PROVIDER_ESCROW.value} ")
            print(f"VoLTiX Deposit Successful: {total_deposit_amount / 100:.2f} {currency}")
            print(f" DEPOSIT FEE 2%: {deposit_fee / 100:.2f} {currency}")     
            print(f"Provider: {payment_transaction.provider.value}")
            print(f"Deposit Transaction Reference: {transaction.transaction_id}")
            print(f"{transaction.created_at}")
            print(f"\nCurrent VoLTiX Balance: {total_balance / 100:.2f} {currency}\n")
    # except Exception as e:
        # return (f"Deposit Failed..{e}")


async def transfer(user_id:uuid.UUID):
    """#Transfer money between two user in the same wallet.
    #Ensure that the entire transaction either succeeds in its entirety or fails in its entirety.
    #Check the current user as sender.
    #Check current user balance. 
    #Make the transaction for sender user.
    #Check the ricever user and reduce the balance from sender.
    # Save the ledger of the transaction."""
    
    print("Enter transfer details:")
    try:
        transfer_amount = int(input("Insert Transfer Amount In Cents:"))
    except ValueError:
        raise ValueError("Invalid Value. Insert Number Only.")
    receiver_email = input("Beneficiary Account :")
    receiver_phone = input("Beneficiary phone : ")
    password = input("To confirm transfer enter your password : ")
    
    async with AsyncSessionLocal()as session: 
        async with session.begin():
            user = await session.scalar(select(User).where(User.user_id == user_id,
                                                     User.currency == Currency.USD))
            if user is None:
                raise KeyError("User Account not found")
            choice_byte = password.encode("utf-8")
            if user.password is None:
                raise ValueError("Password hash is missing")
            if not bcrypt.checkpw(choice_byte, user.password):
                print("The Password Is Not Match. Transfer Failed..!!")
                return
            receiver_user = await session.scalar(select(User).where(User.email_address == receiver_email,
                                                User.phone_number == receiver_phone))
            if receiver_user is None:
                print("User account not existing.")
                return            
            sender_id = user.user_id
            receiver_id = receiver_user.user_id
            if sender_id == receiver_id:
                raise ValueError("Cannot transfer to your own account")
            locked_statement = (select(User).where(User.user_id.in_([sender_id, receiver_id]))
                                        .order_by(User.user_id)
                                            .with_for_update()
                                                .execution_options(populate_existing=True))
            locked_users = (await session.scalars(locked_statement)).all()
            if len(locked_users) != 2:
                raise ValueError("Sender or receiver account not found")
            sender_credit = await session.scalar(select(func.coalesce(func.sum(Ledger.credit),0))
                                                    .where(Ledger.user_id == user.user_id,
                                                        Ledger.account_type == LedgerAccountType.USER_WALLET))     
            sender_debit = await session.scalar(select(func.coalesce(func.sum(Ledger.debit),0))
                                                    .where(Ledger.user_id == user.user_id,
                                                        Ledger.account_type == LedgerAccountType.USER_WALLET))
            user_balance = (sender_credit or 0) - (sender_debit or 0)
            if transfer_amount <= 0:
                print(" The amount should be a positive")
                return
            if user_balance - transfer_amount < 0:
                print(" Insufficient balance")
                return
            user_total_balance = user_balance - transfer_amount
            transfer_transaction = Transaction(initiated_by_user_id=user.user_id,
                                            transaction_type=TransactionType.TRANSFER,
                                                status=TransactionStatus.PENDING,
                                                    amount=transfer_amount)
            session.add(transfer_transaction)
            await session.flush()
            ledger_debit = Ledger(user_id=user.user_id,
                                    transaction_id=transfer_transaction.transaction_id,                                   
                                        account_type=LedgerAccountType.USER_WALLET,
                                                    amount=transfer_amount,
                                                        credit=0,
                                                            debit=transfer_amount)
            ledger_credit = Ledger(user_id=receiver_user.user_id,
                                    transaction_id=transfer_transaction.transaction_id,     
                                        account_type=LedgerAccountType.USER_WALLET,
                                                amount=transfer_amount,
                                                    credit=transfer_amount,
                                                        debit=0)
            transfer_transaction.status = TransactionStatus.SUCCESS
            currency = user.currency.value
            session.add_all([ledger_debit, ledger_credit])
            user = f" {user.first_name} {user.last_name}"
            reciver = f"{receiver_user.first_name} {receiver_user.last_name}"
            transfer_type = f"{ledger_debit.account_type.value}"
            amount = transfer_transaction.amount
            print(f"\nTransfer VoLTiX  {transfer_type} {transfer_transaction.status.value}  {amount/100:.2f} {currency}")
            print(f"From: {user}  To:  {reciver}  VoLTiX {transfer_type}")
            print(f"Transfer Transaction Reference: {transfer_transaction.transaction_id}")
            print(f"{transfer_transaction.created_at}")
            print(f"\nCurrent VoLTiX Balance: {user_total_balance/100 :f} {currency}\n")
                                                
                                     
async def withdrawal(user_id:uuid.UUID):
    """#Check the user and balance.
    #Insert the external or gatway data.
    # Make the transaction for the user.
    # Reduce the user balance ,save the ledger and update the transaction status."""

    try:
        amount = int(input("Insert amount in cents  :"))
    except ValueError:
        raise ValueError("Invalid value, enter Number Only")
    if amount <= 0:
        print(" The amount should be a positive")
        return
    password=input("enter your password to confirm: ")

    async with AsyncSessionLocal()as session:
        async with session.begin():
            user = await session.scalar(select(User).where(User.user_id == user_id)
                                        .with_for_update().execution_options(populate_existing=True))
            if user is None:
                raise ValueError("User account not found")
            user_credit = await session.scalar(select(func.coalesce(func.sum(Ledger.credit),0))
                                                    .where(Ledger.user_id == user.user_id,
                                                    Ledger.account_type == LedgerAccountType.USER_WALLET))
            user_debit = await session.scalar(select(func.coalesce(func.sum(Ledger.debit),0))
                                                .where(Ledger.user_id == user.user_id,
                                                    Ledger.account_type == LedgerAccountType.USER_WALLET))
            user_balance = (user_credit or 0) - (user_debit or 0)
            withdrawal_fee=amount * Decimal("0.02")
            total_withdrawl_amount=amount + withdrawal_fee
            if user_balance - total_withdrawl_amount < 0:
                print(" Insufficient balance")
                return
            total_user_balance=user_balance - total_withdrawl_amount
            external_stmt= (select(ExternalPayments).where(ExternalPayments.user_id ==user.user_id))
            user_external_payment = (await session.scalars(external_stmt)).first()
            if user_external_payment is None:
                raise KeyError("ERROR..!! No External Payment Four User Found")
            choice_byte = password.encode("utf-8")
            if user.password is None:
                raise ValueError("Password is missing")
            if not bcrypt.checkpw(choice_byte, user.password):
                print("The Password Is Not Match..!!")
                return
            withdrawal_transaction = Transaction(initiated_by_user_id=user.user_id,
                                                ext_pay_id=user_external_payment.external_payment_id,
                                                    transaction_type=TransactionType.WITHDRAWAL,
                                                        status=TransactionStatus.PENDING,
                                                                amount=amount)
            session.add(withdrawal_transaction)
            await session.flush()
            wallet_debit = Ledger(user_id=user.user_id,
                                    transaction_id=withdrawal_transaction.transaction_id,
                                        account_type=LedgerAccountType.USER_WALLET,
                                            amount=amount,
                                                credit=0,
                                                    debit=total_withdrawl_amount)    
            provider_credit = Ledger(user_id=user.user_id,
                                    transaction_id=withdrawal_transaction.transaction_id,
                                        account_type=LedgerAccountType.PROVIDER_ESCROW,
                                            amount=amount,
                                                credit=amount,
                                                    debit=0)
            platform_credit = Ledger(user_id=user.user_id,
                                    transaction_id=withdrawal_transaction.transaction_id,
                                        account_type=LedgerAccountType.PLATFORM_REVENUE,
                                            amount=amount,
                                                credit=withdrawal_fee,
                                                    debit=0)
            withdrawal_transaction.status=TransactionStatus.SUCCESS
            session.add_all([wallet_debit, provider_credit, platform_credit])
            currency=user.currency.value
            external_gate_way=user.card_info
            print(f"\nMEMO: {LedgerAccountType.PROVIDER_ESCROW.value}")
            print(f"VoLTiX Withdrawal Successful: {amount/100:.2f} {currency}")
            print(f"2DEPOSIT FEE 2%: {withdrawal_fee / 100:.2f} {currency}")     
            print(f"PROVIDER_ESCROW: {external_gate_way}")
            print(f" Card Info.: {user.card_info}")
            print(f"Withdrawal Transaction Reference: {withdrawal_transaction.transaction_id}")
            print(f"{withdrawal_transaction.created_at}")
            print(f"\nCurrent VoLTiX Balance: {total_user_balance/100:.2f} {currency}\n")
    
        
async def transaction_report(user_id:uuid.UUID):
    """Showing user transaction saved in ledger """

    async with AsyncSessionLocal()as session:
        async with session.begin():
            user = await session.get(User, user_id)
            if user is None:
                raise KeyError("User Account not found")
            user_credit = await session.scalar(select(func.coalesce(func.sum(Ledger.credit),0))
                                                    .where(Ledger.user_id == user.user_id,
                                                    Ledger.account_type == LedgerAccountType.USER_WALLET))
            user_debit = await session.scalar(select(func.coalesce(func.sum(Ledger.debit),0))
                                                .where(Ledger.user_id == user.user_id,
                                                    Ledger.account_type == LedgerAccountType.USER_WALLET))        
            user_balance = (user_credit or 0) - (user_debit or 0)
            currency = user.currency.value
            report_stmt = (select(Ledger).where(Ledger.user_id == user.user_id)
                            .options(joinedload(Ledger.user),joinedload(Ledger.transaction)
                                .options(joinedload(Transaction.payment_methods),selectinload(Transaction.ledger_entries)
                                    .joinedload(Ledger.user)))
                .order_by(Ledger.created_at.asc()).execution_options(populate_existing=True))                      
            ledger_entries = (await session.scalars(report_stmt)).all()
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
                                f"              USER CREDIT: {ledger.credit/100:.2f} {currency}"
                                    f"           DEBIT: {ledger.debit/100:.2f} {currency}")
                    elif ledger.account_type == LedgerAccountType.PROVIDER_ESCROW:
                        if externalPayments is None:
                            raise KeyError("ERROR..!! No External Payment Four User Found")
                        print(f" PAYMENT PROVIDER: {externalPayments.provider}"     
                                f"    PAYMENT CREDIT: {ledger.credit/100:.2f} {currency}"   
                                    f"      DEBIT: {ledger.debit/100:.2f} {currency}")
                    elif ledger.account_type == LedgerAccountType.PLATFORM_REVENUE:
                        print(f" DEPOSIT FEE 2%: {LedgerAccountType.PLATFORM_REVENUE.value}"     
                                f"    PAYMENT CREDIT: {ledger.credit/100:.2f} {currency}"   
                                    f"      DEBIT: {ledger.debit/100:.2f} {currency}")
                        if externalPayments is None:
                            raise KeyError("ERROR..!! No External Payment Four User Found")
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
                                f"               USER CREDIT: {ledger.credit/100:.2f} {currency}"
                                    f"             DEBIT: {ledger.debit/100:.2f} {currency}")
                    elif ledger.account_type == LedgerAccountType.PROVIDER_ESCROW:
                        if externalPayments is None:
                            raise KeyError("ERROR..!! No External Payment Four User Found")
                        print(f" PAYMENT PROVIDER: {externalPayments.provider}"     
                                                        f"    PAYMENT CREDIT: {ledger.credit/100:.2f} {currency}"   
                                                            f"      DEBIT: {ledger.debit/100:.2f} {currency}")
                    elif ledger.account_type == LedgerAccountType.PLATFORM_REVENUE:
                        print(f" WITHDRAWAL FEE 2%: {LedgerAccountType.PLATFORM_REVENUE.value}"     
                                                        f"    PAYMENT CREDIT: {ledger.credit/100:.2f} {currency}"   
                                                            f"      DEBIT: {ledger.debit/100:.2f} {currency}")
                        if externalPayments is None:
                            raise KeyError("ERROR..!! No External Payment Four User Found")
                        print(f" PAYMENT REFERENCE: {externalPayments.external_reference}")
                        print(f" WITHDRAWAL Transaction REFERENCE: {transaction.transaction_id}")
                        print(f" DATE: {transaction.created_at}")      
            print("\n-----------------------")
            print(f" CURRENT VoLTiX BALANCE: {user_balance/100:.2f} {currency}")
            print("-------------------------\n")          
    
            
async def delete_account(user_id:uuid.UUID):
    """Delete user account and his external payments""" 

    password = input("Enter your password to confirm: ")   

    async with AsyncSessionLocal() as session:
        async with session.begin():
            user = await session.scalar(select(User).where(User.user_id == user_id)
                                        .with_for_update(nowait=True).execution_options(populate_existing=True))
            if user is None:
                raise ValueError("User account not found")
            if not user.is_active:
                raise ValueError("Account is already closed")
            total_debit = await session.scalar(select(func.coalesce(func.sum(Ledger.debit), 0))
                                        .where(Ledger.user_id == user.user_id,
                                            Ledger.account_type == LedgerAccountType.USER_WALLET))
            total_credit = await session.scalar(select(func.coalesce(func.sum(Ledger.credit), 0))
                                                .where(Ledger.user_id == user.user_id,
                                                    Ledger.account_type == LedgerAccountType.USER_WALLET))
            balance = (total_credit or 0) - (total_debit or 0)
            if balance != 0:
                raise ValueError(f"Please empty your balance before closing your account. "
                    f"Current balance: {balance}")
            password_byte = password.encode("utf-8")
            if user.password is None:
                raise ValueError("Password hash is missing")
            if not bcrypt.checkpw(password_byte, user.password):
                raise ValueError("Password mismatch")
            user.is_active = False
            user.closed_at = datetime.datetime.now(datetime.timezone.utc)
            user.first_name = None
            user.last_name = None
            user.email_address = None
            user.phone_number = None
            user.password = None
            user.card_info = None
            print("Your account has been successfully closed.")


