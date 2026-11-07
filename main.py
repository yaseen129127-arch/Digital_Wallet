from account import rejester, login
from services import deposit,transfer,withdrawal,transaction_report,delete_account
from tables import User
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


DATABASE_URL=("postgresql+psycopg2://postgres:@localhost:60000/wallet")
engine=create_engine(DATABASE_URL)

def menu_wallet(user_id):
    """Internal menu wallet"""
    with Session(engine)as session:
        try:
            with session.begin():
                user=session.get(User, user_id)
            
                print("\n VoLtiX Wallet")
                print(f"  Wellcome {user.first_name} {user.last_name}")
                print("---------------------------------------------------\n")
                print("1. Deposit Account")
                print("2. Transfer Money")
                print("3. Cash Out")
                print("4. Transaction Report")
                print("5. Remove Account")
                print("6. Logout")
                while True:
                    choose=input("\nChoose an option: ")
                    if choose =="1":
                        deposit(user_id)
                        return menu_wallet(user_id)
                    elif choose == "2":
                        transfer(user_id)
                        return menu_wallet(user_id)
                    elif choose == "3":
                        withdrawal(user_id)
                        return menu_wallet(user_id)
                    elif choose == "4":
                        transaction_report(user_id)
                        return menu_wallet(user_id)
                    elif choose == "5":
                        delete_account(user_id)
                        return menu()
                    elif choose =="6":
                        print("\nGoodbye!")
                        return menu()
                    else:
                        print("\nInvalid choice..! Please Choose A Number From The Menu \n")
                        return menu_wallet(user_id)
        except:
            raise(f"login failed")
            


def menu():
    """The main menu for login to wallet"""
    print("\nWelcome To VoLtiX Wallet")
    print("______________________________\n")
    print("1. Create Account")
    print("2. Login")
    choice=input("\nChoose an option: \n")
    if choice == "1":
        rejester()    
    elif choice == "2":
        user = login()
        if user is not None:
            menu_wallet(user)
    else:
        print("\nInvalid choice. Please Choose A Number From The Menu \n.")
        return menu() 
menu()        

