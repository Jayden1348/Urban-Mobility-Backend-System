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
            return user
        checkresult = account_logic.check_new_username(new_username)
        if checkresult:
            print(f"\nUsername not correct: {checkresult}")
            wait(2)

        else:
            if account_logic.change_username(user.username, new_username):
                print(f"\nUsername successfully changed to: {new_username}")
                wait(2)
                user.username = new_username
                return user
            else:
                print(f"\nUpdate failed, something went wrong")
