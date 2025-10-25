import pandas as pd
import os
import time
from Logic import general_logic


def clear_screen():
    os.system('cls')
    print("\n")


def wait(waittime):
    time.sleep(waittime)


def boolean_confirmation(message, added_info="", clean_screen=True):
    while True:
        if clean_screen:
            clear_screen()
        choice = input(
            f"{added_info}Are you sure you want to {message}? (y/n): ").strip().lower()
        if choice in ("y", "yes", "1"):
            clear_screen()
            return True
        elif choice in ("n", "no", "0"):
            clear_screen()
            return False
        else:
            print("\nPlease enter 'y' or 'n'.")
            wait(2)


def boolean_confirmation_custom(message, clean_screen=True):
    while True:
        if clean_screen:
            clear_screen()
        choice = input(
            f"{message}? (y/n): ").strip().lower()
        if choice in ("y", "yes", "1"):
            clear_screen()
            return True
        elif choice in ("n", "no", "0"):
            clear_screen()
            return False
        else:
            print("\nPlease enter 'y' or 'n'.")
            wait(2)


def boolean_response(message):
    choice = input(message).strip().lower()
    if choice in ("y", "yes", "1"):
        return True
    elif choice in ("n", "no", "0"):
        return False
    else:
        print("\nPlease enter 'y' or 'n'.")
        wait(2)


## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##


def display_objects_table(columns, type, selection, only_display=False, filters=None, unit_map={}):

    get_objects_func = getattr(general_logic.get_logic_files(type),
                               f"get_{type.replace(' ', '_')}")

    if only_display:
        objects = get_objects_func(filters=filters)
        if not objects:
            print(f"No {type}s found!")
            wait(2)
            clear_screen()
            return
    else:
        while True:
            clear_screen()
            search_key = input(
                f"Enter a keyword to search for {type}s, or press Enter to cancel: ")
            if not search_key:
                clear_screen()
                return
            objects = get_objects_func(search_key.strip(), filters=filters)
            if not objects:
                print(f"\nNo {type} found with: '{search_key}'")
                wait(2)
            else:
                break

    rows = []
    new_columns = ["id"] + columns
    for idx, obj in enumerate(objects, start=1):
        row = {"id": idx}
        for col in columns:
            value = getattr(obj, col, None)
            row[col] = value if value is not None else ""
        rows.append(row)
    columns = new_columns

    df = pd.DataFrame(rows)
    col_widths = {}
    for col in columns:
        max_len = max([len(str(val) + unit_map.get(col, "")) if val is not None else 0 for val in df[col]]
                      + [len(col.replace('_', ' ').capitalize())])
        col_widths[col] = max_len + 2

    fmt_parts = [f"{{:<{col_widths['id']}}}"]
    fmt_parts.extend([f"{{:<{col_widths[col]}}}" for col in columns[1:]])
    fmt = "┃ {} ┃ {} ┃".format(fmt_parts[0], " | ".join(fmt_parts[1:]))
    
    header_row = fmt.format("Id", *[col.replace('_', ' ').capitalize() for col in columns[1:]])
    total_width = len(header_row)

    while True:
        clear_screen()
        print(f"{type.capitalize()} search results:\n")
        print("━" * total_width)
        print(header_row)
        print("━" * total_width)
        for _, row in df.iterrows():
            values = []
            for col in columns:
                val = row[col]
                if pd.isna(val) or val is None or val == "":
                    values.append("")
                else:
                    values.append(str(val) + unit_map.get(col, ""))
            print(fmt.format(*values))
        print("━" * total_width)
        print("\n")

        if not selection:
            input("Press Enter to continue...")
            clear_screen()
            return

        if len(objects) == 1:
            choice = boolean_response(
                f"Only one {type} found. Do you want to select this {type}? (y/n): ")
            if choice is None:
                continue
            elif choice:
                return objects[0]
            else:
                clear_screen()
                return

        select_id = input(
            f"Enter id to select a {type} (or press Enter to quit): ").strip()
        if not select_id:
            clear_screen()
            return
        if not general_logic.check_is_digit_valid(select_id, 1, len(objects)):
            print(
                f"\nPlease enter a valid number between 1 and {len(objects)}.")
            wait(2)
            continue
        break
    return objects[int(select_id) - 1]


def get_object_values(obj_fields, type, old_object=None, unit_map={}, restricted_fields=[]):

    if old_object is None:
        old_object = general_logic.get_class(type)
        for field in obj_fields:
            setattr(old_object, field, "")

    changes = {}

    while True:
        clear_screen()
        print(f"\n{type.capitalize()} details:")
        for idx, field in enumerate(obj_fields, start=1):
            value = getattr(old_object, field, "")
            unit = unit_map.get(field, "")
            field_name = field.replace('_', ' ').capitalize()
            print(
                f"{idx:2}. {field_name:<22}{'🔒 ' if field in restricted_fields else '   '}: {value}{unit if value and value != ' ' else ''}")
        select_id = input(
            "\nWhich field do you want to change? (Enter number or press Enter to finish): ").strip()

        if not select_id:
            empty_fields = [field for field in obj_fields if getattr(
                old_object, field) == ""]
            if empty_fields:
                empty_field_names = ", ".join(
                    [field.replace('_', ' ').capitalize() for field in empty_fields])
                message = f"The following fields are still empty: {empty_field_names}\n\nDo you want to quit"
                if boolean_confirmation_custom(message):
                    return
                else:
                    continue
            break

        if not general_logic.check_is_digit_valid(select_id, 1, len(obj_fields)):
            print(
                f"\nPlease enter a valid number between 1 and {len(obj_fields)}.")
            wait(2)
            continue

        if obj_fields[int(select_id) - 1] in restricted_fields:
            print(
                f"\nThe field '{obj_fields[int(select_id) - 1]}' is restricted and cannot be changed.")
            wait(2)
            continue

        field_to_update = obj_fields[int(select_id) - 1]
        while True:
            clear_screen()
            new_value = input(
                f"Enter new value for {field_to_update.replace('_', ' ').capitalize()} (or press Enter to cancel): ").strip()
            if not new_value:
                break

            type_logic = general_logic.get_logic_files(type)
            check_result, error_or_value = getattr(
                type_logic, f'validate_new_{type}_values')(field_to_update, new_value)
            if not check_result:
                print(
                    f"\nInvalid value: {error_or_value}")
                wait(3)
                continue

            if getattr(old_object, field_to_update) == error_or_value:
                if field_to_update in changes:
                    changes.pop(field_to_update)
            else:
                changes[field_to_update] = error_or_value
            setattr(old_object, field_to_update, error_or_value)
            break

    return changes
