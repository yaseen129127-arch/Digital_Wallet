import asyncio
from services import rejister, login, menu_wallet
from models import User
# from sqlalchemy.orm import Session
# from database import SessionLocal
# from sqlalchemy import select
# from schemas import RejisterRequest
from pydantic import ValidationError




async def menu():
    """The main menu for login to wallet"""
    print("\nWelcome To VoLtiX Wallet")
    print("______________________________\n")
    print("1. Create Account")
    print("2. Login")
    choice=input("\nChoose an option: \n")
    if choice == "1":
        try:
            await rejister()     
        except ValidationError as e:
            print(f"\nRegistration failed: {e}")
            return await menu()
    elif choice == "2":
        user_id = await login()
        if user_id is not None:
            await menu_wallet(user_id)
    else:
        print("\nInvalid choice. Please Choose A Number From The Menu \n.")
if __name__ == "__main__":
    asyncio.run(menu())

