from .general_presentation import *
from Logic import backup_logic, logs_logic, account_logic
from Presentation.users_presentation import display_user_fields
import pyperclip
import getpass
display_restore_code_fields = ["code_id", "generated_for_user_id", "backup_filename"]


def search_restore_codes(): # Done
    display_objects_table(display_restore_code_fields, "restore code", selection=False)


def add_restore_code(user): # Done
    clear_screen()
    input("Choose a user to generate a restore code for, and a backup to restore from.\n\nPress Enter to continue...")
    code_user = display_objects_table(display_user_fields, "user", selection=True, filters={"user_role": 1})
    if code_user is None:
        return 
    
    backup_filename, restore_code_obj = select_backup_to_restore(user)
    if backup_filename is None:
        return
    
    if backup_logic.validate_new_restore_code_values(code_user.user_id, backup_filename):
        clear_screen()
        print(f"A restore code for user {code_user.username} and backup {backup_filename} already exists!")
        wait(3)
        return
    
    new_restore_code = account_logic.generate_password()
    success= backup_logic.add_restore_code({"generated_for_user_id": code_user.user_id, "backup_filename": backup_filename, "restore_code": account_logic.hash_password(new_restore_code)})
    clear_screen()
    if success:
        logs_logic.new_log(user.username, "Generated restore code",
                f"Generated restore code for user #{code_user.user_id}, Backup file: {backup_filename}", 0)
        pyperclip.copy(new_restore_code)
        print(f"\nRestore code generated successfully.\n\nThe restore code is: {new_restore_code}\n\nThe code has been copied and added to your clipboard\nPlease make sure to communicate this code securely to this user.")

    else:
        print(f"\nFailed to generate restore code")
        logs_logic.new_log(user.username, "Failed to generate restore code",
                           f"An error occurred while creating restore code", 1)
    input("\nPress Enter to continue...")


def revoke_restore_code(user):  # Done
    chosen_restore_code = display_objects_table(display_restore_code_fields, "restore code", selection=True)
    if chosen_restore_code is None:
        return
    if boolean_confirmation("delete this restore code", f"You are about to delete restore code #{chosen_restore_code.code_id}\n\n"):
        if backup_logic.delete_restore_code(chosen_restore_code):
            logs_logic.new_log(user.username, "Deleted restore code",
                               f"Deleted restore code #{chosen_restore_code.code_id}")
            print(f"Restore code #{chosen_restore_code.code_id} deleted successfully.")
        else:
            logs_logic.new_log(user.username, "Failed deletion",
                               f"{user.username} tried to deleted restore code #{chosen_restore_code.code_id}")
            print("Failed to delete restore code!")
    else:
        print("Restore code deletion cancelled.")
    wait(2)



# Backup functions
def make_backup(user):  # Done
    clear_screen()
    success, filename = backup_logic.create_backup()
    if success:
        print(f"Backup created successfully: {filename}")
        logs_logic.new_log(user.username, "Created backup",
                           f"Backup file: {filename}", 0)
    else:
        print(f"Backup failed: {filename}")
        logs_logic.new_log(user.username, "Backup failed", f"An error occurred while creating backup", 1)
    wait(3)


def restore_backup(user):   # Done

    backup_filename, restore_code_obj = select_backup_to_restore(user)
    if backup_filename is None:
        return

    clear_screen()
    if not boolean_confirmation(f"restore system from backup", f"You are about to restore the entire system from backup {backup_filename}.\n\n⚠️  This action will overwrite existing data!⚠️\nFor safety, a new backup will be created before proceeding.\n\n"):
        return 
    
    make_backup(user)  # Create a backup before restoring

    success, info = backup_logic.restore_backup(backup_filename, restore_code_obj)
    if success:
        print(f"\nBackup restored successfully from: {backup_filename}")
        logs_logic.new_log(user.username, "Restored backup",
                           f"Backup file: {backup_filename} restored", 0)
    else:
        print(f"\nBackup restoration failed: {info}")
        logs_logic.new_log(user.username, "Backup restoration failed",
                           f"An error occurred while restoring backup", 1)
    input("\nPress Enter to continue...")


def select_backup_to_restore(user): # Done
    user_role = account_logic.get_role_num(user.user_role)
    if user_role == 0:
        get_all_backups = backup_logic.get_all_backup_names()

    elif user_role == 1:
        all_available_backups = backup_logic.get_all_backup_names()
        all_restore_codes_for_user = backup_logic.get_restore_code(identifiers=[], filters={"generated_for_user_id": user.user_id})
        
        valid_restore_codes = []
        for restore_code in all_restore_codes_for_user:
            if restore_code.backup_filename in all_available_backups:
                valid_restore_codes.append(restore_code)
        
        get_all_backups = [code.backup_filename for code in valid_restore_codes]


    if not get_all_backups:
        clear_screen()
        print("No backups available for restoration.")
        if user_role == 1:
            print("\nYou do not have any backup restore codes assigned to you.")
        wait(3)
        return None, None
    
    while True:
        clear_screen()
        print("Choose a backup for restoration:")
        for i, backup in enumerate(get_all_backups, start=1):
            print(f" {i} - {backup}")
        backup_filename_num = input("\nEnter id of backup to restore: ").strip()
        if backup_filename_num == "":
            return None, None
        if backup_filename_num.isdigit() and 1 <= int(backup_filename_num) <= len(get_all_backups):
            if user_role == 1:
                chosen_restore_code = all_restore_codes_for_user[int(backup_filename_num) - 1]
                clear_screen()
                input_code = getpass.getpass(f"Enter your restore code for {chosen_restore_code.backup_filename} (hidden for privacy): ").strip()
                if not account_logic.verify_password(chosen_restore_code.restore_code, input_code):
                    clear_screen()
                    print("Invalid restore code.")
                    wait(2)
                    continue
            return get_all_backups[int(backup_filename_num) - 1], chosen_restore_code if user_role == 1 else None
        else:
            print("\nInvalid option. Please try again.")
            wait(2)


def cleanup_restore_codes():
    num_of_removed = backup_logic.cleanup_restore_code_table()
    clear_screen()
    if num_of_removed > 0:
        print(f"Cleanup complete. Removed {num_of_removed} obsolete restore codes.")
    else:
        print("Cleanup complete. No obsolete restore codes found.")
    wait(3)