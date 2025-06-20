from .generaltools import *
from Logic import scooter_logic, logs_logic
from datetime import datetime


def search_scooter_info():
    """
    Handles searching for scooter information.
    """
    search_key = input(
        "Enter serial number or model to search: ").strip()  # Get search key
    serial_number = search_scooter_by_serial_number(search_key)
    if serial_number is None:
        print("\nNo scooter found with that serial number.")
        input("Press Enter to continue...")
        return
    results = scooter_logic.search_scooter(serial_number)
    if results:
        print("\nSearch Results:")
        for scooter in results:
            print(scooter)
    else:
        print("\nNo scooters found.")
    input("Press Enter to continue...")


def search_scooter_by_serial_number(serial_number):
    scooter = scooter_logic.search_scooter(serial_number)
    if len(scooter) == 1:  # If scooter is found
        return scooter[0].serial_number  # Return the serial number
    if len(scooter) == 0:
        print("\nNo scooter found with that serial number.")
    if len(scooter) > 1:  # If multiple scooters are found
        print("\nMultiple scooters found with that serial number:")
        interaction = True
        while interaction:
            for s in range(0, len(scooter)):
                print(
                    f"{s+1} - {scooter[s].serial_number} ({scooter[s].model})")

            selected_scooter = input("Select the scooter: ")
            clear_screen()

            if selected_scooter.isdigit() and 1 <= int(selected_scooter) <= len(scooter):
                interaction = False
                return scooter[int(selected_scooter) - 1].serial_number

            if selected_scooter.lower() == "b" or selected_scooter.lower() == "":
                interaction = False
                return None
            # Prompt for valid selection
            print("\nInvalid selection. Please try again.")


def update_scooter_info(user):
    """
    Handles updating scooter information based on user role, with validation.
    """
    serial_number = input(
        "Enter the serial number of the scooter to update: ").strip()
    serial_number = search_scooter_by_serial_number(serial_number)
    if serial_number is None:
        print("\nNo scooter found with that serial number.")
        input("Press any key to continue...")
        return

    allowed_fields = scooter_logic.filter_update_data(
        user.user_role, {k: None for k in scooter_logic.field_types.keys()}).keys()
    if user.user_role in (0, 1):  # Super Admin or System Admin can update all fields
        allowed_fields = scooter_logic.field_types.keys()
    allowed_fields = list(allowed_fields)

    # remove so that the inservicedate cannot be updated
    if "InServiceDate" in allowed_fields:
        allowed_fields.remove("InServiceDate")

    print("Enter new values (leave blank to keep current value):")
    updated_data = {}
    db_values = scooter_logic.get_scooter_by_serial_number(
        serial_number)  # Fetch current values from the database

    for field in allowed_fields:
        while True:
            value = input(f"{field}: ").strip()
            if value == "":
                break  # Skip updating this field

            extra_value = None
            if field == "TargetRangeSoCMin":
                extra_value = updated_data.get("TargetRangeSoCMax")
            elif field == "TargetRangeSoCMax":
                extra_value = updated_data.get("TargetRangeSoCMin")

            converted_value, error = scooter_logic.validate_field_value(
                field, value, extra_value)
            if error:
                print(f"Error: {error}")
            else:
                updated_data[field] = converted_value
                break

    if "TargetRangeSoCMin" in updated_data or "TargetRangeSoCMax" in updated_data:
        min_value = updated_data.get(
            "TargetRangeSoCMin", db_values.target_range_soc_min)
        max_value = updated_data.get(
            "TargetRangeSoCMax", db_values.target_range_soc_max)
        if min_value is not None and max_value is not None and min_value > max_value:
            print("Error: TargetRangeSoCMin cannot be greater than TargetRangeSoCMax.")
            input("Press any key to continue...")
            return

    if not updated_data:
        print("\nNo updates provided.")
        input("Press any key to continue...")
        return

    filtered_data = scooter_logic.filter_update_data(
        user.user_role, updated_data)
    if not filtered_data:
        print("\nYou do not have permission to update these fields.")
        input("Press any key to continue...")
        return

    result = scooter_logic.update_scooter(serial_number, filtered_data)
    if result:
        print("\nScooter updated successfully.")
        logs_logic.new_log(user.username, "Updated scooter info", None, 0)
    else:
        print("\nFailed to update scooter.")
    input("Press any key to continue...")


def add_scooter(user):
    """
    Handles adding a new scooter.
    """
    if user.user_role == 2:
        print("\nYou do not have permission to add scooters.")
        wait(2)
        return

    print("Enter the details for the new scooter:")
    scooter_data = {}
    required_fields = [
        "Brand", "Model", "SerialNumber", "TopSpeed", "BatteryCapacity",
        "StateOfCharge", "TargetRangeSoCMin", "TargetRangeSoCMax",
        "Latitude", "Longitude", "OutOfService", "Mileage", "LastMaintenanceDate"
    ]
    # Collect data for the new scooter
    for field in required_fields:
        if field == "InServiceDate":  # Automatically set the in-service date
            scooter_data[field] = datetime.now().strftime("%Y-%m-%d")
            continue

        while True:
            value = input(f"{field}: ").strip()
            if value == "":
                print(f"{field} is required. Please provide a value.")
                continue

            # Validate the field value
            converted_value, error = scooter_logic.validate_field_value(
                field, value)
            if error:
                print(f"Error: {error}")
            else:
                scooter_data[field] = converted_value
                break

    min_value = scooter_data.get("TargetRangeSoCMin")
    max_value = scooter_data.get("TargetRangeSoCMax")
    if min_value is not None and max_value is not None and min_value > max_value:
        print("Error: TargetRangeSoCMin cannot be greater than TargetRangeSoCMax.")
        input("Press Enter to continue...")
        return

    # Add the scooter to the database
    scooter_data["InServiceDate"] = datetime.now().strftime("%Y-%m-%d")
    result = scooter_logic.add_scooter(scooter_data)
    if result:
        print("\nScooter added successfully.")
        logs_logic.new_log(user.username, "Added scooter",
                           f"{user.username} added scooter with serial number: {scooter_data['SerialNumber']}", 0)
    else:
        print("\nFailed to add scooter. Please check the data and try again.")
    input("Press Enter to continue...")


def delete_scooter(user):
    """
    Handles deleting a scooter.
    """
    if user.user_role == 2:
        print("\nYou do not have permission to delete scooters.")
        wait(2)
        return

    serial_number = input(
        "Enter the serial number of the scooter to delete: ").strip()
    serial_number = search_scooter_by_serial_number(serial_number)
    if serial_number is None:
        print("\nNo scooter found with that serial number.")
        input("Press Enter to continue...")
        return
    confirmation = input(
        f"Are you sure you want to delete the scooter with serial number: {serial_number}? (y/n): ").strip().lower()  # Confirm deletion
    if confirmation != 'y':
        print("\nDeletion cancelled.")
        input("Press Enter to continue...")
        return
    if scooter_logic.delete_scooter(serial_number):
        logs_logic.new_log(user.username, "Deleted scooter",
                           f"{user.username} deleted scooter with serial number: {serial_number}", 0)
        print("\nScooter deleted successfully.")
    else:
        print("\nFailed to delete scooter.")
    input("Press Enter to continue...")
