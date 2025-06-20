import sqlite3
from Models.DataModels import User, Traveller, Scooter, Log
from Logic.encryption import encrypt_data, decrypt_data
from Logic.encryption import hash_password

def get_all_from_table(table_name):
    allowed_tables = ['Logs', 'Scooters', 'Travellers', 'Users']

    if table_name not in allowed_tables:
        raise ValueError("Invalid table name.")

    conn = sqlite3.connect('ScooterApp.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()

    model_map = {
        'Users': User,
        'Travellers': Traveller,
        'Scooters': Scooter,
        'Logs': Log
    }
    model_class = model_map[table_name]
    objects = [model_class(**row) for row in results]
    return objects


def get_one_from_table(table_name, identifier_value):
    allowed_tables = ['Logs', 'Scooters', 'Travellers', 'Users']
    if table_name not in allowed_tables:
        raise ValueError("Invalid table name.")

    primary_keys = {
        'Users': "Username",
        'Travellers': "CustomerID",
        'Scooters': "SerialNumber",
        'Logs': "LogID"
    }
    identifier = primary_keys[table_name]

    conn = sqlite3.connect('ScooterApp.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    query = f"SELECT * FROM {table_name} WHERE {identifier} = ?"
    cursor.execute(query, (identifier_value,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    model_map = {
        'Users': User,
        'Travellers': Traveller,
        'Scooters': Scooter,
        'Logs': Log
    }
    model_class = model_map[table_name]
    return model_class(**dict(row))


def update_item_from_table(table_name, identifier_value, new_values):
    allowed_tables = ['Logs', 'Scooters', 'Travellers', 'Users']
    if table_name not in allowed_tables:
        raise ValueError("Invalid table name.")

    primary_keys = {
        'Users': "Username",
        'Travellers': "CustomerID",
        'Scooters': "SerialNumber",
        'Logs': "LogID"
    }
    identifier = primary_keys[table_name]

    set_changes = ", ".join([f"{col} = ?" for col in new_values.keys()])
    values = list(new_values.values())
    values.append(identifier_value)

    query = f"UPDATE {table_name} SET {set_changes} WHERE {identifier} = ?"

    conn = sqlite3.connect('ScooterApp.db')
    cursor = conn.cursor()
    cursor.execute(query, values)
    conn.commit()
    success = cursor.rowcount > 0  # True if at least one row was updated
    cursor.close()
    conn.close()
    return success

def remove_item_from_table(table_name, identifier_value):
    allowed_tables = ['Logs', 'Scooters', 'Travellers', 'Users']
    if table_name not in allowed_tables:
        raise ValueError("Invalid table name.")

    primary_keys = {
        'Users': "Username",
        'Travellers': "CustomerID",
        'Scooters': "SerialNumber",
        'Logs': "LogID"
    }
    identifier = primary_keys[table_name]

    query = f"DELETE FROM {table_name} WHERE {identifier} = ?"

    conn = sqlite3.connect('ScooterApp.db')
    cursor = conn.cursor()
    cursor.execute(query, (identifier_value,))
    conn.commit()
    success = cursor.rowcount > 0  # True if at least one row was deleted
    cursor.close()
    conn.close()
    return success



def add_item_to_table(table_name, new_values):

    allowed_tables = ['Logs', 'Scooters', 'Travellers', 'Users']
    if table_name not in allowed_tables:
        raise ValueError("Invalid table name.")

    # encription
    if table_name == "Users":
        new_values["Username"] = encrypt_data(new_values["Username"])
        new_values["Password"] = hash_password(new_values["Password"])  # Hash passwords
    elif table_name == "Travellers":
        for field in ["FirstName", "LastName", "EmailAddress", "MobilePhone", "StreetName"]:
            new_values[field] = encrypt_data(new_values[field])


    columns = ", ".join(new_values.keys())
    placeholders = ", ".join(["?"] * len(new_values))
    values = list(new_values.values())

    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    conn = sqlite3.connect('ScooterApp.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, values)
        conn.commit()
        success = True

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

        success = False
    finally:
        cursor.close()
        conn.close()

    return success
