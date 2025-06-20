from Access import DataAccess
from datetime import date


def add_role(username, password, firstname, lastname, rolenum):
    today_str = date.today().isoformat()
    return DataAccess.add_item_to_table("Users", {"Username": username, "Password": password,
                                                  "FirstName": firstname, "LastName": lastname, "UserRole": rolenum, "RegistrationDate": today_str})


def get_role_by_username(username, rolenum):
    user = DataAccess.get_one_from_table("Users", username)
    if not user:
        return None
    if user.user_role != rolenum:
        return None
    return user


def delete_role(username):
    return DataAccess.remove_item_from_table("Users", username)
