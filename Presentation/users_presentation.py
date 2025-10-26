from .general_presentation import *
from Logic import user_logic, logs_logic, account_logic
import copy
import pyperclip


change_user_fields = ["username", "first_name", "last_name"]
display_user_fields = ["user_id"] + change_user_fields + ["user_role", "registration_date"]

def search_user(rolenum=None):
    filters = {"user_role": rolenum} if rolenum is not None else None
    display_objects_table(display_user_fields, "user", selection=False, filters=filters)


def add_user(user, rolenum=None):
    new_user_dict = get_object_values(
        change_user_fields, "user")

    if new_user_dict:
        if boolean_confirmation("add this user", f"You are about to add a new user, {new_user_dict['username']} ({'System Administrator' if rolenum == 1 else 'Service Engineer' if rolenum == 2 else 'Unknown Role'}).\n\n"):
            new_user_dict["user_role"] = rolenum
            new_password = account_logic.generate_password()
            new_user_dict["password"] = new_password
            new_user_id = user_logic.add_user(new_user_dict)
            if new_user_id:
                logs_logic.new_log(user.username, "Added user",
                                   f"{user.username} added user #{new_user_id}")
                pyperclip.copy(new_password)
                print(f"\nUser added successfully.\n\n{new_user_dict['username']}'s new temporary password is: {new_password}\n\nThe password has been copied and added to your clipboard\nPlease make sure to communicate this password securely to this user.")
                input("\nPress Enter to continue...")
            else:
                logs_logic.new_log(user.username, "Failed addition",
                                   f"{user.username} tried to add a new user")
                print("\nFailed to add user. Please check the data and try again.")
                wait(2)
        else:
            print("User addition cancelled.")
            wait(2)


def update_user(user, rolenum=None):
    filters = {"user_role": rolenum} if rolenum is not None else None
    selected_user = display_objects_table(display_user_fields, "user", selection=True, filters=filters)
    if selected_user is None:
        return

    old_user = copy.deepcopy(selected_user)
    changes = get_object_values(change_user_fields, "user", old_object=selected_user)

    if not changes:
        clear_screen()
        print("No changes made. Cancelling...")

    else:
        if boolean_confirmation("update this user", f"You are about to update user #{old_user.user_id}, {old_user.username} ({'System Administrator' if account_logic.get_role_num(old_user.user_role) == 1 else 'Service Engineer' if account_logic.get_role_num(old_user.user_role) == 2 else 'Unknown Role'})\n\n"):
            if user_logic.update_user(old_user.user_id, changes):
                logs_logic.new_log(user.username, "Updated user",
                                   f"{user.username} updated user #{old_user.user_id}")
                print("\nUser updated successfully.")
            else:
                logs_logic.new_log(selected_user.username, "Failed update",
                                   f"{selected_user.username} tried to update user #{old_user.user_id}")
                print("\nFailed to update user. Please check the data and try again.")
        else:
            print("User update cancelled.")
    wait(2)
    clear_screen()


def delete_user(user, rolenum=None):
    filters = {"user_role": rolenum} if rolenum is not None else None
    user_to_delete = display_objects_table(
        display_user_fields, "user", selection=True, filters=filters)
    if user_to_delete is None:
        return

    if boolean_confirmation("delete this user", f"You are about to delete user #{user_to_delete.user_id}, {user_to_delete.username} ({'System Administrator' if rolenum == 1 else 'Service Engineer' if rolenum == 2 else 'Unknown Role'})\n\n"):
        if user_logic.delete_user(user_to_delete.user_id, rolenum == 1):
            logs_logic.new_log(user.username, "Deleted user",
                               f"{user.username} deleted user #{user_to_delete.user_id}")
            print(f"\nUser {user_to_delete.username} deleted successfully.")
        else:
            logs_logic.new_log(user.username, "Failed deletion",
                               f"{user.username} tried to deleted user #{user_to_delete.user_id}")
            print("Failed to delete user!")
    else:
        print("User deletion cancelled.")
    wait(2)


def reset_password(user, rolenum=None):
    filters = {"user_role": rolenum} if rolenum is not None else None
    user_to_reset = display_objects_table(
        display_user_fields, "user", selection=True, filters=filters)
    if user_to_reset is None:
        return

    new_password = account_logic.generate_password()

    if boolean_confirmation("reset this user's password", f"You are about to reset the password for user #{user_to_reset.user_id}, {user_to_reset.username} ({'System Administrator' if rolenum == 1 else 'Service Engineer' if rolenum == 2 else 'Unknown Role'}).\n\n"):
        if user_logic.reset_password(user_to_reset.user_id, new_password):
            logs_logic.new_log(user.username, "Reset password",
                               f"{user.username} reset password for user #{user_to_reset.user_id}")
            pyperclip.copy(new_password)
            print(f"\nPassword reset successfully.\n\n{user_to_reset.username}'s new temporary password is: {new_password}\n\nThe password has been copied and added to your clipboard\nPlease make sure to communicate this password securely to this user.")
            input("\nPress Enter to continue...")
        else:
            logs_logic.new_log(user.username, "Failed password reset",
                               f"{user.username} tried to reset password for user #{user_to_reset.user_id}")
            print("\nFailed to reset password. Please try again.")
            wait(2)
    else:
        print("Password reset cancelled.")
        wait(2)


def show_all_users():
    display_objects_table(display_user_fields, "user", selection=False, only_display=True)