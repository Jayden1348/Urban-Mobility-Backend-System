from .general_presentation import *
from Logic import logs_logic, account_logic
from .menus import *


def start():    # Done
    while True:
        clear_screen()
        print("Welcome to the Urban Mobility System\n")
        print("1. Login")
        print("2. Exit")
        choice = input("\nSelect an option (1 or 2): ").strip().lower()
        clear_screen()

        if choice in ("1", "l"):
            user = account_presentation.identity_verification()
            if user:
                clear_screen()
                print(f"\nCorrect Login\nWelcome {user.username}!\n")
                logs_logic.new_log(user.username, "Logged in", None, 0)
                wait(1.5)
                user_role = account_logic.get_role_num(user.user_role)
                if user_role == 0:
                    super_admin_menu(user)
                elif user_role == 1:
                    system_admin_menu(user)
                elif user_role == 2:
                    service_engineer_menu(user)
                else:
                    print("Unknown role!")
                    wait(2)
            
        elif choice in ("2", "e"):
            print("Goodbye!")
            break
        else:
            print("\nInvalid option. Please try again.")
            wait(2)
