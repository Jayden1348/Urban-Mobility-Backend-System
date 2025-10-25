from Access import DataAccess
from Logic import general_logic, account_logic, backup_logic
from Utils.encryption import encryptor



def get_user(search_key="", identifiers=None, filters=None):
    if identifiers is None:
        identifiers = ["user_id", "username", "first_name", "last_name"]
    return DataAccess.search_item_in_table(
        "Users", search_key, identifiers=identifiers, filters=filters)


def add_user(new_user_data):
    new_user_data["registration_date"] = general_logic.get_today_date()
    new_user_data["password"] = account_logic.hash_password(new_user_data["password"])

    return DataAccess.add_item_to_table("Users", encryptor.encrypt_object_data("Users", new_user_data))


def update_user(user_id, updated_user_data):
    return DataAccess.update_item_from_table("Users", user_id, encryptor.encrypt_object_data("Users", updated_user_data))


def delete_user(user_id, del_related_data=False):
    success = DataAccess.remove_item_from_table("Users", user_id)
    
    if success and del_related_data:
        restore_codes_delete = backup_logic.get_restore_code(identifiers=[], filters={"generated_for_user_id": user_id})
        for code in restore_codes_delete:
            backup_logic.delete_restore_code(code)
        
    return success


def reset_password(user_id, new_password):
    return DataAccess.update_item_from_table(
        "Users", user_id, {"password": account_logic.hash_password(new_password)})


# Validation for new user values
def validate_new_user_values(field, v):
    if field == "username":
        is_valid, errormsg = account_logic.check_new_username(v.lower())
        if is_valid:
            return True, v.lower()
        else:
            return False, errormsg

    if field in ["first_name", "last_name"]:
        if len(v) <= 25:
            if general_logic.validate_char_string(v, letters=True, numbers=False, others=" -'"):
                return True, v.title()
            return False, "Only letters, spaces, and - are allowed."
        return False, "Maximum length is 25 characters."    

    return False, "The value entered does not meet the criteria for this field."

