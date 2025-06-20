from .generaltools import *
from Logic import account_logic, logs_logic
from .menus import *


def start():
    logintries = 0
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
            user = account_logic.validate_password(username, password)
            if user:
                clear_screen()
                print(f"\nCorrect Login\nWelcome {username}!\n")
                logintries = 0
                logs_logic.new_log(user.username, "Logged in", None, 0)
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
                logintries += 1
                if logintries == 1:
                    logs_logic.new_log(
                        None, "Unsuccessful login", f"username: {username} is used for a login attempt with a wrong password", 0)
                if logintries == 2:
                    logs_logic.new_log(
                        None, "Unsuccessful login", f"Multiple failed login attempts in a row", 1)
                input("Press Enter to try again...")
        elif choice in ("2", "e"):
            print("Goodbye!")
            break
        else:
            print("\nInvalid option. Please try again.")
            wait(2)
