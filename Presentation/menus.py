from .general_presentation import *
from .nested_menus import *
from . import users_presentation
from .scooter_presentation import *


def super_admin_menu(user):
    while True:
        print(f"Main Menu ({user.username})\n")
        print("1. Scooter functions")
        print("2. Traveller functions")
        print("3. Service engineer functions")
        print("4. System Admin functions")
        print("5. System Backup functions")
        print("6. See logs")
        print("7. See users & roles")
        print("8. Log out")
        choice = input("\nSelect an option (1-8): ").strip().lower()
        clear_screen()

        if choice == "1":
            scooter_functions(user)

        elif choice == "2":
            traveller_functions(user)

        elif choice == "3":
            user_functions(user, 2)

        elif choice == "4":
            user_functions(user, 1)

        elif choice == "5":
            system_backup_functions(user)

        elif choice == "6":
            log_functions()

        elif choice == "7":
            users_presentation.show_all_users()

        elif choice == "8" or choice == "b":
            if boolean_confirmation("log out"):
                return
        else:
            print("\nInvalid option. Please try again.")
            wait(1.5)
            clear_screen()


def system_admin_menu(user):
    while True:
        print(f"Main Menu ({user.username})\n")
        print("1. Scooter functions")
        print("2. Traveller functions")
        print("3. Service engineer functions")
        print("4. System Backup functions")
        print("5. See logs")
        print("6. See users & roles")
        print("7. My account")
        print("8. Log out")
        choice = input("\nSelect an option (1-8): ").strip().lower()
        clear_screen()

        if choice == "1":
            scooter_functions(user)

        elif choice == "2":
            traveller_functions(user)

        elif choice == "3":
            user_functions(user, 2)

        elif choice == "4":
            system_backup_functions(user)

        elif choice == "5":
            log_functions()

        elif choice == "6":
            users_presentation.show_all_users()

        elif choice == "7":
            if account_functions(user) == "LogOut":
                return
        elif choice == "8" or choice == "b":
            if boolean_confirmation("log out"):
                return
        else:
            print("\nInvalid option. Please try again.")
            wait(1.5)
            clear_screen()


def service_engineer_menu(user):
    while True:
        print(f"Main Menu ({user.username})\n")
        print("1. Search scooter info")
        print("2. Advanced scooter search")
        print("3. Update scooter info")
        print("4. My account")
        print("5. Log out")
        choice = input("\nSelect an option (1-5): ").strip().lower()
        clear_screen()

        if choice == "1":
            scooter_presentation.search_scooter()

        elif choice == "2":
            scooter_presentation.advanced_scooter_search()

        elif choice == "3":
            scooter_presentation.update_scooter(user)
            
        elif choice == "4":
            if account_functions(user) == "LogOut":
                return
        elif choice == "5" or choice == "b":
            if boolean_confirmation("log out"):
                return
        else:
            print("\nInvalid option. Please try again.")
            wait(1.5)
            clear_screen()
