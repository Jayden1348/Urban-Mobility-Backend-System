from Access import DataAccess
import re


def check_new_username(new_username):

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


def change_username(old_username, new_username):
    # Sending to the Access layer to change username
    return DataAccess.update_item_from_table("Users", old_username, {"Username": new_username})
