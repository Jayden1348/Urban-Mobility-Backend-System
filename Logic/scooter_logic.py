from Access import DataAccess


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
        if search_key.lower() in scooter.serial_number.lower() or search_key.lower() in scooter.model.lower()
    ]

def filter_update_data(user_role, updated_data):
    """
    Filters the update data based on the user's role.
    """
    allowed_fields = {
        0: None,  # Super Admin can update all fields
        1: None,  # System Admin can update all fields
        2: [  # Service Engineer can only update these fields
            "StateOfCharge", "TargetRangeSoCMin", "TargetRangeSoCMax",
            "Latitude", "Longitude", "OutOfService", "Mileage", "LastMaintenanceDate"
        ]
    }

    if allowed_fields[user_role] is None:
        return updated_data  # No restrictions for Super Admin and System Admin

    return {key: value for key, value in updated_data.items() if key in allowed_fields[user_role]}

def validate_scooter_data(scooter_data, isUpdate=False):
    
    # Validates scooter data before adding or updating.
    
    errors = []
    if isUpdate:
        if not (10 <= len(scooter_data.get("SerialNumber", "")) <= 17) or scooter_data.get("SerialNumber") is None:
            errors.append("Serial number must be between 10 and 17 alphanumeric characters.")
        if not scooter_data.get("SerialNumber", "").isalnum() or scooter_data.get("SerialNumber") is None:
            errors.append("Serial number can only contain alphanumeric characters.")

        if not (0 <= scooter_data.get("StateOfCharge", 0) <= 100) or scooter_data.get("StateOfCharge") is None:
            errors.append("State of Charge (SoC) must be between 0 and 100.")

        if not (0 <= scooter_data.get("TargetRangeSoCMin", 0) <= 100) or scooter_data.get("TargetRangeSoCMin") is None:
            errors.append("Target Range SoC Min must be between 0 and 100.")

        if not (0 <= scooter_data.get("TargetRangeSoCMax", 0) <= 100) or scooter_data.get("TargetRangeSoCMax") is None:
            errors.append("Target Range SoC Max must be between 0 and 100.")

        if not (51.85 <= scooter_data.get("Latitude", 52) <= 52.05) or scooter_data.get("Latitude") is None:
            errors.append("Latitude must be within the Rotterdam region (51.85 to 52.05).")

        if not (4.35 <= scooter_data.get("Longitude", 4.4) <= 4.65) or scooter_data.get("Longitude") is None:
            errors.append("Longitude must be within the Rotterdam region (4.35 to 4.65).")

        if scooter_data.get("OutOfService") not in (0, 1) or scooter_data.get("OutOfService") is None:
            errors.append("Out of Service must be 0 (No) or 1 (Yes).")
    
    else:
        if not (10 <= len(scooter_data.get("SerialNumber", "")) <= 17):
            errors.append("Serial number must be between 10 and 17 alphanumeric characters.")
        if not scooter_data.get("SerialNumber", "").isalnum():
            errors.append("Serial number can only contain alphanumeric characters.")

        if not (0 <= scooter_data.get("StateOfCharge", 0) <= 100):
            errors.append("State of Charge (SoC) must be between 0 and 100.")

        if not (0 <= scooter_data.get("TargetRangeSoCMin", 0) <= 100):
            errors.append("Target Range SoC Min must be between 0 and 100.")

        if not (0 <= scooter_data.get("TargetRangeSoCMax", 0) <= 100):
            errors.append("Target Range SoC Max must be between 0 and 100.")

        if not (51.85 <= scooter_data.get("Latitude", 52) <= 52.05):
            errors.append("Latitude must be within the Rotterdam region (51.85 to 52.05).")

        if not (4.35 <= scooter_data.get("Longitude", 4.4) <= 4.65):
            errors.append("Longitude must be within the Rotterdam region (4.35 to 4.65).")

        if scooter_data.get("OutOfService") not in (0, 1):
            errors.append("Out of Service must be 0 (No) or 1 (Yes).")

    return errors