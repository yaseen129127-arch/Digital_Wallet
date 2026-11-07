import bcrypt
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from tables import User,ExternalPayments , Currency

DATABASE_URL=("postgresql+psycopg2://postgres:@localhost:60000/wallet")
engine=create_engine(DATABASE_URL)




def rejester():
    """Create account """
    first_name=input("First Name : ")
    last_name=input ("Last Name : ")
    email_address=input("Email Address : ")
    phone_number=input("Phone Number : ")
    password=input("Password : ")
    card_info=input("Insert The Card Information : ")
    with Session(engine)as session:
        with session.begin():
            password_byet=password.encode("utf-8")
            salt=bcrypt.gensalt()
            hashed=bcrypt.hashpw(password_byet, salt)
            existing_email=session.scalar(select(User).where(User.email_address == email_address))
            if existing_email:
                print("/n Email Address is Already Used")
                return
            existing_phone=session.scalar(select(User).where(User.phone_number == phone_number))
            if existing_phone:
                print("/n Phone Number is Already Used")
                return
            new_user=User(first_name=first_name,
                            last_name=last_name, 
                                email_address=email_address, 
                                    phone_number=phone_number, 
                                        password_hash=hashed,
                                            currency=Currency.USD)
            session.add(new_user)
            session.flush()
            gate_way= ExternalPayments(user_id=new_user.user_id,
                                        provider="Stripe",
                                            external_reference="A123",
                                                card_info=card_info)
            session.add(gate_way)   
            print("\nAccount Created Successfully")
 

def login():
    """ Login to user account"""
    with Session(engine)as session:
        with session.begin():
            email=input("User Email : ")
            password=input("Password : ")     
            password_byte = password.encode("utf-8")       
            user=session.scalar(select(User).where(User.email_address == email))
            if user is None or not user.is_active:
                print("Account not found or closed")
                return None
            # if password != user.password_hash:
            password_stored=user.password_hash
            if bcrypt.checkpw(password_byte,password_stored):
                print("login successful")
                return user.user_id
            else:
                raise ValueError("Invalide password")     

    
