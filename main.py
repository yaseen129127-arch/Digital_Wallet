from user import rejester, login


def menu_wallet(user):
    """The main menu inside the wallet"""
    
    print(f"wellcome {user.first_name}{user.last_name}\n")
    print("____________________________________\n")
    print("1. Vaultix Wallet")
    print("2. Balance")
    print("3. Send Money")
    print("4. Cash")
    print("5. Logout")




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

