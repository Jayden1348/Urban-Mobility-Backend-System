from cryptography.fernet import Fernet
import os

ENCRYPTED_FIELDS = {
    'Users': ['username', 'first_name', 'last_name'],
    'Travellers': ['first_name', 'last_name', 'street_name', 'house_number', 'email_address', 'mobile_phone', 'driving_license_number'],
    'Scooters': [],
    'RestoreCodes': ['backup_filename']
}

class Encryption:
    def __init__(self):
        self._cipher = Fernet(self._get_or_create_key())
    
    def _get_or_create_key(self):
        key_file = "encryption.key"
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
        return key

    def encrypt_data(self, data):
        return self._cipher.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data):
        return self._cipher.decrypt(encrypted_data.encode()).decode()


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








