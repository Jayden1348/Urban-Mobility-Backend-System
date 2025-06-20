from .generaltools import *
from . import account_presentation, users_presentation


def scooter_functions():  # Accessible by SuperAdmin & SystemAdmin
    while True:
        clear_screen()
        print("Scooter related functions:\n")
        print("1. Search scooter info")
        print("2. Update scooter info")
        print("3. Add scooter")
        print("4. Delete scooter")
        print("5. Go back")
        choice = input("\nSelect an option (1-5): ").strip().lower()
        clear_screen()

        if choice == "1":
            pass
            # Search scooter info
        elif choice == "2":
            pass
            # Update scooter info
        elif choice == "3":
            pass
            # Add scooter
        elif choice == "4":
            pass
            # Delete scooter
        elif choice == "5" or choice == "b":
            return
        else:
            print("\nInvalid option. Please try again.")
            wait(2)


def traveller_functions():  # Accessible by SuperAdmin & SystemAdmin
    while True:
        clear_screen()
        print("Traveller related functions:\n")
        print("1. Search traveller info")
        print("2. Update traveller info")
        print("3. Add traveller")
        print("4. Delete traveller")
        print("5. Go back")
        choice = input("\nSelect an option (1-5): ").strip().lower()
        clear_screen()

        if choice == "1":
            pass
            # Search traveller info
        elif choice == "2":
            pass
            # Update traveller info
        elif choice == "3":
            pass
            # Add traveller
        elif choice == "4":
            pass
            # Delete traveller
        elif choice == "5" or choice == "b":
            return
        else:
            print("\nInvalid option. Please try again.")
            wait(2)


def service_engineer_functions():   # DONE Accessible by SuperAdmin & SystemAdmin
    while True:
        clear_screen()
        print("Service engineer related functions:\n")
        print("1. Update service engineer info")
        print("2. Add service engineer")
        print("3. Delete service engineer")
        print("4. Go back")
        choice = input("\nSelect an option (1-4): ").strip().lower()
        clear_screen()

        if choice == "1":
            users_presentation.update_user(2)
        elif choice == "2":
            users_presentation.add_user(2)
        elif choice == "3":
            users_presentation.delete_user(2)
        elif choice == "4" or choice == "b":
            return
        else:
            print("\nInvalid option. Please try again.")


def system_admin_functions():       # DONE Accessible only by SuperAdmin
    while True:
        clear_screen()
        print("System admin related functions:\n")
        print("1. Update system admin info")
        print("2. Add system admin")
        print("3. Delete system admin")
        print("4. Go back")
        choice = input("\nSelect an option (1-4): ").strip().lower()
        clear_screen()

        if choice == "1":
            users_presentation.update_user(1)
        elif choice == "2":
            users_presentation.add_user(1)
        elif choice == "3":
            users_presentation.delete_user(1)
        elif choice == "4" or choice == "b":
            return
        else:
            print("\nInvalid option. Please try again.")


# Accessible by SuperAdmin & SystemAdmin, but some functions are accessible only by SuperAdmin
def backend_system_functions(user):
    role = user.user_role
    while True:
        clear_screen()
        print("Backend System related functions:\n")
        print("1. Make backup")
        print("2. Restore backup")

        if role == 0:
            print("3. Allow System Admin to restore")
            print("4. Revoke System Admin to restore")
            print("5. Go back")
        else:
            print("3. Go back")
        choice = input(
            f"\nSelect an option (1-{5 if role == 0 else 3}): ").strip().lower()
        clear_screen()

        if choice == "1":
            pass
            # Make backup of backend system
        elif choice == "2":
            pass
            # Restore backup of backend system (! If the user is a SystemAdmin, it needs a code. The SuperAdmin has full clearance)
            # Give "role" to a function that checks if the user is SystemAdmin and needs the code.
        elif (choice == "3" or choice == "b") and role != 0:
            return

        elif choice == "3" and role == 0:
            pass
            # Allow a System Admin to restore a backup (generates a code the System admin should use to restore a backup)
        elif choice == "4" and role == 0:
            pass
            # Revoke a restore code for System Admin
        elif (choice == "5" or choice == "b") and role == 0:
            return
        else:
            print("\nInvalid option. Please try again.")
            wait(2)


def account_functions(user):        # DONE Accessible by SystemAdmin & Service Engineer
    while True:
        clear_screen()
        print("Account functions:\n")
        print("1. Update username")
        print("2. Update password")
        print("3. Update profile")
        print("4. Delete account")
        print("5. Go back")
        choice = input("\nSelect an option (1-5): ").strip().lower()
        clear_screen()

        if choice == "1":
            account_presentation.update_username(user)
        elif choice == "2":
            account_presentation.update_password(user)
        elif choice == "3":
            account_presentation.update_profile(user)
        elif choice == "4":
            if account_presentation.delete_account(user) == "LogOut":
                return "LogOut"
        elif choice == "5" or choice == "b":
            return
        else:
            print("\nInvalid option. Please try again.")
            wait(2)
