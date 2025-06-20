from Access import DataAccess
import re


def validate_password(username, password):
    users = DataAccess.get_all_from_table("Users")
    for user in users:
        if user.username == username:
            if user.password == password:
                return user
            else:
                return None
    return None


def check_new_username(user, new_username):

    # Check if the new username is the same as the current one (case-insensitive)
    if user.username.lower() == new_username.lower():
        return "New username must be different from the current username!"

    # Length check
    if not (8 <= len(new_username) <= 10):
        return "Username must be between 8 and 10 characters!"

    # Start character check
    if not re.match(r"^[a-zA-Z_]", new_username):
        return "Username must start with a letter or underscore (_)!"

    # Allowed characters check
    if not re.match(r"^[a-zA-Z0-9_'.]+$", new_username):
        return "Username can only contain letters, numbers, underscores (_), apostrophes ('), and periods (.)"

    # Uniqueness check (case-insensitive)
    users = DataAccess.get_all_from_table("Users")
    existing_usernames = {u.username.lower() for u in users}
    if new_username in existing_usernames:
        return "This username is already taken. Please choose another one."

    return None


def check_new_password(new_password):

    # Length check
    if not (12 <= len(new_password) <= 30):
        return "Password must be between 12 and 30 characters!"

    # Allowed characters check
    allowed_specials = r"~!@#$%&_\-\+=`|\(\){}\[\]:;'<>,\.?/"
    allowed_pattern = rf"^[a-zA-Z0-9{re.escape(allowed_specials)}]+$"
    if not re.match(allowed_pattern, new_password):
        return "Password contains invalid characters!"

    # At least one lowercase letter
    if not re.search(r"[a-z]", new_password):
        return "Password must contain at least one lowercase letter!"

    # At least one uppercase letter
    if not re.search(r"[A-Z]", new_password):
        return "Password must contain at least one uppercase letter!"

    # At least one digit
    if not re.search(r"\d", new_password):
        return "Password must contain at least one digit!"

    # At least one special character
    if not re.search(rf"[{re.escape(allowed_specials)}]", new_password):
        return "Password must contain at least one special character!"

    return None


def change_username(username, new_username):
    # Sending to the Access layer to change username
    return DataAccess.update_item_from_table("Users", username, {"Username": new_username})


def change_password(username, new_password):
    # Sending to the Access layer to change password
    return DataAccess.update_item_from_table("Users", username, {"Password": new_password})


def change_profile(username, new_first_name, new_last_name):
    return DataAccess.update_item_from_table("Users", username, {"FirstName": new_first_name, "LastName": new_last_name})


def delete_account(username):
    return DataAccess.remove_item_from_table("Users", username)
