from cryptography.fernet import Fernet
import os
import sys

ENCRYPTED_FIELDS = {
    'Users': ['username', 'first_name', 'last_name'],
    'Travellers': ['first_name', 'last_name', 'street_name', 'house_number', 'email_address', 'mobile_phone', 'driving_license_number'],
    'Scooters': [],
    'RestoreCodes': ['backup_filename']
}

class Encryption:
    def __init__(self):
        self._cipher = Fernet(self._get_key())
    
    def _get_key(self):
        key_file = "encryption.key"
        
        # Check if key file exists
        if not os.path.exists(key_file):
            print("\n❌ ERROR: encryption.key file not found!\n")
            print("Cannot decrypt existing data without the encryption key.")
            print("Please restore encryption.key from backup or contact an admin.\n")
            sys.exit(1)
        
        try:
            with open(key_file, 'rb') as f:
                key = f.read()
            
            # Test if key is valid
            test_cipher = Fernet(key)
            test_cipher.encrypt(b"test")
            
            return key
            
        except Exception:
            print("\n❌ ERROR: encryption.key file is corrupted!\n")
            print("Cannot decrypt existing data with invalid key.")
            print("Please restore encryption.key from backup or contact an admin.\n")
            sys.exit(1)

    def encrypt_data(self, data):
        try:
            return self._cipher.encrypt(data.encode()).decode()
        except Exception:
            return data

    def decrypt_data(self, encrypted_data):
        try:
            return self._cipher.decrypt(encrypted_data.encode()).decode()
        except Exception :
            return encrypted_data



    def encrypt_object_data(self, table_name, data_dict):
        encrypted_dict = data_dict.copy() 
        for field in ENCRYPTED_FIELDS[table_name]:
            if field in encrypted_dict:
                encrypted_dict[field] = self.encrypt_data(str(encrypted_dict[field]))
        return encrypted_dict

    def decrypt_object_data(self, table_name, data_dict):
        decrypted_dict = data_dict.copy()
        for field in ENCRYPTED_FIELDS[table_name]:
            if field in decrypted_dict:
                decrypted_dict[field] = self.decrypt_data(decrypted_dict[field]) if decrypted_dict[field] is not None else None
        return decrypted_dict


encryptor = Encryption()








