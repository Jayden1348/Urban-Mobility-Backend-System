from Access import DataAccess


def validate_login(username, password):
    users = DataAccess.get_all_from_table("Users")
    for user in users:
        if user.username == username:
            if user.password == password:
                return user
            else:
                return None
    return None
