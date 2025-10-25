from Access import DataAccess
from Logic import general_logic
from Utils.encryption import encryptor

                
CITIES = ["Rotterdam", "Amsterdam", "Utrecht", "Eindhoven", "Groningen", "Maastricht", "Delft", "Leiden", "Nijmegen", "Haarlem"]


def get_traveller(search_key="", identifiers=None, filters=None):  # Done
    if identifiers is None:
        identifiers = ["customer_id", "first_name", "last_name", "email_address"]
    return DataAccess.search_item_in_table(
        "Travellers", search_key, identifiers=identifiers, filters=filters)


def add_traveller(new_traveller_data):  # Done
    if "gender" in new_traveller_data:
        new_traveller_data["gender"] = 1 if new_traveller_data["gender"] == "Female" else 0
    new_traveller_data["registration_date"] = general_logic.get_today_date()

    return DataAccess.add_item_to_table("Travellers", encryptor.encrypt_object_data("Travellers", new_traveller_data))


def update_traveller(customer_id, updated_traveller_data):    # Done
    if "gender" in updated_traveller_data:
        updated_traveller_data["gender"] = 1 if updated_traveller_data["gender"] == "Female" else 0

    return DataAccess.update_item_from_table("Travellers", customer_id, encryptor.encrypt_object_data("Travellers", updated_traveller_data))


def delete_traveller(customer_id):   # Done
    return DataAccess.remove_item_from_table("Travellers", customer_id)


# Validation for new traveller values
def validate_new_traveller_values(field, v):    # Done
    if field in ["first_name", "last_name"]:
        if len(v) <= 25:
            if general_logic.validate_char_string(v, letters=True, numbers=False, others=" -'"):
                return True, v.title()
            return False, "Only letters, spaces, and - are allowed."
        return False, "Maximum length is 25 characters."

    if field == "date_of_birth":
        right_date, datestring_or_error = general_logic.validate_date_format(v.lower())
        if right_date:
            return True, datestring_or_error
        return False, datestring_or_error

    if field == "gender":
        if v.lower() in ("male", "female", "man", "woman", "m", "f"):
            new_v = "Male" if v.lower() in ("male", "man", "m") else "Female"
            return True, new_v
        return False, "Please enter either Male or Female."
    
    if field == "street_name":
        if len(v) <= 30:
            if general_logic.validate_char_string(v, letters=True, numbers=True, others=" -'().&"):
                return True, v.title()
            return False, "Only letters, numbers, spaces, and - ' . ( ) & are allowed."
        return False, "Maximum length is 30 characters."
    
    if field == "house_number":
        if len(v) <= 10: 
            if general_logic.validate_char_string(v, letters=True, numbers=True, others="-/"):
                return True, v.upper()
            return False, "Only numbers and letters are allowed."
        return False, "Maximum length is 10 characters."

    if field == "zip_code":
        if len(v) == 6:
            if general_logic.validate_char_string(v, letters=True, numbers=True):
                v = v.upper()
                if v[0:4].isdigit() and v[4] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" and v[5] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    return True, v
                return False, "Format must be 1234AB."
            return False, "Only letters and numbers are allowed."
        return False, "Zip code length must be exactly 6 characters."
    
    if field == "city":
        if v.title() in CITIES:
            return True, v.title()
        return False, f"City must be one of the following: {', '.join(CITIES)}."
    
    if field == "email_address":
        if len(v) <= 30:
            if "@" in v and v.count("@") == 1:
                local_part, domain_part = v.split("@")
                if local_part and general_logic.validate_char_string(local_part, letters=True, numbers=True, others="._+-"):
                    if "." in domain_part:
                        domain_parts = domain_part.split(".")
                        valid_domain = True
                        for part in domain_parts:
                            if not part:
                                valid_domain = False
                                break
                            if not general_logic.validate_char_string(part, letters=True, numbers=True, others="-"):
                                valid_domain = False
                                break
                        if valid_domain:
                            top_domain = domain_parts[-1]
                            if general_logic.validate_char_string(top_domain, letters=True, numbers=True):
                                return True, v.lower()
                            return False, "Invalid top-level domain."
                        return False, "Invalid domain format."
                    return False, "Domain must contain at least one dot."
                return False, "Invalid local part (before @)."
            return False, "Email must contain exactly one @ symbol."
        return False, "Maximum length is 30 characters."
    
    if field == "mobile_phone":
        if len(v) == 8:
            if v.isdigit():
                return True, f"+31-6-{v}"
            return False, "Only numbers are allowed."
        return False, "Mobile phone number must be exactly 8 digits."
    
    if field == "driving_license_number":
        if len(v) == 9:
            if general_logic.validate_char_string(v, letters=True, numbers=True):
                if v[0].isalpha() and v[2:9].isdigit():
                    if not get_traveller(identifiers=[], filters={"driving_license_number": v.upper()}):
                        return True, v.upper()
                    return False, "There is already a user with this drivers license. It must be a unique drivers license."
                return False, "Driving license number must be AB1234567 or A12345678 format."
            return False, "Only letters and numbers are allowed."
        return False, "Driving license number must be exactly 9 characters."
    
    return False, "The value entered does not meet the criteria for this field."