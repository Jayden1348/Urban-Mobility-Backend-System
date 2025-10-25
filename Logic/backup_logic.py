from Access import DataAccess
from datetime import datetime
from Utils.encryption import encryptor
import zipfile
import os

def get_restore_code(search_key="", identifiers=None, filters=None):    # Done
    if identifiers is None:
        identifiers = ["code_id", "generated_for_user_id", "backup_filename"]
    return DataAccess.search_item_in_table(
        "RestoreCodes", search_key, identifiers=identifiers, filters=filters)


def add_restore_code(new_restore_code_data):   # Done
    return DataAccess.add_item_to_table("RestoreCodes", encryptor.encrypt_object_data("RestoreCodes", new_restore_code_data))


def delete_restore_code(restore_code_entry):    # Done
    return DataAccess.remove_item_from_table("RestoreCodes", restore_code_entry.code_id)


def validate_new_restore_code_values(user_id, backup_filename):  # Done
    existing_code = get_restore_code(identifiers=[],
        filters={"generated_for_user_id": user_id, "backup_filename": backup_filename})
    return len(existing_code) > 0



## Backup functions
def create_backup():    # Done
    backup_dir = "System Backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"scooter_system_backup_{timestamp}.zip"
    backup_filepath = os.path.join(backup_dir, backup_filename)
    
    # Complete system backup
    directories_to_backup = [
        "Access/",
        "Logic/",
        "Presentation/",
        "Models/",
        "Utils/",
        "Logs/",
    ]
    
    files_to_backup = [
        "ScooterApp.db",
        "encryption.key",
        "Program.py",
        "databasechange.py",
    ]
    
    try:
        with zipfile.ZipFile(backup_filepath, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
            for directory in directories_to_backup:
                if os.path.exists(directory):
                    for root, dirs, files in os.walk(directory):
                        for file in files:
                            if file.endswith('.py') or file.endswith('.enc') or not file.startswith('.'):
                                file_path = os.path.join(root, file)
                                backup_zip.write(file_path)
            
            # Add individual files
            for file_path in files_to_backup:
                if os.path.exists(file_path):
                    backup_zip.write(file_path)
        
        return True, backup_filename
    except Exception as e:
        return False, str(e)


def restore_backup(backup_filename, restore_code_obj):   # Done
    backup_dir = "System Backups"
    src = os.path.join(backup_dir, backup_filename)
    
    if not os.path.exists(src):
        return False, f"Backup file '{backup_filename}' does not exist."
    
    try:
        current_restore_codes = get_restore_code(identifiers=[])

        with zipfile.ZipFile(src, 'r') as backup_zip:
            file_list = backup_zip.namelist()
            
            for file_path in file_list:
                try:
                    file_dir = os.path.dirname(file_path)
                    if file_dir and not os.path.exists(file_dir):
                        os.makedirs(file_dir, exist_ok=True)
                    
                    backup_zip.extract(file_path, ".")
                    
                except Exception as file_error:
                    print(f"Warning: Could not restore file {file_path}: {file_error}")
                    continue

            # Restore existing restore codes
            DataAccess.clear_table("RestoreCodes")
            for restore_code in current_restore_codes:
                add_restore_code({"restore_code": restore_code.restore_code,
                                  "backup_filename": restore_code.backup_filename,
                                  "generated_for_user_id": restore_code.generated_for_user_id})

            if restore_code_obj:
                delete_restore_code(restore_code_obj)
        return True, f"Complete system restored from {backup_filename}. Files restored: {len(file_list)}"
        
    except Exception as e:
        return False, f"Restore failed: {str(e)}"


def get_all_backup_names():  # Done
    backup_dir = "System Backups"
    if not os.path.exists(backup_dir):
        return []
    
    backup_files = []
    for file in os.listdir(backup_dir):
        if file.endswith('.zip') and file.startswith('scooter_system_backup_'):
            backup_files.append(file)
    

    backup_files.sort(reverse=True)
    return backup_files


def cleanup_restore_code_table():
    available_backups = get_all_backup_names()
    all_restore_codes = get_restore_code(identifiers=[])
    
    removed_count = 0
    for code in all_restore_codes:
        if code.backup_filename not in available_backups:
            if delete_restore_code(code):
                removed_count += 1

    return removed_count
