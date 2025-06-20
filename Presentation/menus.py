from .generaltools import *
from .nested_menus import *
from . import logs_presentation, users_presentation


def super_admin_menu(user):  # DONE
    while True:
        print("Main Menu (Super Admin)\n")
        print("1. Scooter related functions")
        print("2. Traveller related functions")
        print("3. Service engineer related functions")
        print("4. System Admin related functions")
        print("5. Backend system related functions")
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
            service_engineer_functions(user)

        elif choice == "4":
            system_admin_functions(user)

        elif choice == "5":
            backend_system_functions(user)

        elif choice == "6":
            logs_presentation.show_all_logs()

        elif choice == "7":
            users_presentation.show_all_users()

        elif choice == "8" or choice == "b":
            if areyousure("log out"):
                return
        else:
            print("\nInvalid option. Please try again.")
            wait(2)
            clear_screen()


def system_admin_menu(user):  # DONE
    while True:
        print("Main Menu (System Admin)\n")
        print("1. Scooter related functions")
        print("2. Traveller related functions")
        print("3. Service engineer related functions")
        print("4. Backend system related functions")
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
            service_engineer_functions(user)

        elif choice == "4":
            backend_system_functions(user)

        elif choice == "5":
            logs_presentation.show_all_logs()
        elif choice == "6":
            users_presentation.show_all_users()

        elif choice == "7":
            account_functions(user)

        elif choice == "8" or choice == "b":
            if areyousure("log out"):
                return
        else:
            print("\nInvalid option. Please try again.")
            wait(2)
            clear_screen()


def service_engineer_menu(user):
    while True:
        print("Main Menu (System Engineer)\n")
        print("1. Search scooter info")
        print("2. Update scooter info")
        print("3. My account")
        print("4. Log out")
        choice = input("\nSelect an option (1-4): ").strip().lower()
        clear_screen()

        if choice == "1":
            pass
            # Search scooter info
        elif choice == "2":
            pass
            # Update SOME (not all) scooter info
            # Servcie engineer can only change: state_of_charge, target_range_soc_min, target_range_soc_max, latitude, longitude, out_of_service, mileage, in_service_date
            # Service engineer can NOT change: brand, model, serial_number, top_speed, battery_capacity
        elif choice == "3":
            if account_functions(user) == "LogOut":
                return
        elif choice == "4" or choice == "b":
            if areyousure("log out"):
                return
        else:
            print("\nInvalid option. Please try again.")
            wait(2)
            clear_screen()
