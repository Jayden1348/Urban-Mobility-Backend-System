from Access import DataAccess
import datetime

field_types = {
    "TopSpeed": float,
    "BatteryCapacity": float,
    "StateOfCharge": "percentage",
    "TargetRangeSoCMin": "percentage",
    "TargetRangeSoCMax": "percentage",
    "Latitude": float,
    "Longitude": float,
    "OutOfService": int,
    "Mileage": float,
    "LastMaintenanceDate": "date",
    "InServiceDate": "date",
    "SerialNumber": "serial"
}

def add_scooter(scooter_data):
    return DataAccess.insert_item_into_table("Scooters", scooter_data)


def update_scooter(serial_number, updated_data):
    return DataAccess.update_item_from_table("Scooters", serial_number, updated_data)


def delete_scooter(serial_number):
    return DataAccess.delete_item_from_table("Scooters", serial_number)


def search_scooter(search_key):
    # searches scooter by checking if the serial number or model contains the search key
    scooters = DataAccess.get_all_from_table("Scooters")
    return [
        scooter for scooter in scooters
        if search_key.lower() in scooter.serial_number.lower() or search_key.lower() in (scooter.model).lower()
    ]

def filter_update_data(user_role, updated_data):
    """
    Filters the update data based on the user's role.
    """
    allowed_fields = {
        0: [  # Super Admin can update all fields
            "Brand", "Model", "SerialNumber", "TopSpeed", "BatteryCapacity",
            "StateOfCharge", "TargetRangeSoCMin", "TargetRangeSoCMax",
            "Latitude", "Longitude", "OutOfService", "Mileage",
            "LastMaintenanceDate"
        ],  
        1: [  # System Admin can update all fields
            "Brand", "Model", "SerialNumber", "TopSpeed", "BatteryCapacity",
            "StateOfCharge", "TargetRangeSoCMin", "TargetRangeSoCMax",
            "Latitude", "Longitude", "OutOfService", "Mileage",
            "LastMaintenanceDate"
        ],  
        2: [  # Service Engineer can only update these fields
            "StateOfCharge", "TargetRangeSoCMin", "TargetRangeSoCMax",
            "Latitude", "Longitude", "OutOfService", "Mileage", "LastMaintenanceDate"
        ]
    }

    if allowed_fields[user_role] is None:
        return updated_data  # No restrictions for Super Admin and System Admin

    return {key: value for key, value in updated_data.items() if key in allowed_fields[user_role]}


def validate_field_value(field, value, extra_value = None):
    
    # validates the value of a field based on its type and constraints
   
    if value == "":
        return None, None  # Allow skipping

    expected_type = field_types.get(field)

    if expected_type == int and field == "OutOfService":
        if value.isdigit():
            if int(value) in (0, 1):
                return int(value), None
            return None, "Out of Service must be 0 (No) or 1 (Yes)."
        return None, f"{field} must be a whole number."

    elif expected_type == float:
        try:
            float_val = float(value)
            # Latitude validation
            if field == "Latitude" and not (51.85 <= float_val <= 52.05):
                return None, "Latitude must be within the Rotterdam region (51.85 to 52.05)."
            # Longitude validation
            if field == "Longitude" and not (4.35 <= float_val <= 4.65):
                return None, "Longitude must be within the Rotterdam region (4.35 to 4.65)."
            return float_val, None
        except ValueError:
            return None, f"{field} must be a number."

    elif expected_type == "date":
        try:
            datetime.datetime.strptime(value, "%Y-%m-%d")
            return value, None
        except ValueError:
            return None, f"{field} must be in YYYY-MM-DD format."

    elif expected_type == "serial":
        if not (10 <= len(value) <= 17):
            return None, "Serial number must be between 10 and 17 characters."
        if not value.isalnum():
            return None, "Serial number must be alphanumeric."
        return value, None
    elif expected_type == "percentage":
        if value.isdigit():
            num = int(value)
            if 0 <= num <= 100:
                if extra_value is not None:
                    if field == "TargetRangeSoCMin" and num > extra_value:
                        return None, "Target Range SoC Min cannot be greater than Target Range SoC Max."
                    elif field == "TargetRangeSoCMax" and num < extra_value:
                        return None, "Target Range SoC Max cannot be less than Target Range SoC Min."
                return num, None

            else:
                return None, f"{field} must be between 0 and 100."
            
        else:
            return None, f"{field} must be a whole number."


    return value, None

def get_scooter_by_serial_number(serial_number):
    """
    Retrieves the current values of a scooter by its serial number.
    """
    scooter = DataAccess.find_item_in_table("Scooters", serial_number)
    if scooter:
        return scooter
    return {}