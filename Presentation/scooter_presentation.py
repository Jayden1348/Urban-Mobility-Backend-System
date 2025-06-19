from .generaltools import *  # Import utility functions like clear_screen and wait
from Logic import scooter_logic  # Import scooter logic functions
from datetime import datetime

def search_scooter_info():
    """
    Handles searching for scooter information.
    """
    search_key = input("Enter serial number or model to search: ").strip()  # Get search key
    results = scooter_logic.search_scooter(search_key)  # Call logic to search scooters
    if results:  # If results are found
        print("\nSearch Results:")
        for scooter in results:  # Print each scooter in the results
            print(scooter)
    else:  # If no results are found
        print("\nNo scooters found.")
    wait(2)  # Pause for 2 seconds


def update_scooter_info(user):
    """
    Handles updating scooter information.
    """
    serial_number = input("Enter the serial number of the scooter to update: ").strip()  # Get serial number
    updated_data = {}  # Initialize dictionary for updated data
    print("Enter new values (leave blank to keep current value):")
    updated_data["Brand"] = input("Brand: ").strip() or None  # Get new brand
    updated_data["Model"] = input("Model: ").strip() or None  # Get new model
    updated_data["SerialNumber"] = input("Serial Number: ").strip() or None  # Get new serial number
    updated_data["TopSpeed"] = input("Top Speed (km/h): ").strip() or None  # Get new top speed
    updated_data["BatteryCapacity"] = input("Battery Capacity (Wh): ").strip() or None  # Get new battery capacity
    updated_data["StateOfCharge"] = input("State of Charge (%): ").strip() or None  # Get new state of charge
    updated_data["TargetRangeSoCMin"] = input("Target Range SoC Min (%): ").strip() or None  # Get new min SoC
    updated_data["TargetRangeSoCMax"] = input("Target Range SoC Max (%): ").strip() or None  # Get new max SoC
    updated_data["Latitude"] = input("Latitude: ").strip() or None  # Get new latitude
    updated_data["Longitude"] = input("Longitude: ").strip() or None  # Get new longitude
    updated_data["OutOfService"] = input("Out of Service (0 = No, 1 = Yes): ").strip() or None  # Get new out-of-service status
    updated_data["Mileage"] = input("Mileage (km): ").strip() or None  # Get new mileage
    updated_data["LastMaintenanceDate"] = input("Last Maintenance Date (YYYY-MM-DD): ").strip() or None  # Get new maintenance date
    updated_data["InServiceDate"] = None  # Get new in-service date

    # Remove empty fields
    updated_data = {k: v for k, v in updated_data.items() if v is not None}
    errors = scooter_logic.validate_scooter_data(updated_data, True)  # Validate the updated data
    if errors:  # If there are validation errors
        print("\nValidation errors:")
        for error in errors:  # Print each error
            print(f"- {error}")
        wait(10)  # Pause for 2 seconds
        return  # Exit the function
    # Filter updates based on user role
    filtered_data = scooter_logic.filter_update_data(user.user_role, updated_data)
    if not filtered_data:  # If no fields are allowed to be updated
        print("\nYou do not have permission to update these fields.")
        wait(2)
        return

    # Call update logic
    result = scooter_logic.update_scooter(serial_number, filtered_data)
    if result:  # If update is successful
        print("\nScooter updated successfully.")
    else:  # If update fails
        print("\nFailed to update scooter:")
    wait(2)  # Pause for 2 seconds


def add_scooter(user):
    """
    Handles adding a new scooter.
    """
    if user.user_role == 2:  # Check if user is a Service Engineer
        print("\nYou do not have permission to add scooters.")  # Restrict access
        wait(2)
        return

    # Collect data for the new scooter
    scooter_data = {
        "Brand": input("Brand: ").strip(),
        "Model": input("Model: ").strip(),
        "SerialNumber": input("Serial Number: ").strip(),
        "TopSpeed": float(input("Top Speed (km/h): ").strip()),
        "BatteryCapacity": float(input("Battery Capacity (Wh): ").strip()),
        "StateOfCharge": int(input("State of Charge (%): ").strip()),
        "TargetRangeSoCMin": int(input("Target Range SoC Min (%): ").strip()),
        "TargetRangeSoCMax": int(input("Target Range SoC Max (%): ").strip()),
        "Latitude": float(input("Latitude: ").strip()),
        "Longitude": float(input("Longitude: ").strip()),
        "OutOfService": int(input("Out of Service (0 = No, 1 = Yes): ").strip()),
        "Mileage": float(input("Mileage (km): ").strip()),
        "LastMaintenanceDate": input("Last Maintenance Date (YYYY-MM-DD): ").strip(),
        "InServiceDate": datetime.now().strftime("%Y-%m-%d"),
    }
    result = scooter_logic.add_scooter(scooter_data)  # Call add logic
    if result:  # If addition is successful
        print("\nScooter added successfully.")
    else:  # If addition fails
        print("\nFailed to add scooter:")
        for error in result["errors"]:  # Print each error
            print(f"- {error}")
    wait(2)  # Pause for 2 seconds


def delete_scooter(user):
    """
    Handles deleting a scooter.
    """
    if user.user_role == 2:  # Check if user is a Service Engineer
        print("\nYou do not have permission to delete scooters.")  # Restrict access
        wait(2)
        return

    serial_number = input("Enter the serial number of the scooter to delete: ").strip()  # Get serial number
    if scooter_logic.delete_scooter(serial_number):  # Call delete logic
        print("\nScooter deleted successfully.")
    else:  # If deletion fails
        print("\nFailed to delete scooter.")
    wait(2)  # Pause for 2 seconds