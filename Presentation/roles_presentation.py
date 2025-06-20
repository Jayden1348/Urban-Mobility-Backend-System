from .generaltools import *
from Logic import account_logic, roles_logic


def add_role(rolenum):
    while True:
        clear_screen()
        print(
            f"Add a new {'System Administrator' if rolenum == 1 else 'Service Engineer' if rolenum == 2 else 'Unknown Role'}\n")

        username = input(
            "Enter username: ").strip().lower()
        checkresult = account_logic.check_new_username(None, username)
        if checkresult:
            print(f"\nUsername not correct: {checkresult}")
            wait(2)
            continue

        first_name = input(
            "\nEnter new first name: ").strip().capitalize()
        last_name = input(
            "Enter new last name: ").strip().capitalize()

        clear_screen()
        finalcheck = f"""You are about to make a {'System Administrator' if rolenum == 1 else 'Service Engineer' if rolenum == 2 else 'Unknown Role'}\n
Username: {username}
First name: {first_name}
Last name: {last_name}\n
"""
        if not areyousure("make this user", finalcheck):
            print("User creation cancelled.")
            wait(2)
            return

        success = roles_logic.add_role(
            username, account_logic.generate_password(), first_name, last_name, rolenum)
        if success:
            print(f"\n{'System Administrator' if rolenum == 1 else 'Service Engineer' if rolenum == 2 else 'Unknown Role'} successfully created.")
            wait(2)
            return
        else:
            print("\nUpdate failed, something went wrong.")
            wait(2)
            return
