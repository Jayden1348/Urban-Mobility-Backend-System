from .generaltools import *
from Logic import traveller_logic
from datetime import datetime
CITIES = [
        "Rotterdam", "Amsterdam", "Utrecht", "Eindhoven", "Groningen",
        "Maastricht", "Delft", "Leiden", "Nijmegen", "Haarlem"
    ]

def search_traveller_info():
    """
    Handles searching for traveller information.
    """
    search_key = input("Enter customerID, first name, or last name to search: ").strip()
    customer_ID = find_traveller_by_key(search_key)  # Find traveller by key
    if customer_ID is None:  # If no traveller found
        print("\nNo traveller found with that search key.")
        input("Press Enter to continue...")
        return
    results = traveller_logic.search_traveller(customer_ID)
    if results:
        print("\nSearch Results:")
        for traveller in results:
            print(traveller)
    else:
        print("\nNo travellers found.")
    input("Press Enter to continue...")

def find_traveller_by_key(search_key):
    """
    Finds a traveller by searching in FirstName, LastName, or CustomerID.
    """
    travellers = traveller_logic.search_traveller(search_key)

    if len(travellers) == 1:  # If exactly one traveller is found
        return travellers[0].customerID  # Return the CustomerID

    if len(travellers) == 0:  # If no travellers are found
        print("\nNo traveller found with that search key.")
        return None

    if len(travellers) > 1:  # If multiple travellers are found
        print("\nMultiple travellers found with that search key:")
        interaction = True
        while interaction:
            for i, traveller in enumerate(travellers, start=1):
                print(f"{i} - {traveller.customerID} ({traveller.first_name} {traveller.last_name})")

            selected_traveller = input("Select the traveller (or press 'b' to go back): ").strip()

            if selected_traveller.isdigit() and 1 <= int(selected_traveller) <= len(travellers):
                interaction = False
                return travellers[int(selected_traveller) - 1].customerID

            if selected_traveller.lower() == "b" or selected_traveller == "":
                interaction = False
                return None

            print("\nInvalid selection. Please try again.")  # Prompt for valid selection

def add_traveller():
    """
    Handles adding a new traveller.
    """
    print("Enter the details for the new traveller:")
    traveller_data = {}
    required_fields = [
        "FirstName", "LastName", "DateOfBirth", "Gender", "StreetName",
        "HouseNumber", "ZipCode", "City", "EmailAddress", "MobilePhone", "DrivingLicenseNumber"
    ]

    for field in required_fields:
        while True:
            if field == "City":
                print("Please choose a city from the following list:")
                for city in range(1, len(CITIES)+1):
                    print(f"{city} - {CITIES[city-1]}")
                while True:
                    try:
                        choice = int(input("Enter the number corresponding to your choice: ").strip())
                        if 1 <= choice <= len(CITIES):
                            
                            value = CITIES[choice-1]
                            break
                        else:
                            print("Invalid choice. Please select a valid number from the list.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
            else:
                if field == "MobilePhone":
                    print("+31-6-")
                value = input(f"{field}: ").strip()
                if value == "":
                    print(f"{field} is required. Please provide a value.")
                    continue

                # Validate the field value
            converted_value, error = traveller_logic.validate_field_value(field, value)
            if error:
                print(f"Error: {error}")
            else:
                traveller_data[field] = converted_value
                break

    result = traveller_logic.add_traveller(traveller_data)
    if result:
        print("\nTraveller added successfully.")
    else:
        print("\nFailed to add traveller. Please check the data and try again.")
    input("Press Enter to continue...")


def update_traveller_info():
    """
    Handles updating traveller information.
    """
    search_key = input("Enter the name or CustomerID of the traveller to update: ").strip()
    results = find_traveller_by_key(search_key)
    if not results:
        print("\nNo traveller found with that CustomerID or name.")
        input("Press Enter to continue...")
        return

    print("Enter new values (leave blank to keep current value):")
    updated_data = {}
    for field in traveller_logic.field_types.keys():
        while True:
            if field == "City":
                print("Please choose a city from the following list:")
                for city in range(1, len(CITIES)+ 1):
                    print(f"{city} - {CITIES[city -1]}")
                try:
                    choice = input("Enter the number corresponding to your choice (or leave blank to skip): ").strip()
                    if choice == "":
                        break  # Skip updating this field
                    if not choice.isdigit():
                        print("Invalid input. Please enter a number.")
                        continue
                    choice = int(choice)
                    if 1 <= choice <= len(CITIES):
                        value = CITIES[choice-1]
                        updated_data[field] = value
                        break  # Exit the loop after a valid choice
                    else:
                        print("Invalid choice. Please select a valid number from the list.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            else:
                value = input(f"{field}: ").strip()
                if value == "":
                    break  # Skip updating this field

                # Validate the field value
                converted_value, error = traveller_logic.validate_field_value(field, value)
                if error:
                    print(f"Error: {error}")
                else:
                    updated_data[field] = converted_value
                    break  # Exit the loop if the value is valid

    if not updated_data:
        print("\nNo updates provided.")
        input("Press Enter to continue...")
        return

    result = traveller_logic.update_traveller(results, updated_data)
    if result:
        print("\nTraveller updated successfully.")
    else:
        print("\nFailed to update traveller.")
    input("Press Enter to continue...")

def delete_traveller():
    """
    Handles deleting a traveller.
    """
    search = input("Enter the name or the customerID of the traveller to delete: ").strip()
    
    search = find_traveller_by_key(search)
    if search is None:  # If no traveller found
        print("\nNo traveller found with that CustomerID or name.")
        input("Press Enter to continue...")
        return
    
    confirmation = input(f"Are you sure you want to delete the traveller: {search[0]}? (y/n): ").strip().lower()
    if confirmation != 'y':
        print("\nDeletion cancelled.")
        input("Press Enter to continue...")
        return

    result = traveller_logic.delete_traveller(search[0].customerID)
    if result:
        print("\nTraveller deleted successfully.")
    else:
        print("\nFailed to delete traveller.")
    input("Press Enter to continue...")