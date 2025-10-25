import re
import string
import random
import bcrypt
from Logic import user_logic


def check_new_username(new_username):
    # Length check
    if not (8 <= len(new_username) <= 10):
        return False, "Username must be between 8 and 10 characters!"

    # Start character check
    if not re.match(r"^[a-zA-Z_]", new_username):
        return False, "Username must start with a letter or underscore (_)!"

    # Allowed characters check
    if not re.match(r"^[a-zA-Z0-9_'.]+$", new_username):
        return False, "Username can only contain letters, numbers, underscores (_), apostrophes ('), and periods (.)"

    # Uniqueness check (case-insensitive)
    if user_logic.get_user(identifiers=[], filters={"username": new_username}):
        return False, "This username is already taken. Please choose another one."

    return True, new_username.lower()


def get_role_num(role_str):
    roles = {
        "super admin": 0,
        "system admin": 1,
        "service engineer": 2
    }
    return roles.get(role_str.lower(), -1)


# Password functions
def verify_password(stored_hash, entered_password):         # Done
    password_bytes = entered_password.encode('utf-8')
    hashed_bytes = stored_hash.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def verify_password_username(username, entered_password):   # Done
    user = user_logic.get_user(identifiers=[], filters={"username": username})
    if user:
        return user[0], verify_password(user[0].password, entered_password)
    return None, False


def validate_new_password(new_password, old_password):      # Done
    
    errors = []

    # Length check
    if len(new_password) < 12:
        errors.append("Password must be at least 12 characters")
    elif len(new_password) > 30:
        errors.append("Password must be no longer than 30 characters")

    # Allowed characters check
    allowed_specials = "~!@#$%&_-+=`|\\(){}[]:;'<>,.?/"
    allowed_chars = string.ascii_letters + string.digits + allowed_specials
    
    invalid_chars = set(new_password) - set(allowed_chars)
    if invalid_chars:
        errors.append(f"Password contains invalid characters: {', '.join(sorted(invalid_chars))}")


    # At least one lowercase letter
    if not re.search(r"[a-z]", new_password):
        errors.append("Password must contain at least one lowercase letter")

    # At least one uppercase letter
    if not re.search(r"[A-Z]", new_password):
        errors.append("Password must contain at least one uppercase letter")

    # At least one digit
    if not re.search(r"\d", new_password):
        errors.append("Password must contain at least one digit")

    # At least one special character
    if not re.search(rf"[{re.escape(allowed_specials)}]", new_password):
        errors.append("Password must contain at least one special character")

    if verify_password(old_password, new_password):
        errors.append("New password cannot be the same as the old password")

    if errors:
        return False, "\n".join([f"- {error}" for error in errors])

    return True, "Password meets all requirements"


def hash_password(password):                                # Done
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def generate_password(length=16):                           # Done
    specials = "~!@#$%&_-+=`|\\(){}[]:;'<>,.?/"

    if length < 12:
        length = 12
    if length > 30:
        length = 30

    num_of_symbols = min(4, max(3, length // 5))  # 3-4 special chars
    num_of_digits = max(2, length // 8)            # At least 2 digits
    num_of_uppercase = max(2, length // 8)         # At least 2 uppercase
    num_of_lowercase = length - num_of_symbols - num_of_digits - num_of_uppercase 

    password_chars = []
    
    for _ in range(num_of_symbols):
        password_chars.append(random.choice(specials))
    
    for _ in range(num_of_digits):
        password_chars.append(random.choice(string.digits))
    
    for _ in range(num_of_uppercase):
        password_chars.append(random.choice(string.ascii_uppercase))

    for _ in range(num_of_lowercase):
        password_chars.append(random.choice(string.ascii_lowercase))

    random.shuffle(password_chars)
    return ''.join(password_chars)