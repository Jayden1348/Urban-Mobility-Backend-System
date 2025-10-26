from Access import DataAccess
from Logic import general_logic
import random
import string
from Utils.encryption import encryptor

LONGITUDE_MAX = 4.65
LONGITUDE_MIN = 4.30
LATITUDE_MAX = 52.05
LATITUDE_MIN = 51.85
CITY_AREA = "Rotterdam"



def get_scooter(search_key="", identifiers=None, filters=None):
    if identifiers is None:
        identifiers = ["scooter_id", "serial_number", "brand", "model"]
    return DataAccess.search_item_in_table(
        "Scooters", search_key, identifiers=identifiers, filters=filters)


def add_scooter(new_scooter_data):
    if "out_of_service" in new_scooter_data:
        new_scooter_data["out_of_service"] = 1 if new_scooter_data["out_of_service"] == "Yes" else 0
    if "target_range_soc" in new_scooter_data:
        new_scooter_data["target_range_soc_min"] = new_scooter_data["target_range_soc"].split(
            "-")[0].strip()
        new_scooter_data["target_range_soc_max"] = new_scooter_data["target_range_soc"].split(
            "-")[1].strip()
        new_scooter_data.pop("target_range_soc")
    new_scooter_data["in_service_date"] = general_logic.get_today_date()

    return DataAccess.add_item_to_table("Scooters", encryptor.encrypt_object_data("Scooters", new_scooter_data))


def update_scooter(scooter_id, updated_scooter_data):
    if "out_of_service" in updated_scooter_data:
        updated_scooter_data["out_of_service"] = 1 if updated_scooter_data["out_of_service"] == "Yes" else 0
    if "target_range_soc" in updated_scooter_data:
        updated_scooter_data["target_range_soc_min"] = updated_scooter_data["target_range_soc"].split(
            "-")[0].strip()
        updated_scooter_data["target_range_soc_max"] = updated_scooter_data["target_range_soc"].split(
            "-")[1].strip()
        updated_scooter_data.pop("target_range_soc")

    return DataAccess.update_item_from_table("Scooters", scooter_id, encryptor.encrypt_object_data("Scooters", updated_scooter_data))


def delete_scooter(scooter_id):
    return DataAccess.remove_item_from_table("Scooters", scooter_id)


# Validation for new scooter values
def validate_new_scooter_values(field, v):
    if field in ["brand", "model"]:
        if len(v) <= 20:
            if general_logic.validate_char_string(v, letters=True, numbers=True, others=" -+.&"):
                return True, v.title()
            return False, "Only letters, numbers, spaces, and - + & . are allowed."
        return False, "Maximum length is 20 characters."

    if field == "serial_number":
        if v.lower() in ("r", "random"):
            return True, generate_random_serial_number()
        if 10 <= len(v) <= 17:
            if v.isalnum():
                if not get_scooter(identifiers=[], filters={"serial_number": v}):
                    return True, v
                return False, "The serial number already exists in the system."
            return False, "Serial number can only contains letters and numbers."
        return False, "Serial number length must be 10 - 17 characters."

    if field == "top_speed":
        if v.replace(".", "", 1).isdigit() and 0 < round(float(v)) <= 80:
            return True, round(float(v))
        return False, "Top speed must be a positive number up to 80 km/h."

    if field == "battery_capacity":
        if v.replace(".", "", 1).isdigit() and 0 < round(float(v), 1):
            return True, f"{float(v):.1f}"
        return False, "Battery capacity must be a positive number."

    if field == "state_of_charge":
        if v.isdigit() and 0 <= int(v) <= 100:
            return True, int(v)
        return False, "State of charge must be a number between 0 and 100 %."

    if field == "target_range_soc":
        if v.count('-') == 1:
            parts = v.split('-')
            if all(part.strip().isdigit() for part in parts):
                min_val = int(parts[0].strip())
                max_val = int(parts[1].strip())
                if 0 <= min_val <= 100 and 0 <= max_val <= 100:
                    if min_val < max_val:
                        return True, f"{min_val} - {max_val}"
                    return False, "The minimum value must be less than the maximum value."
            return False, "Both values must be numbers between 0 and 100 %."
        return False, "Please enter two numbers separated by a dash (for example: 20-80)."

    if field == "latitude":
        if v.replace(".", "", 1).isdigit() and LATITUDE_MIN <= float(v) <= LATITUDE_MAX:
            return True, f"{float(v):.5f}"
        return False, f"Latitude must be a number between {LATITUDE_MIN} and {LATITUDE_MAX} to be in {CITY_AREA}."

    if field == "longitude":
        if v.replace(".", "", 1).isdigit() and LONGITUDE_MIN <= float(v) <= LONGITUDE_MAX:
            return True, f"{float(v):.5f}"
        return False, f"Longitude must be a number between {LONGITUDE_MIN} and {LONGITUDE_MAX} to be in {CITY_AREA}."

    if field == "out_of_service":
        if v.lower() in ("0", "1", "yes", "no", "y", "n"):
            new_v = "Yes" if v.lower() in ("1", "yes", "y") else "No"
            return True, new_v
        return False, "Please enter either Yes or No."

    if field == "mileage":
        if v.replace(".", "", 1).isdigit() and 0 <= float(v):
            return True, round(float(v), 1)
        return False, " Mileage must be a positive number."

    if field == "last_maintenance_date":
        right_date, datestring_or_error = general_logic.validate_date_format(v.lower())
        if right_date:
            return True, datestring_or_error
        return False, datestring_or_error

    return False, "The value entered does not meet the criteria for this field."

# Random generation
def generate_random_serial_number():
    while True:
        new_serial_number = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(10, 17)))
        if not get_scooter(identifiers=[], filters={"serial_number": new_serial_number}):
            return new_serial_number
