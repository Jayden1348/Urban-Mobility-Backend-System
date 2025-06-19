from .generaltools import *
from Logic import account_logic


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
            wait(2)
            user.password = new_password
            return
        else:
            print("\nUpdate failed, something went wrong.")
            wait(2)
            return
