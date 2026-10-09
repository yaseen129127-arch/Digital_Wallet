from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from tables import User




DATABASE_URL = (
    "postgresql+psycopg2://postgres:hanoyaseen@localhost:60000/wallet"
)

engine = create_engine(DATABASE_URL)

def rejester():
    """Create account """
    first_name = input("First Name : ")
    last_name = input ("Last Name : ")
    email_address = input("Email Address : ")
    phone_number = input("Phone Number : ")
    password_hash = input("Password : ")
    with Session (engine) as session :
        existing_email = session.scalar(select(User).where (User.email_address == email_address))
        if existing_email :
            print("/n Email Address is Already Used")
            return
    with Session (engine) as session :
        existing_phone = session.scalar(select(User).where (User.phone_number == phone_number))
        if existing_phone :
            print("/n Email Address is Already Used")
            return
    
    new_user = User(first_name =first_name, last_name = last_name, email_address = email_address, phone_number =phone_number, password_hash= password_hash )
    session.add(new_user)   
    session.commit()

def login():
    """ Login to user account"""
    email = input("User Email : ")
    password = input("Password : ")
    with Session (engine) as session :
        user = session.scalar(select(User).where (User.email_address == email))
        if user is None:
            print("No account is associated with this email address")
            return None
        if password != user.password_hash :
            print("Wrong Password !")
            return None
        
        return user
    
