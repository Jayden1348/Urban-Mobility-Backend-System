from .generaltools import *
from Logic import backup_logic, logs_logic


def make_backup(user):
    clear_screen()
    print("Creating a backup of the backend system...\n")
    success, info = backup_logic.create_backup()
    if success:
        print(f"Backup created successfully: {info}")
        logs_logic.new_log(user.username, "Created backup",
                           f"Backup file: {info}", 0)
    else:
        print(f"Backup failed: {info}")
        logs_logic.new_log(user.username, "Backup failed", f"Error: {info}", 1)
    wait(3)


def restore_backup(user):
    clear_screen()
    # Require code for System Admins
    if user.user_role == 1:
        code = input(
            "Enter the restore code provided by the Super Administrator (or press Enter to cancel): ").strip()
        if not code:
            print("Restore cancelled.")
            wait(2)
            return

        valid = backup_logic.verify_restore_code(code)
        if not valid:
            print("Invalid restore code.")
            logs_logic.new_log(user.username, "Restore failed",
                               "Invalid restore code entered", 1)
            wait(2)
            return

    backup_dir = "Backup Databases"
    if not os.path.exists(backup_dir):
        print("No backup directory found.")
        wait(2)
        return

    backups = [f for f in os.listdir(backup_dir) if f.endswith(".db")]
    if not backups:
        print("No backup files found.")
        wait(2)
        return

    print("Available backups:\n")
    for idx, fname in enumerate(backups, 1):
        print(f"{idx}. {fname}")

    print("\nEnter the number of the backup you want to restore (or press Enter to cancel):")
    choice = input("> ").strip()
    if not choice:
        print("Restore cancelled.")
        wait(2)
        return

    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(backups):
            raise ValueError
        backup_file = backups[idx]
    except ValueError:
        print("Invalid selection.")
        wait(2)
        return

    print(f"\nRestoring backup: {backup_file} ...")
    success, info = backup_logic.restore_backup(backup_file)
    if success:
        print(f"Restore successful: {info}")
        logs_logic.new_log(user.username, "Restored backup",
                           f"Restored from {backup_file}", 0)
    else:
        print(f"Restore failed: {info}")
        logs_logic.new_log(user.username, "Restore failed",
                           f"Error: {info}", 1)
    wait(3)
