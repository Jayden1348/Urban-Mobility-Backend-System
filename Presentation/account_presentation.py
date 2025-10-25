from .general_presentation import *
from Logic import logs_logic, user_logic, account_logic
import copy, time, getpass

user_fields = ["username", "first_name", "last_name"]



def update_account(user):   # Done
    old_userprofile = copy.deepcopy(user)
    changes = get_object_values(user_fields, "user", old_object=old_userprofile)

    if not changes:
        clear_screen()
        print("No changes made. Cancelling...")

    else:
        if boolean_confirmation("update your profile", f"You are about to update your profile.\n\n"):
            if user_logic.update_user(user.user_id, changes):
                logs_logic.new_log(user.username, "Updated profile",
                                   f"{user.username} updated their profile")
                print("\nProfile updated successfully.")

                for field, new_value in changes.items():
                    setattr(user, field, new_value)
            else:
                logs_logic.new_log(user.username, "Failed update",
                                   f"{user.username} tried to update their profile.")
                print("\nFailed to update profile. Please try again later.")
        else:
            print("Profile update cancelled.")
    wait(2)


def update_password(user):  # Done
    if not identity_verification(user):
        return
    
    while True:
        clear_screen()
        new_password = getpass.getpass("Enter new password: ").strip()
        if not new_password:
            return
        
        confirm_password = getpass.getpass("Confirm new password: ").strip()
        if new_password != confirm_password:
            print("\nPasswords do not match. Please try again.")
            wait(2)
            continue
        
        is_valid, message = account_logic.validate_new_password(new_password, user.password)
        if not is_valid:
            print(f"\nPassword validation failed:\n{message}")
            wait(5)
            continue
        break

    ## Update Password
    update_password_data = {"password": account_logic.hash_password(new_password)}
    if user_logic.update_user(user.user_id, update_password_data):
        user.password = update_password_data["password"]
        logs_logic.new_log(user.username, "Updated password",
                           f"{user.username} updated their password")
        print("\nPassword updated successfully.")
    else:
        logs_logic.new_log(user.username, "Failed password update",
                           f"{user.username} tried to update their password.")
        print("\nFailed to update password. Please try again later.")
    wait(2)


def delete_account(user):   # Done
    warning = f"⚠️  DELETE ACCOUNT⚠️\nTHIS ACTION CANNOT BE UNDONE!\n\n"
    
    if not identity_verification(user, warning):
        return

    while True:
        print(warning)
        confirmation_input = input("Please type 'DELETE' to confirm account deletion (or press Enter to cancel): ")
        if confirmation_input == "DELETE":
            break
        elif confirmation_input == "":
            return
        else:
            print("\nIncorrect input. Please type 'DELETE' or press Enter.")
            wait(2)
        clear_screen()

    # Final confirmation after password success
    if boolean_confirmation("delete your account", f"{warning}\nFinal Warning: You are about to permanently delete your account and all associated data.\n"):
        if user_logic.delete_user(user.user_id, account_logic.get_role_num(user.user_role) == 1):
            logs_logic.new_log(user.username, "Deleted account", 
                            f"{user.username} deleted their own account")
            print("Account deleted successfully. Logging out...")
            wait(2)
            return "LogOut"
        else:
            logs_logic.new_log(user.username, "Failed account deletion", 
                            f"{user.username} tried to delete their own account")
            print("Failed to delete account. Please try again later.")
    



LOGIN_COOLDOWN = 0
LOGIN_COOLDOWN_SECONDS = 60
TOTAL_FAILED_ATTEMPTS = 0
MAX_ATTEMPTS = 5

def identity_verification(user=None, extra_message=""): # Done
    global LOGIN_COOLDOWN, TOTAL_FAILED_ATTEMPTS
    
    if LOGIN_COOLDOWN > 0:
        remaining_cooldown = LOGIN_COOLDOWN - time.time()
        if remaining_cooldown > 0:
            print(f"❌ Identity Verification temporarily disabled. Please wait {int(remaining_cooldown)} seconds.")
            wait(2)
            return
        else:
            LOGIN_COOLDOWN = 0

    show_message = extra_message + "\nIdentity Verification\n"

    if TOTAL_FAILED_ATTEMPTS < MAX_ATTEMPTS:
        remaining_attempts = MAX_ATTEMPTS - TOTAL_FAILED_ATTEMPTS
    else:
        remaining_attempts = 1
    
    for attempt in range(remaining_attempts):
        clear_screen()
        print(show_message)

        if user is None:
            username = input("Username: ")
            if not username:
                return
        else:
            username = user.username
            print(f"Username: {username}")
        password = getpass.getpass("\nEnter password (hidden for privacy): ")

        if not password:
            return
        
        if user is None:
            user, validation_success = account_logic.verify_password_username(username, password)
        else:
            validation_success = account_logic.verify_password(user.password, password)

        if validation_success:
            TOTAL_FAILED_ATTEMPTS = 0
            clear_screen()
            return user
        else:
            TOTAL_FAILED_ATTEMPTS += 1

            
            if TOTAL_FAILED_ATTEMPTS <= MAX_ATTEMPTS:
                remaining = MAX_ATTEMPTS - TOTAL_FAILED_ATTEMPTS
                if remaining > 0:
                    logs_logic.new_log(None, "Failed identity verification", f"Username: '{user.username if user else username}' failed a verification attempt (Total: {TOTAL_FAILED_ATTEMPTS})", 1 if TOTAL_FAILED_ATTEMPTS >= 3 else 0)
                    print(f"\n❌ Incorrect password. {remaining} attempts remaining.")
                    wait(2)
                    
                else:
                    LOGIN_COOLDOWN = time.time() + LOGIN_COOLDOWN_SECONDS
                    print(f"\n❌ Too many failed attempts. Please wait {LOGIN_COOLDOWN_SECONDS} seconds before trying again.")
                    logs_logic.new_log(None, "User lockout", f"Username: '{user.username if user else username}' has been locked out after {TOTAL_FAILED_ATTEMPTS} failed verification attempts.", 1)
                    wait(2)
                    return
            else:
                cooldown_multiplier = TOTAL_FAILED_ATTEMPTS - MAX_ATTEMPTS
                escalated_cooldown = LOGIN_COOLDOWN_SECONDS * (2 ** cooldown_multiplier)
                LOGIN_COOLDOWN = time.time() + escalated_cooldown
                print(f"\n❌ Incorrect password. Please wait {int(escalated_cooldown)} seconds before trying again.")
                wait(2)
                return
    
    return