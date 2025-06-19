from .generaltools import *
from Logic.loginlogic import validate_login
from .menus import *


def start():
    while True:
        clear_screen()
        print("Welcome to the Urban Mobility System\n")
        print("1. Login")
        print("2. Exit")
        choice = input("\nSelect an option: ")
        clear_screen()

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            user = validate_login(username, password)
            if user:
                clear_screen()
                print(f"\nCorrect Login\nWelcome {username}!\n")
                wait(2)
                if user.user_role == 0:
                    super_admin_menu()
                elif user.user_role == 1:
                    system_admin_menu()
                elif user.user_role == 2:
                    service_engineer_menu()
                else:
                    print("Unknown role!")
                    wait(2)
            else:
                print("\nUsername or password is incorrect!")
                wait(2)
        elif choice == "2":
            print("Goodbye!")
            break
