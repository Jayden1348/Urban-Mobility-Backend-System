from .general_presentation import *
from . import account_presentation, backup_presentation, users_presentation, scooter_presentation, traveller_presentation
from Logic import account_logic

def scooter_functions(user):            # Accessible by SuperAdmin & SystemAdmin        # Done
    while True:
        clear_screen()
        print("Scooter functions:\n")
        print("1. Search scooter info")
        print("2. Advanced scooter search")
        print("3. Update scooter info")
        print("4. Add scooter")
        print("5. Delete scooter")
        print("6. Go back")
        choice = input("\nSelect an option (1-6): ").strip().lower()
        clear_screen()

        if choice == "1":
            scooter_presentation.search_scooter()
        elif choice == "2":
            scooter_presentation.advanced_scooter_search()
        elif choice == "3":
            scooter_presentation.update_scooter(user)
        elif choice == "4":
            scooter_presentation.add_scooter(user)
        elif choice == "5":
            scooter_presentation.delete_scooter(user)
        elif choice == "6" or choice == "b":
            return
        else:
            print("\nInvalid option. Please try again.")
            wait(1.5)


def traveller_functions(user):          # Accessible by SuperAdmin & SystemAdmin        # Done
    while True:
        clear_screen()
        print("Traveller functions:\n")
        print("1. Search traveller info")
        print("2. Advanced traveller search")
        print("3. Update traveller info")
        print("4. Add traveller")
        print("5. Delete traveller")
        print("6. Go back")
        choice = input("\nSelect an option (1-6): ").strip().lower()
        clear_screen()

        if choice == "1":
            traveller_presentation.search_traveller()
        elif choice == "2":
            traveller_presentation.advanced_traveller_search()
        elif choice == "3":
            traveller_presentation.update_traveller(user)
        elif choice == "4":
            traveller_presentation.add_traveller(user)
        elif choice == "5":
            traveller_presentation.delete_traveller(user)
        elif choice == "6" or choice == "b":
            return
        else:
            print("\nInvalid option. Please try again.")
            wait(1.5)


def user_functions(user, role_num):   # Accessible by SuperAdmin & SystemAdmin          # Done
    if role_num == 1:
        role_name = "System Admin"
    elif role_num == 2:
        role_name = "Service Engineer"
    else:
        return
    while True:
        clear_screen()
        print(f"{role_name} functions:\n")
        print(f"1. Search {role_name.lower()} info")
        print(f"2. Update {role_name.lower()} info")
        print(f"3. Add {role_name.lower()}")
        print(f"4. Delete {role_name.lower()}")
        print(f"5. Reset {role_name.lower()} password")
        print("6. Go back")
        choice = input("\nSelect an option (1-6): ").strip().lower()
        clear_screen()

        if choice == "1":
            users_presentation.search_user(role_num)
        elif choice == "2":
            users_presentation.update_user(user, role_num)
        elif choice == "3":
            users_presentation.add_user(user, role_num)
        elif choice == "4":
            users_presentation.delete_user(user, role_num)
        elif choice == "5":
            users_presentation.reset_password(user, role_num)
        elif choice == "6" or choice == "b":
            return
        else:
            print("\nInvalid option. Please try again.")


# Accessible by SuperAdmin & SystemAdmin, but some functions are accessible only by SuperAdmin
def system_backup_functions(user):
    role = account_logic.get_role_num(user.user_role)
    while True:
        clear_screen()
        if role == 0: # Super Admin
            print("System Backup functions:\n")
            print("1. Make backup")
            print("2. Restore backup")
            print("3. Search restore codes")
            print("4. Add backup restore code")
            print("5. Revoke backup restore code")
            print("6. Cleanup restore codes")
            print("7. Go back")

            choice = input(f"\nSelect an option (1-7): ").strip().lower()
            if choice == "1":
                backup_presentation.make_backup(user)
            elif choice == "2":
                backup_presentation.restore_backup(user)
            elif choice == "3":
                backup_presentation.search_restore_codes()
            elif choice == "4":
                backup_presentation.add_restore_code(user)
            elif choice == "5":
                backup_presentation.revoke_restore_code(user)
            elif choice == "6":
                backup_presentation.cleanup_restore_codes()
            elif choice == "7" or choice == "b":
                clear_screen()
                return
            else:
                print("\nInvalid option. Please try again.")
                wait(1.5)

        elif role == 1: # System Admin
            print("System Backup functions:\n")
            print("1. Make backup")
            print("2. Restore backup")
            print("3. Go back")

            choice = input(f"\nSelect an option (1-3): ").strip().lower()
            if choice == "1":
                backup_presentation.make_backup(user)
            elif choice == "2":
                backup_presentation.restore_backup(user)
            elif choice == "3" or choice == "b":
                clear_screen()
                return
            else:
                print("\nInvalid option. Please try again.")
                wait(1.5)
        else:
            return


def account_functions(user):        #  Accessible by SystemAdmin & Service Engineer     # Done
    while True:
        clear_screen()
        print("Account functions:\n")
        print("1. Update profile")
        print("2. Update password")
        print("3. Delete account")
        print("4. Go back")
        choice = input("\nSelect an option (1-4): ").strip().lower()
        clear_screen()

        if choice == "1":
            account_presentation.update_account(user)
        elif choice == "2":
            account_presentation.update_password(user)
        elif choice == "3":
            if account_presentation.delete_account(user) == "LogOut":
                return "LogOut"
        elif choice == "4" or choice == "b":
            return
        else:
            print("\nInvalid option. Please try again.")
            wait(1.5)
