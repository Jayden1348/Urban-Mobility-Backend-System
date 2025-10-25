from .general_presentation import *
from Logic import traveller_logic, logs_logic
import copy

change_traveller_fields = ["first_name", "last_name", "date_of_birth", "gender", "street_name", "house_number", "zip_code", "city", "email_address", "mobile_phone", "driving_license_number"]
display_traveller_fields = ["customer_id"] + change_traveller_fields + ["registration_date"]


def search_traveller():  # Done
    display_objects_table(display_traveller_fields, "traveller", selection=False)


def add_traveller(user):    # Done
    new_traveller_dict = get_object_values(
        change_traveller_fields, "traveller")

    if new_traveller_dict:
        if boolean_confirmation("add this traveller", f"You are about to add a new traveller, {new_traveller_dict['first_name']} {new_traveller_dict['last_name']}.\n\n"):
            new_customer_id = traveller_logic.add_traveller(new_traveller_dict)
            if new_customer_id:
                logs_logic.new_log(user.username, "Added traveller",
                                   f"{user.username} added traveller #{new_customer_id}")
                print("\nTraveller added successfully.")
            else:
                logs_logic.new_log(user.username, "Failed addition",
                                   f"{user.username} tried to add a new traveller")
                print("\nFailed to add traveller. Please check the data and try again.")
        else:
            print("Traveller addition cancelled.")
        wait(2)


def update_traveller(user):  # Done
    traveller = display_objects_table(
        display_traveller_fields, "traveller", selection=True)
    if traveller is None:
        return

    old_traveller = copy.deepcopy(traveller)
    changes = get_object_values(change_traveller_fields, "traveller", old_object=traveller)

    if not changes:
        clear_screen()
        print("No changes made. Cancelling...")

    else:
        if boolean_confirmation("update this traveller", f"You are about to update traveller #{old_traveller.customer_id}, {old_traveller.first_name} {old_traveller.last_name}.\n\n"):
            if traveller_logic.update_traveller(old_traveller.customer_id, changes):
                logs_logic.new_log(user.username, "Updated traveller",
                                   f"{user.username} updated traveller #{old_traveller.customer_id}")
                print("\nTraveller updated successfully.")
            else:
                logs_logic.new_log(user.username, "Failed update",
                                   f"{user.username} tried to update traveller #{old_traveller.customer_id}")
                print("\nFailed to update traveller. Please check the data and try again.")
        else:
            print("Traveller update cancelled.")
    wait(2)
    clear_screen()


def delete_traveller(user):  # Done
    traveller_to_delete = display_objects_table(
        display_traveller_fields, "traveller", selection=True)
    if traveller_to_delete is None:
        return

    if boolean_confirmation("delete this traveller", f"You are about to delete traveller #{traveller_to_delete.customer_id}, {traveller_to_delete.first_name} {traveller_to_delete.last_name}.\n\n"):
        if traveller_logic.delete_traveller(traveller_to_delete.customer_id):
            logs_logic.new_log(user.username, "Deleted traveller",
                               f"{user.username} deleted traveller #{traveller_to_delete.customer_id}")
            print(f"\nTraveller {traveller_to_delete.customer_id} deleted successfully.")
        else:
            logs_logic.new_log(user.username, "Failed deletion",
                               f"{user.username} tried to deleted traveller #{traveller_to_delete.customer_id}")
            print("Failed to delete traveller!")
    else:
        print("Traveller deletion cancelled.")
    wait(2)


def advanced_traveller_search():    # Done
    input("Advanced Search\n\nAdvanced Search lets you enter values to search for objects with matching fields.\nFor example, when you searching for all travellers living in Rotterdam, enter 'Rotterdam' for the 'city' field.\n\nPress Enter to continue...")

    empty_traveller = general_logic.get_class("traveller")
    for field in change_traveller_fields:
        setattr(empty_traveller, field, " ")

    advanced_traveller_fields_search = change_traveller_fields.copy()
    advanced_traveller_fields_search.remove("driving_license_number")
    search_filters = get_object_values(
        advanced_traveller_fields_search, "traveller", old_object=empty_traveller)

    if not search_filters:
        return

    if "gender" in search_filters:
        search_filters["gender"] = 1 if search_filters["gender"] == "Female" else 0

    display_objects_table(display_traveller_fields, "traveller",
                          selection=False, only_display=True, filters=search_filters)
