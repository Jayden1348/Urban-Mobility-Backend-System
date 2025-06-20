import shutil
import os
from datetime import datetime


def create_backup():
    src = "ScooterApp.db"
    backup_dir = "Backup Databases"
    # Create the folder if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dst = os.path.join(backup_dir, f"backup_ScooterApp_{timestamp}.db")
    try:
        shutil.copy2(src, dst)
        return True, dst
    except Exception as e:
        return False, str(e)


def restore_backup(backup_filename):
    backup_dir = "Backup Databases"
    src = os.path.join(backup_dir, backup_filename)
    dst = "ScooterApp.db"
    if not os.path.exists(src):
        return False, f"Backup file '{backup_filename}' does not exist."
    try:
        shutil.copy2(src, dst)
        return True, f"Database restored from {backup_filename}."
    except Exception as e:
        return False, str(e)

# def verify_restore_code(backup):
