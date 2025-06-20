from Access import DataAccess
import datetime
from Logic.encryption import encrypt_data, decrypt_data

field_types = {
    "FirstName": str,
    "LastName": str,
    "DateOfBirth": "date",
    "Gender": str,
    "StreetName": str,
    "HouseNumber": str,
    "ZipCode": str,
    "City": str,
    "EmailAddress": str,
    "MobilePhone": str,
    "DrivingLicenseNumber": str,
}

def add_traveller(traveller_data):
    for field in ["FirstName", "LastName", "EmailAddress", "MobilePhone", "StreetName"]:
        traveller_data[field] = encrypt_data(traveller_data[field])
    traveller_data["RegistrationDate"] = datetime.datetime.now().strftime("%Y-%m-%d")
    return DataAccess.add_item_to_table("Travellers", traveller_data)

def update_traveller(customerID, updated_data):
    return DataAccess.update_item_from_table("Travellers", customerID, updated_data)

def delete_traveller(customerID):
    return DataAccess.remove_item_from_table("Travellers", customerID)


def search_traveller(search_key):
    """
    Searches for a traveller by CustomerID, FirstName, or LastName.
    """
    travellers = DataAccess.get_all_from_table("Travellers")
    search_key = str(search_key).lower()

    decrypted_travellers = []
    for traveller in travellers:
        # Decrypt sensitive fields
        traveller.first_name = decrypt_data(traveller.first_name)
        traveller.last_name = decrypt_data(traveller.last_name)
        decrypted_travellers.append(traveller)


    # Perform the search
    return [
        traveller for traveller in decrypted_travellers
        if search_key in str(traveller.customerID).lower() or
           search_key in traveller.first_name.lower() or
           search_key in traveller.last_name.lower()
    ]

def validate_field_value(field, value):
    if value == "":
        return None, f"{field} is required."

    expected_type = field_types.get(field)

    if expected_type == "date":
        try:
            datetime.datetime.strptime(value, "%Y-%m-%d")
            return value, None
        except ValueError:
            return None, f"{field} must be in YYYY-MM-DD format."

    if field == "Gender" and value.lower() not in ["male", "female"]:
        return None, "Gender must be 'male' or 'female'."

    if field == "MobilePhone":
    # Ensure the value is exactly 8 digits
        if not value.isdigit() or len(value) != 8:
            return None, "Mobile phone must contain exactly 8 digits (DDDDDDDD)."
        return f"+31-6-{value}", None  # Format the phone number as +31-6-DDDDDDDD

    if field == "DrivingLicenseNumber":
    # Validate format XXDDDDDDD or XDDDDDDDD
        if len(value) == 9 and value[:2].isalpha() and value[2:].isdigit():
            return value, None
        elif len(value) == 9 and value[:1].isalpha() and value[1:].isdigit():
            return value, None
        else:
            return None, "Driving license number must be in the format XXDDDDDDD or XDDDDDDDD."
    if field == "ZipCode":
        # Validate format DDDDXX
        if len(value) == 6 and value[:4].isdigit() and value[4:].isalpha() and value[4:].isupper():
            return value, None
        else:
            return None, "Zip code must be in the format DDDDXX (e.g., 1234AB)."
    return value, None