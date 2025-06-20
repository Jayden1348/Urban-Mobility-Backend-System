from .generaltools import *
from Logic import account_logic, user_logic, logs_logic


def add_user(user, rolenum):
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
        temp_password = account_logic.generate_password()
        success = user_logic.add_user(
            username, temp_password, first_name, last_name, rolenum)
        if success:
            print(f"\n{'System Administrator' if rolenum == 1 else 'Service Engineer' if rolenum == 2 else 'Unknown Role'} successfully created.")
            logs_logic.new_log(
                user.username, "Added user", f"{user.username} added {username} as a {'System Administrator' if rolenum == 1 else 'Service Engineer' if rolenum == 2 else 'Unknown Role'}", 0)
            wait(2)
            print(f"{username}'s temporary password is: {temp_password}")
            wait(2)
            return
        else:
            print("\nUpdate failed, something went wrong.")
            wait(2)
            return


def delete_user(user, rolenum):
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
        user = user_logic.get_user_by_username(username, rolenum)
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

        success = user_logic.delete_user(username)
        if success:
            print(f"\n{'System Administrator' if rolenum == 1 else 'Service Engineer' if rolenum == 2 else 'Unknown Role'} successfully deleted.")
            logs_logic.new_log(
                user.username, "Deleted user", f"{user.username} deleted {username}", 0)
            wait(2)
            return
        else:
            print("\nDeletion failed, something went wrong.")
            wait(2)
            return


def update_user(user, rolenum):
    while True:
        clear_screen()
        print(
            f"Update a {'System Administrator' if rolenum == 1 else 'Service Engineer' if rolenum == 2 else 'Unknown Role'}\n"
        )

        old_username = input(
            "Enter username to update (or press Enter to cancel): "
        ).strip().lower()
        if not old_username:
            print("\nUser update cancelled.")
            wait(2)
            return

        # Check if user exists and has the correct role
        user = user_logic.get_user_by_username(old_username, rolenum)
        if not user:
            print(
                f"\nNo user found or this user is not a {'System Administrator' if rolenum == 1 else 'Service Engineer' if rolenum == 2 else 'Unknown Role'}.")
            wait(2)
            continue

        while True:
            clear_screen()
            print(
                f"Update a {'System Administrator' if rolenum == 1 else 'Service Engineer' if rolenum == 2 else 'Unknown Role'}"
            )

            print(f"\nCurrent username: {old_username}")
            new_username = input(
                "\nEnter new username (or press Enter to keep current): ").strip().lower()
            if not new_username:
                new_username = old_username
            else:
                checkresult = account_logic.check_new_username(
                    user, new_username)
                if checkresult:
                    print(f"\nUsername not correct: {checkresult}")
                    wait(2)
                    continue

            while True:
                message = f"""Update a {'System Administrator' if rolenum == 1 else 'Service Engineer' if rolenum == 2 else 'Unknown Role'}\n
Username: {new_username}\n
Do you want to change the password to a randomly generated one? (y/n): """
                change_password = areyousure_custommessage(message)
                if change_password:
                    new_password = account_logic.generate_password()
                else:
                    new_password = user.password

                print(f"\nCurrent first name: {user.first_name}")
                new_first_name = input(
                    "Enter new first name (or press Enter to keep current): ").strip().capitalize()
                if not new_first_name:
                    new_first_name = user.first_name

                print(f"\nCurrent last name: {user.last_name}")
                new_last_name = input(
                    "Enter new last name (or press Enter to keep current): ").strip().capitalize()
                if not new_last_name:
                    new_last_name = user.last_name

                clear_screen()
                if (new_username == user.username and new_password == user.password and new_first_name == user.first_name and new_last_name == user.last_name):
                    print("\nNo changes detected. User update cancelled.")
                    wait(2)
                    return

                finalcheck = f"""You are about to update {'System Administrator' if rolenum == 1 else 'Service Engineer' if rolenum == 2 else 'Unknown Role'}\n
Username: {new_username}
Password: {'new randomly generated' if change_password else 'old password'}
First name: {new_first_name}
Last name: {new_last_name}\n
"""
                if not areyousure("update this user", finalcheck):
                    print("User update cancelled.")
                    wait(2)
                    return

                success = user_logic.update_user(
                    old_username, new_username, new_password, new_first_name, new_last_name)
                if success:
                    print(
                        f"\n{'System Administrator' if rolenum == 1 else 'Service Engineer' if rolenum == 2 else 'Unknown Role'} successfully updated.")
                    logs_logic.new_log(
                        user.username, "Updated user", f"{user.username} updated {new_username}'s account", 0)
                    wait(2)
                    if change_password:
                        print(
                            f"\n{new_username}'s temporary password is: {new_password}")
                        wait(3)
                    return
                else:
                    print("\nUpdate failed, something went wrong.")
                    wait(2)
                    return


def show_all_users():
    clear_screen()
    users = user_logic.get_all_users()
    if not users:
        print("No users found.")
        wait(2)
        return

    print("All Users:\n")
    print(f"{'Username':<15} {'Role':<11} {'First Name':<15} {'Last Name':<15} {'Registration Date':<15}")
    print("-" * 70)
    for user in users:
        username = getattr(user, "username", getattr(user, "Username", ""))
        role = getattr(user, "user_role", getattr(user, "UserRole", ""))
        # Convert role number to string if needed
        if isinstance(role, int):
            if role == 0:
                role_str = "SuperAdmin"
            elif role == 1:
                role_str = "SysAdmin"
            elif role == 2:
                role_str = "Engineer"
            else:
                role_str = str(role)
        else:
            role_str = str(role)
        first_name = getattr(user, "first_name",
                             getattr(user, "FirstName", ""))
        last_name = getattr(user, "last_name", getattr(user, "LastName", ""))
        reg_date = getattr(user, "registration_date",
                           getattr(user, "RegistrationDate", ""))
        print(
            f"{str(username or ''):<15} {str(role_str or ''):<11} {str(first_name or ''):<15} {str(last_name or ''):<15} {str(reg_date or ''):<15}")

    input("\nPress Enter to return...")
    clear_screen()
