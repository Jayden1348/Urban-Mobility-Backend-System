import sqlite3
from Models.DataModels import User, Traveller, Scooter, Log


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


def update_item_from_table(table_name, identifier_value, new_values):
    allowed_tables = ['Logs', 'Scooters', 'Travellers', 'Users']
    if table_name not in allowed_tables:
        raise ValueError("Invalid table name.")

    primary_keys = {
        'Users': "Username",
        'Travellers': "DrivingLicenseNumber",
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
