from cryptography.fernet import Fernet, InvalidToken
import bcrypt
import hashlib

# This key should be stored securely (e.g., in an environment variable or a secure key vault)
# For demonstration purposes, it is hardcoded here.
key = b'FQmwlu2yec2W5fQNzAEBpR7kTzrdAIDO-PuAEQ8V9RM='
cipher = Fernet(key)

# -------------------------------
# Encryption and Decryption
# -------------------------------

def encrypt_data(data):
    """
    Encrypts the given data using Fernet encryption.
    """
    if data is None:
        return None
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(data):
    """
    Decrypts the given data using Fernet encryption.
    """
    if data is None:
        return None
    try:
        return cipher.decrypt(data.encode()).decode()
    except InvalidToken:
        return data  # Return plaintext if decryption fails

# -------------------------------
# Hashing for Passwords
# -------------------------------

def hash_password(password):
    """
    Hashes a password using bcrypt.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def validate_password(password, hashed_password):
    """
    Validates a password against its hashed value.
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

# -------------------------------
# Deterministic Hashing for Usernames
# -------------------------------

def hash_username(username):
    """
    Hashes the username using SHA-256 for deterministic matching.
    """
    return hashlib.sha256(username.encode()).hexdigest()