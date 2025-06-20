from .generaltools import *
from Logic import account_logic, roles_logic


def add_role(rolenum):
    while True:
        clear_screen()
        print(
            f"Add a new {'System Administrator' if rolenum == 1 else 'Service Engineer' if rolenum == 2 else 'Unknown Role'}\n")

        username = input(
            "Enter username (or press Enter to cancel): ").strip().lower()
        if not username:
            print("\nUser creation cancelled.")
            wait(2)
            return
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


def delete_role(rolenum):
    while True:
        clear_screen()
        print(
            f"Delete a {'System Administrator' if rolenum == 1 else 'Service Engineer' if rolenum == 2 else 'Unknown Role'}\n"
        )

        username = input(
            "Enter username to delete (or press Enter to cancel): "
        ).strip().lower()
        if not username:
            print("\nUser deletion cancelled.")
            wait(2)
            return

        # Check if user exists and has the correct role
        user = roles_logic.get_role_by_username(username, rolenum)
        if not user:
            print(
                f"\nNo user found or this user is not a {'System Administrator' if rolenum == 1 else 'Service Engineer' if rolenum == 2 else 'Unknown Role'}.")
            wait(2)
            continue

        clear_screen()
        finalcheck = f"You are about to delete {user.username} ({'System Administrator' if rolenum == 1 else 'Service Engineer' if rolenum == 2 else 'Unknown Role'})\n\n"
        if not areyousure("delete this user", finalcheck):
            print("User deletion cancelled.")
            wait(2)
            return

        success = roles_logic.delete_role(username)
        if success:
            print(f"\n{'System Administrator' if rolenum == 1 else 'Service Engineer' if rolenum == 2 else 'Unknown Role'} successfully deleted.")
            wait(2)
            return
        else:
            print("\nDeletion failed, something went wrong.")
            wait(2)
            return
