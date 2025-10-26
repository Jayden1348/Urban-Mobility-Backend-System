from Utils.encryption import encryptor, ENCRYPTED_FIELDS
import sqlite3
from Models.DataModels import User, Traveller, Scooter, RestoreCode

PRIMARY_KEYS = {
    'Users': "user_id",
    'Travellers': "customer_id",
    'Scooters': "scooter_id",
    'RestoreCodes': "code_id"
}


def search_item_in_table(table_name, search_value, identifiers=None, filters=None):
    allowed_tables = ['Scooters', 'Travellers', 'Users', 'RestoreCodes']
    if table_name not in allowed_tables:
        raise ValueError("Invalid table name.")

    conn = sqlite3.connect('ScooterApp.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        params = []
        encrypted_filters = {}
        
        # Check if ANY identifier is encrypted 
        has_encrypted_identifiers = False
        if identifiers:
            for field in identifiers:
                if field in ENCRYPTED_FIELDS.get(table_name, []):
                    has_encrypted_identifiers = True
                    break
            

        # Separate encrypted and non-encrypted filters
        query_filter_conditions = []
        if filters:
            for field, value in filters.items():
                if field not in ENCRYPTED_FIELDS.get(table_name, []):
                    query_filter_conditions.append(f"{field} = ?")
                    params.append(value)
                else:
                    encrypted_filters[field] = value


        query = f"SELECT * FROM {table_name}"
        
        if query_filter_conditions:
            query += " WHERE " + " AND ".join(query_filter_conditions)
        

        # Only add search conditions to SQL if NO identifiers are encrypted
        if not has_encrypted_identifiers and identifiers and search_value.strip():
            search_conditions = []
            for field in identifiers:
                search_conditions.append(f"{field} LIKE ?")
                params.append(f"%{search_value}%")
            
            if search_conditions:
                if query_filter_conditions:
                    query += " AND (" + " OR ".join(search_conditions) + ")"
                else:
                    query += " WHERE (" + " OR ".join(search_conditions) + ")"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Create objects with decrypted data
        model_map = {'Users': User, 'Travellers': Traveller, 'Scooters': Scooter, 'RestoreCodes': RestoreCode}
        model_class = model_map[table_name]
        all_objects = [model_class(**encryptor.decrypt_object_data(table_name, dict(row))) for row in rows]

        # Client-side filtering for encrypted filters
        if encrypted_filters:
            filtered_objects = []
            for obj in all_objects:
                filter_match = True
                for field, value in encrypted_filters.items():
                    if hasattr(obj, field):
                        if str(value).lower() != str(getattr(obj, field)).lower():
                            filter_match = False
                            break
                if filter_match:
                    filtered_objects.append(obj)
            all_objects = filtered_objects

        # Client-side search for identifiers
        if has_encrypted_identifiers and identifiers and search_value.strip():
            filtered_objects = []
            for obj in all_objects:
                search_match = False
                for field in identifiers:
                        if search_value.lower() in str(getattr(obj, field)).lower():
                            search_match = True
                            break
                if search_match:
                    filtered_objects.append(obj)
            all_objects = filtered_objects
        return all_objects

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def update_item_from_table(table_name, identifier_value, new_values):
    allowed_tables = ['Scooters', 'Travellers', 'Users', 'RestoreCodes']
    if table_name not in allowed_tables:
        raise ValueError("Invalid table name.")

    if not new_values or not isinstance(new_values, dict):
        raise ValueError("No values to insert or input is not a dictionary.")

    identifier = PRIMARY_KEYS[table_name]

    set_changes = ", ".join([f"{col} = ?" for col in new_values.keys()])
    values = list(new_values.values())
    values.append(identifier_value)

    query = f"UPDATE {table_name} SET {set_changes} WHERE {identifier} = ?"
    conn = sqlite3.connect('ScooterApp.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, values)
        conn.commit()
        success = cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        success = False
    finally:
        cursor.close()
        conn.close()
    return success


def remove_item_from_table(table_name, identifier_value):
    allowed_tables = ['Scooters', 'Travellers', 'Users', 'RestoreCodes']
    if table_name not in allowed_tables:
        raise ValueError("Invalid table name.")

    identifier = PRIMARY_KEYS[table_name]
    query = f"DELETE FROM {table_name} WHERE {identifier} = ?"

    conn = sqlite3.connect('ScooterApp.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (identifier_value,))
        conn.commit()
        success = cursor.rowcount > 0  # True if at least one row was deleted
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        success = False
    finally:
        cursor.close()
        conn.close()
    return success


def add_item_to_table(table_name, new_values):

    allowed_tables = ['Scooters', 'Travellers', 'Users', 'RestoreCodes']
    if table_name not in allowed_tables:
        raise ValueError("Invalid table name.")

    if not new_values or not isinstance(new_values, dict):
        raise ValueError("No values to insert or input is not a dictionary.")

    columns = ", ".join(new_values.keys())
    placeholders = ", ".join(["?"] * len(new_values))
    values = list(new_values.values())

    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    conn = sqlite3.connect('ScooterApp.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, values)
        conn.commit()
        return cursor.lastrowid

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def clear_table(table_name):
    allowed_tables = ['Scooters', 'Travellers', 'Users', 'RestoreCodes']
    if table_name not in allowed_tables:
        raise ValueError("Invalid table name.")
    
    conn = sqlite3.connect('ScooterApp.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"DELETE FROM {table_name}")
        conn.commit()
    except sqlite3.Error as e:
        print(f"Warning: Could not clear {table_name} table: {e}")
    finally:
        cursor.close()
        conn.close()