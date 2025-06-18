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
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserRole INTEGER NOT NULL CHECK(UserRole IN (0, 1, 2)), -- 0 = Super Administrator, 1 = System Administrator, 2 = Service Engineer
        Username TEXT NOT NULL,
        Password TEXT NOT NULL,
        FirstName TEXT  ,
        LastName TEXT,        
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

    cursor.execute("""
    CREATE TABLE Logs (
        LogID INTEGER PRIMARY KEY AUTOINCREMENT,
        Date DATE NOT NULL,
        Time TIME NOT NULL,
        Username TEXT NOT NULL,
        Description TEXT NOT NULL,
        AdditionalInfo TEXT,
        Suspicious INTEGER NOT NULL CHECK(Suspicious IN (0, 1)) -- 0 = No, 1 = Yes
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()

    print("SQLite database and tables created successfully.")


def create_user(userrole, username, password, firstname, lastname, registrationdate):
    if userrole in (1, 2):
        if not (firstname and lastname and registrationdate):
            print("System Administrators and Service Engineers must have a first name, last name, and registration date.")
            return
    if userrole == 0 and (firstname or lastname or registrationdate):
        firstname = None
        lastname = None
        registrationdate = None
        print("Super Administrators don't have profile info. Firstname, lastname and registrationdate set to None")
    db_file = "ScooterApp.db"
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Users (UserRole, Username, Password, FirstName, LastName, RegistrationDate)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (userrole, username, password, firstname, lastname, registrationdate))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"User '{username}' created successfully.")


if __name__ == "__main__":
    create_database()
    create_user(0, "super_admin", "Admin_123?", None, None, None)
