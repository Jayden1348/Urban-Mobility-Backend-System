from Access import DataAccess
from datetime import date


def add_role(username, password, firstname, lastname, rolenum):
    today_str = date.today().isoformat()
    return DataAccess.add_item_to_table("Users", {"Username": username, "Password": password,
                                                  "FirstName": firstname, "LastName": lastname, "UserRole": rolenum, "RegistrationDate": today_str})
