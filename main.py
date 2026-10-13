from account import rejester, login
from services import charge


def menu_wallet(user):
    """The main menu inside the wallet"""
    
    print(f"Wellcome {user.first_name} {user.last_name}\n")
    print("____________________________________\n")
    print(" Vaultix Wallet")
    print("____________________________________\n")
    print("1. Charge Vaultiix")
    print("2. Send Money")
    print("3. Cash Out")
    print("4. Vaultix Report")
    print("5. Logout")
    while True:
        choose = input("\nChoose an option: ")
        if choose =="1" :
            charge(user)
        else :
            return




def main():
    """The main menu for login to wallet"""
    
    print("\nWelcome To Vaultix Wallet")
    print("______________________________\n")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")
    while True:
    
        choice = input("\nChoose an option: ")

        if choice == "1":
            rejester()
            
        elif choice == "2":
            user = login()
            if user is not None:
                menu_wallet(user)

        elif choice == "3":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid choice. Please try again.")
            #return
main()

