from Access.DataAccess import get_all_from_table


def validate_login(username, password):
    users = get_all_from_table("Users")
    for user in users:
        print(user.first_name)
