from .generaltools import *
from Logic import account_logic, logs_logic


def update_username(user):
    while True:
        clear_screen()
        print(f"Your current username is {user.username}\n")

        new_username = input(
            "Enter your new username (or press Enter to cancel): ").strip().lower()
        if not new_username:
            print("\nUsername update cancelled.")
            wait(2)
            return
        checkresult = account_logic.check_new_username(user, new_username)
        if checkresult:
            print(f"\nUsername not correct: {checkresult}")
            wait(2)
            continue

        if account_logic.change_username(user.username, new_username):
            print(f"\nUsername successfully changed to: {new_username}")
            logs_logic.new_log(user.username, "Updated username",
                               f"{user.username} changed his username to {new_username}", 0)
            wait(2)
            user.username = new_username
            return
        else:
            print(f"\nUpdate failed, something went wrong")
            wait(2)
            return


def update_password(user):
    while True:
        clear_screen()
        print(f"Change password for user: {user.username}\n")

        current_password = input(
            "Enter your current password (or press Enter to cancel): ").strip()
        if not current_password:
            print("\nPassword update cancelled.")
            wait(2)
            return

        if not account_logic.validate_password(user.username, current_password):
            print("\nCurrent password is incorrect.")
            wait(2)
            continue

        while True:
            clear_screen()
            new_password = input("\nEnter your new password: ").strip()
            confirm_password = input("Confirm your new password: ").strip()
            if new_password != confirm_password:
                print("\nPasswords do not match. Please try again.")
                wait(2)
                continue
            checkresult = account_logic.check_new_password(new_password)
            if checkresult:
                print(f"\n{checkresult}. Please try again.")
                wait(2)
                continue
            break

        if account_logic.change_password(user.username, new_password):
            print("\nPassword successfully changed.")
            logs_logic.new_log(user.username, "Updated password", None, 0)
            wait(2)
            user.password = new_password
            return
        else:
            print("\nUpdate failed, something went wrong.")
            wait(2)
            return


def update_profile(user):
    while True:
        clear_screen()
        print(f"Update profile for user: {user.username}\n")
        print(f"Current first name: {user.first_name}")
        print(f"Current last name:  {user.last_name}")

        new_first_name = input(
            "\nEnter new first name (or press Enter to keep current): ").strip().capitalize()
        new_last_name = input(
            "Enter new last name (or press Enter to keep current): ").strip().capitalize()

        # Use current values if nothing entered
        if not new_first_name:
            new_first_name = user.first_name
        if not new_last_name:
            new_last_name = user.last_name

        # If no changes, return
        if new_first_name == user.first_name and new_last_name == user.last_name:
            print("\nNo changes detected. Profile update cancelled.")
            wait(2)
            return

        # Confirm changes
        clear_screen()
        print("\nYou are about to update your profile to:")
        print(f"First name: {new_first_name}")
        print(f"Last name: {new_last_name}")
        if not areyousure("save these changes", f"New first name: {new_first_name}\nNew last name:  {new_last_name}\n"):
            print("Profile update cancelled.")
            wait(2)
            return

        # Update in database
        success = account_logic.change_profile(
            user.username,
            new_first_name,
            new_last_name,
        )
        if success:
            print("\nProfile updated successfully.")
            logs_logic.new_log(user.username, "Updated profile", None, 0)
            user.first_name = new_first_name
            user.last_name = new_last_name
            wait(2)
            return
        else:
            print("\nUpdate failed, something went wrong.")
            wait(2)
            return


def delete_account(user):
    while True:
        clear_screen()
        warning = f"Delete account for user: {user.username}\n\nWARNING: This action cannot be undone.\n"

        if not areyousure("delete your account", warning):
            print("Account deletion cancelled.")
            wait(2)
            return
        while True:
            clear_screen()
            print(warning)
            password = input(
                "Enter your password to confirm deletion (or press Enter to cancel): ").strip()
            if not password:
                print("\nAccount deletion cancelled.")
                wait(2)
                return

            if not account_logic.validate_password(user.username, password):
                print("\nPassword is incorrect.")
                wait(2)
                continue

            if account_logic.delete_account(user.username):
                print("\nAccount deleted successfully.")
                logs_logic.new_log(user.username, "Deleted user",
                                   f"{user.username} deleted his own account", 0)
                wait(2)
                print("\nLogging out. Goodbye!")
                wait(2)
                return "LogOut"
            else:

                print("\nAccount deletion failed, something went wrong.")
                wait(2)
                return
