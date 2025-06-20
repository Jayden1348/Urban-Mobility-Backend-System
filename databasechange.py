import sqlite3
from Logic.encryption import encrypt_data, hash_password, hash_username


def create_database():
    """
    Creates the SQLite database and tables.
    """
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
        FirstName TEXT,
        LastName TEXT,
        UserRole INTEGER NOT NULL CHECK(UserRole IN (0, 1, 2)), -- 0 = Super Administrator, 1 = System Administrator, 2 = Service Engineer
        RegistrationDate DATETIME
    );
    """)

    cursor.execute(f"""
    CREATE TABLE Travellers (
        CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
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
        DrivingLicenseNumber TEXT NOT NULL UNIQUE,
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
    """
    Executes a query with the provided data.
    """
    db_file = "ScooterApp.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.executemany(query, data)
        conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        cursor.close()
        conn.close()


def seed_scooters():
    """
    Seeds the Scooters table with initial data.
    """
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
    """
    Seeds the Users table with initial data.
    """
    users = [
        # Super Admins (role 0)
        (hash_username("super_admin"), hash_password("Admin_123?"), None, None, 0, "2024-06-01"),
        # System Admins (role 1)
        (hash_username("sysadmin1"), hash_password("SysPass1!"), encrypt_data("Alice"), encrypt_data("Smith"), 1, "2024-06-01"),
        (hash_username("sysadmin2"), hash_password("SysPass2!"), encrypt_data("Bob"), encrypt_data("Johnson"), 1, "2024-06-02"),
        # Service Engineers (role 2)
        (hash_username("engineer1"), hash_password("EngPass1!"), encrypt_data("Charlie"), encrypt_data("Brown"), 2, "2024-06-03"),
        (hash_username("engineer2"), hash_password("EngPass2!"), encrypt_data("Dana"), encrypt_data("White"), 2, "2024-06-04"),
    ]


    query = """
        INSERT INTO Users (Username, Password, FirstName, LastName, UserRole, RegistrationDate)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    dbconnect(query, users)
    print("Users table seeded successfully.")


def seed_logs():
    """
    Seeds the Logs table with initial data.
    """
    logs = [
        # (Date, Time, Username, Description, AdditionalInfo, Suspicious)
        ("2021-05-12", "15:51:19", encrypt_data("john_m_05"), "Logged in", None, 0),
        ("2021-05-12", "18:00:20", encrypt_data("superadmin"),
         "New admin user is created", "username: mike12", 0),
        ("2021-05-12", "18:05:33", None, "Unsuccessful login",
         'username: "mike12" is used for a login attempt with a wrong password', 0),
        ("2021-05-12", "18:07:10", None, "Unsuccessful login",
         "Multiple usernames and passwords are tried in a row", 1),
        ("2021-05-12", "18:08:02", encrypt_data("superadmin"),
         "User is deleted", 'User "mike12" is deleted', 0),
    ]
    query = """
        INSERT INTO Logs (Date, Time, Username, Description, AdditionalInfo, Suspicious)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    dbconnect(query, logs)
    print("Logs table seeded successfully.")


def seed_travellers():
    """
    Seeds the Travellers table with initial data.
    """
    travellers = [
        {
            "FirstName": encrypt_data("John"),
            "LastName": encrypt_data("Doe"),
            "DateOfBirth": "2000-01-01",
            "Gender": "male",
            "StreetName": encrypt_data("Main Street"),
            "HouseNumber": "123",
            "ZipCode": "12345",
            "City": "Rotterdam",
            "EmailAddress": encrypt_data("John@example.com"),
            "MobilePhone": encrypt_data("1234567890"),
            "DrivingLicenseNumber": encrypt_data("DL123456"),
            "RegistrationDate": "2024-06-01"
        },
    ]

    query = """
        INSERT INTO Travellers (
            FirstName, LastName, DateOfBirth, Gender, StreetName, HouseNumber,
            ZipCode, City, EmailAddress, MobilePhone, DrivingLicenseNumber, RegistrationDate
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    dbconnect(query, [tuple(traveller.values()) for traveller in travellers])
    print("Travellers table seeded successfully.")


if __name__ == "__main__":
    create_database()
    seed_users()
    seed_scooters()
    seed_logs()
    seed_travellers()

