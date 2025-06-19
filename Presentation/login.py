from .generaltools import *
from Logic import loginlogic
from .menus import *


def start():
    while True:
        clear_screen()
        print("Welcome to the Urban Mobility System\n")
        print("1. Login")
        print("2. Exit")
        choice = input("\nSelect an option (1 or 2): ").strip().lower()
        clear_screen()

        if choice in ("1", "l"):
            username = input("Username: ")
            password = input("Password: ")
            user = loginlogic.validate_login(username, password)
            if user:
                clear_screen()
                print(f"\nCorrect Login\nWelcome {username}!\n")
                wait(2)
                if user.user_role == 0:
                    super_admin_menu(user)
                elif user.user_role == 1:
                    system_admin_menu(user)
                elif user.user_role == 2:
                    service_engineer_menu(user)
                else:
                    print("Unknown role!")
                    wait(2)
            else:
                print("\nUsername or password is incorrect!")
                wait(2)
        elif choice in ("2", "e"):
            print("Goodbye!")
            break
        else:
            print("\nInvalid option. Please try again.")
            wait(2)
