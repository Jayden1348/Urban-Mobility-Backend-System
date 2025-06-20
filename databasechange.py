import sqlite3


def create_database():
    # SQLite database file name
    db_file = "ScooterApp.db"

    # Connect to SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Predefined list of cities
    CITIES = [
        "Rotterdam", "Amsterdam", "Utrecht", "Eindhoven", "Groningen",
        "Maastricht", "Delft", "Leiden", "Nijmegen", "Haarlem"
    ]

    # Drop tables if they exist
    cursor.execute("DROP TABLE IF EXISTS Logs;")
    cursor.execute("DROP TABLE IF EXISTS Scooters;")
    cursor.execute("DROP TABLE IF EXISTS Travellers;")
    cursor.execute("DROP TABLE IF EXISTS Users;")

    # Create tables
    cursor.execute("""
    CREATE TABLE Users (
        Username TEXT NOT NULL PRIMARY KEY,
        Password TEXT NOT NULL,
        FirstName TEXT  ,
        LastName TEXT,
        UserRole INTEGER NOT NULL CHECK(UserRole IN (0, 1, 2)), -- 0 = Super Administrator, 1 = System Administrator, 2 = Service Engineer       
        RegistrationDate DATETIME
    );
    """)

    cursor.execute(f"""
    CREATE TABLE Travellers (
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        DateOfBirth DATE NOT NULL,
        Gender TEXT CHECK(Gender IN ('male', 'female')) NOT NULL,
        StreetName TEXT NOT NULL,
        HouseNumber TEXT NOT NULL,
        ZipCode TEXT NOT NULL,
        City TEXT NOT NULL CHECK(City IN ({','.join([f"'{city}'" for city in CITIES])})),
        EmailAddress TEXT NOT NULL,
        MobilePhone TEXT NOT NULL, 
        DrivingLicenseNumber TEXT NOT NULL PRIMARY KEY, 
        RegistrationDate DATETIME NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE Scooters (
        Brand TEXT NOT NULL,
        Model TEXT NOT NULL,
        SerialNumber TEXT NOT NULL PRIMARY KEY,
        TopSpeed REAL NOT NULL, -- km/h
        BatteryCapacity REAL NOT NULL, -- Wh
        StateOfCharge INTEGER NOT NULL CHECK(StateOfCharge BETWEEN 0 AND 100), -- % 
        TargetRangeSoCMin INTEGER NOT NULL CHECK(TargetRangeSoCMin BETWEEN 0 AND 100),
        TargetRangeSoCMax INTEGER NOT NULL CHECK(TargetRangeSoCMax BETWEEN 0 AND 100),
        Latitude REAL NOT NULL CHECK(Latitude BETWEEN 51.85 AND 52.05), -- Rotterdam region approx.
        Longitude REAL NOT NULL CHECK(Longitude BETWEEN 4.35 AND 4.65), -- Rotterdam region approx.
        OutOfService INTEGER NOT NULL CHECK(OutOfService IN (0, 1)), -- 0 = available, 1 = out of service
        Mileage REAL NOT NULL, -- km
        LastMaintenanceDate TEXT NOT NULL, -- ISO 8601 format: YYYY-MM-DD
        InServiceDate DATETIME NOT NULL
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("SQLite database and tables created successfully.")


def dbconnect(query, data):
    db_file = "ScooterApp.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.executemany(query, data)
    conn.commit()
    cursor.close()
    conn.close()


def seed_scooters():
    scooters = [
        (
            "Segway", "Ninebot", "SN1001", 25.0, 374.0, 100, 20, 80, 51.92, 4.48, 0, 1200.5, "2024-06-01", "2024-01-15"
        ),
        (
            "Xiaomi", "M365", "SN1002", 25.0, 280.0, 85, 15, 90, 51.93, 4.50, 0, 800.0, "2024-05-20", "2024-02-10"
        ),
        (
            "NIU", "KQi3", "SN1003", 32.0, 460.0, 60, 10, 95, 51.95, 4.60, 1, 1500.0, "2024-04-10", "2024-03-01"
        ),
    ]
    query = """
        INSERT INTO Scooters (
            Brand, Model, SerialNumber, TopSpeed, BatteryCapacity, StateOfCharge,
            TargetRangeSoCMin, TargetRangeSoCMax, Latitude, Longitude, OutOfService,
            Mileage, LastMaintenanceDate, InServiceDate
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    dbconnect(query, scooters)
    print("Scooters table seeded successfully.")


def seed_users():
    users = [
        # Super Admins (role 0)
        (0, "super_admin", "Admin_123?", None, None, None),
        # System Admins (role 1)
        (1, "sysadmin1", "SysPass1!", "Alice", "Smith", "2024-06-01"),
        (1, "sysadmin2", "SysPass2!", "Bob", "Johnson", "2024-06-02"),
        # Service Engineers (role 2)
        (2, "engineer1", "EngPass1!", "Charlie", "Brown", "2024-06-03"),
        (2, "engineer2", "EngPass2!", "Dana", "White", "2024-06-04"),
    ]
    query = """
        INSERT INTO Users (UserRole, Username, Password, FirstName, LastName, RegistrationDate)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    dbconnect(query, users)
    print("Users table seeded successfully.")


if __name__ == "__main__":
    create_database()
    seed_users()
    seed_scooters()
