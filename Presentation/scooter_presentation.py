from .general_presentation import *
from Logic import scooter_logic, logs_logic, account_logic
import copy

unit_map = {
    "top_speed": " km/h",
    "battery_capacity": " Wh",
    "state_of_charge": " %",
    "mileage": " km",
    "target_range_soc": " %"
}

change_scooter_fields = ["brand", "model", "serial_number", "top_speed", "battery_capacity", "state_of_charge", "target_range_soc", "latitude", "longitude","out_of_service", "mileage", "last_maintenance_date"]
display_scooter_fields = ["scooter_id"] + change_scooter_fields + ["in_service_date"]


def search_scooter():
    display_objects_table(
        display_scooter_fields, "scooter", selection=False, unit_map=unit_map)


def add_scooter(user):
    new_scooter_dict = get_object_values(
        change_scooter_fields, "scooter", unit_map=unit_map)

    if new_scooter_dict:
        if boolean_confirmation("add this scooter", f"You are about to add a new scooter, {new_scooter_dict['brand']} {new_scooter_dict['model']}.\n\n"):
            new_scooter_id = scooter_logic.add_scooter(new_scooter_dict)
            if new_scooter_id:
                logs_logic.new_log(user.username, "Added scooter",
                                   f"{user.username} added scooter #{new_scooter_id}")
                print("\nScooter added successfully.")
            else:
                logs_logic.new_log(user.username, "Failed addition",
                                   f"{user.username} tried to add a new scooter")
                print("\nFailed to add scooter. Please check the data and try again.")
        else:
            print("Scooter addition cancelled.")
        wait(2)


def update_scooter(user):
    scooter = display_objects_table(
        display_scooter_fields, "scooter", selection=True, unit_map=unit_map)
    if scooter is None:
        return

    old_scooter = copy.deepcopy(scooter)
    if account_logic.get_role_num(user.user_role) == 2:
        restricted_fields = ["brand", "model",
                             "serial_number", "top_speed", "battery_capacity"]
    else:
        restricted_fields = []
    changes = get_object_values(change_scooter_fields, "scooter", old_object=scooter,
                                unit_map=unit_map, restricted_fields=restricted_fields)

    if not changes:
        clear_screen()
        print("No changes made. Cancelling...")

    else:
        if boolean_confirmation("update this scooter", f"You are about to update scooter #{old_scooter.scooter_id}, {old_scooter.brand} {old_scooter.model}.\n\n"):
            if scooter_logic.update_scooter(old_scooter.scooter_id, changes):
                logs_logic.new_log(user.username, "Updated scooter",
                                   f"{user.username} updated scooter #{old_scooter.scooter_id}")
                print("\nScooter updated successfully.")
            else:
                logs_logic.new_log(user.username, "Failed update",
                                   f"{user.username} tried to update scooter #{old_scooter.scooter_id}")
                print("\nFailed to update scooter. Please check the data and try again.")
        else:
            print("Scooter update cancelled.")
    wait(2)
    clear_screen()


def delete_scooter(user):
    scooter_to_delete = display_objects_table(
        display_scooter_fields, "scooter", selection=True, unit_map=unit_map)
    if scooter_to_delete is None:
        return

    if boolean_confirmation("delete this scooter", f"You are about to delete scooter #{scooter_to_delete.scooter_id}\n\n"):
        if scooter_logic.delete_scooter(scooter_to_delete.scooter_id):
            logs_logic.new_log(user.username, "Deleted scooter",
                               f"{user.username} deleted scooter #{scooter_to_delete.scooter_id}")
            print(f"\nScooter #{scooter_to_delete.scooter_id} deleted successfully.")
        else:
            logs_logic.new_log(user.username, "Failed deletion",
                               f"{user.username} tried to deleted scooter #{scooter_to_delete.scooter_id}")
            print("Failed to delete scooter!")
    else:
        print("Scooter deletion cancelled.")
    wait(2)


def advanced_scooter_search():
    input("Advanced Search\n\nAdvanced Search lets you enter values to search for objects with matching fields.\nFor example, when you searching for all scooters that are out of service, enter 'Yes' for the 'out of service' field.\n\nPress Enter to continue...")

    empty_scooter = general_logic.get_class("scooter")
    for field in change_scooter_fields:
        setattr(empty_scooter, field, " ")

    advanced_scooter_fields_search = change_scooter_fields.copy()
    advanced_scooter_fields_search.remove("serial_number")
    search_filters = get_object_values(
        advanced_scooter_fields_search, "scooter", old_object=empty_scooter, unit_map=unit_map)
    
    if not search_filters:
        return

    if "out_of_service" in search_filters:
        search_filters["out_of_service"] = 1 if search_filters["out_of_service"] == "Yes" else 0
    if "target_range_soc" in search_filters:
        search_filters["target_range_soc_min"] = search_filters["target_range_soc"].split(
            "-")[0].strip()
        search_filters["target_range_soc_max"] = search_filters["target_range_soc"].split(
            "-")[1].strip()
        search_filters.pop("target_range_soc")

    display_objects_table(display_scooter_fields + ["in_service_date"], "scooter",
                          selection=False, only_display=True, filters=search_filters, unit_map=unit_map)
