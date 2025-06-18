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
