import sqlite3
import bcrypt
from Utils.encryption import encryptor

def create_database():
    db_file = "ScooterApp.db"

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    CITIES = [
        "Rotterdam", "Amsterdam", "Utrecht", "Eindhoven", "Groningen",
        "Maastricht", "Delft", "Leiden", "Nijmegen", "Haarlem"
    ]

    cursor.execute("DROP TABLE IF EXISTS Scooters;")
    cursor.execute("DROP TABLE IF EXISTS Travellers;")
    cursor.execute("DROP TABLE IF EXISTS Users;")
    cursor.execute("DROP TABLE IF EXISTS RestoreCodes;")

    cursor.execute("""
    CREATE TABLE Scooters (
        scooter_id INTEGER PRIMARY KEY AUTOINCREMENT,
        brand TEXT NOT NULL,
        model TEXT NOT NULL,
        serial_number TEXT NOT NULL UNIQUE,
        top_speed INTEGER NOT NULL,
        battery_capacity REAL NOT NULL,
        state_of_charge INTEGER NOT NULL CHECK(state_of_charge BETWEEN 0 AND 100),
        target_range_soc_min INTEGER NOT NULL CHECK(target_range_soc_min BETWEEN 0 AND 100),
        target_range_soc_max INTEGER NOT NULL CHECK(target_range_soc_max BETWEEN 0 AND 100),
        latitude REAL NOT NULL CHECK(latitude BETWEEN 51.85 AND 52.05),
        longitude REAL NOT NULL CHECK(longitude BETWEEN 4.35 AND 4.65),
        out_of_service INTEGER NOT NULL CHECK(out_of_service IN (0, 1)),
        mileage REAL NOT NULL,
        last_maintenance_date TEXT NOT NULL,
        in_service_date TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        first_name TEXT,
        last_name TEXT,
        user_role INTEGER NOT NULL CHECK(user_role IN (0, 1, 2)),
        registration_date TEXT
    );
    """)

    cursor.execute(f"""
    CREATE TABLE Travellers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        driving_license_number TEXT NOT NULL UNIQUE,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        date_of_birth TEXT NOT NULL,
        gender INTEGER NOT NULL CHECK(gender IN (0, 1)),
        street_name TEXT NOT NULL,
        house_number TEXT NOT NULL,
        zip_code TEXT NOT NULL,
        city TEXT NOT NULL CHECK(city IN ({','.join([f"'{city}'" for city in CITIES])})),
        email_address TEXT NOT NULL,
        mobile_phone TEXT NOT NULL,
        registration_date TEXT NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE RestoreCodes (
        code_id INTEGER PRIMARY KEY AUTOINCREMENT,
        restore_code TEXT NOT NULL UNIQUE,
        backup_filename TEXT NOT NULL,
        generated_for_user_id INTEGER NOT NULL,
        FOREIGN KEY (generated_for_user_id) REFERENCES Users(user_id)
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
    import random
    import string

    def random_serial(length):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def random_lat():
        return round(random.uniform(51.85, 52.05), 5)

    def random_long():
        return round(random.uniform(4.35, 4.65), 5)

    brands = ["Segway", "Xiaomi", "NIU", "E-TWOW", "Inokim",
              "Vsett", "Kaabo", "Dualtron", "Apollo", "Zero"]
    models = ["Ninebot", "M365", "KQi3", "GT",
              "Light", "Mini", "Pro", "Ultra", "City", "Max"]
    scooters = []
    for i in range(30):
        brand = random.choice(brands)
        model = random.choice(models)
        serial_len = random.randint(10, 17)
        serial = random_serial(serial_len)
        top_speed = round(random.uniform(20, 40))
        battery = round(random.uniform(250, 500), 1)
        soc = random.randint(0, 100)
        soc_min = random.randint(0, 50)
        soc_max = random.randint(soc_min + 1, 100)
        lat = random_lat()
        long = random_long()
        out_of_service = random.randint(0, 1)
        mileage = round(random.uniform(100, 3000), 1)
        last_maint = f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
        in_service = f"2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}"

        scooters.append((brand, model, serial, top_speed, battery, soc, soc_min,
                        soc_max, lat, long, out_of_service, mileage, last_maint, in_service))
    query = """
        INSERT INTO Scooters (
            brand, model, serial_number, top_speed, battery_capacity, state_of_charge,
            target_range_soc_min, target_range_soc_max, latitude, longitude, out_of_service,
            mileage, last_maintenance_date, in_service_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    dbconnect(query, scooters)
    print("Scooters table seeded successfully.")


def seed_users():
    plain_passwords = [
        "Admin_123?",
        "SysPassword1!",
        "SysPassword2!",
        "SysPassword3!",
        "SysPassword4!",
        "EngPassword1!",
        "EngPassword2!",
        "EngPassword3!",
        "EngPassword4!"
    ]
    
    # Hash all passwords
    hashed_passwords = []
    for password in plain_passwords:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        hashed_passwords.append(hashed.decode('utf-8'))
    
    users = [
        # Super Admins (role 0)
        (encryptor.encrypt_data("super_admin"), hashed_passwords[0], None, None, 0, None),

        # System Admins (role 1)
        (encryptor.encrypt_data("sysadmin1"), hashed_passwords[1], encryptor.encrypt_data("Max"), encryptor.encrypt_data("Verstappen"), 1, "2024-06-02"),
        (encryptor.encrypt_data("sysadmin2"), hashed_passwords[2], encryptor.encrypt_data("Oscar"), encryptor.encrypt_data("Piastri"), 1, "2024-06-03"),
        (encryptor.encrypt_data("sysadmin3"), hashed_passwords[3], encryptor.encrypt_data("Lando"), encryptor.encrypt_data("Norris"), 1, "2024-06-04"),
        (encryptor.encrypt_data("sysadmin4"), hashed_passwords[4], encryptor.encrypt_data("George"), encryptor.encrypt_data("Russell"), 1, "2024-06-05"),

        # Service Engineers (role 2)
        (encryptor.encrypt_data("engineer1"), hashed_passwords[5], encryptor.encrypt_data("Charles"), encryptor.encrypt_data("Leclerc"), 2, "2024-06-06"),
        (encryptor.encrypt_data("engineer2"), hashed_passwords[6], encryptor.encrypt_data("Carlos"), encryptor.encrypt_data("Sainz"), 2, "2024-06-07"),
        (encryptor.encrypt_data("engineer3"), hashed_passwords[7], encryptor.encrypt_data("Lewis"), encryptor.encrypt_data("Hamilton"), 2, "2024-06-08"),
        (encryptor.encrypt_data("engineer4"), hashed_passwords[8], encryptor.encrypt_data("Fernando"), encryptor.encrypt_data("Alonso"), 2, "2024-06-09"),
    ]
    
    query = """
        INSERT INTO Users (username, password, first_name, last_name, user_role, registration_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    dbconnect(query, users)
    print("Users table seeded successfully with hashed passwords.")


def seed_travellers():
    import random
    import string
    import datetime
    first_names = ["Emma", "Noah", "Sophie", "Daan", "Julia", "Sem", "Mila",
                   "Luuk", "Sara", "Finn", "Lotte", "Jesse", "Eva", "Bram", "Tess"]
    last_names = ["de Jong", "Jansen", "de Vries", "van den Berg", "Bakker", "van Dijk",
                  "Visser", "Smit", "Meijer", "de Boer", "Mulder", "Bos", "Vos", "Peters", "Hendriks"]
    streets = ["Hoofdstraat", "Dorpsweg", "Stationslaan", "Kerkstraat", "Schoolstraat",
               "Lindelaan", "Burgemeesterweg", "Parklaan", "Molenstraat", "Spoorweg"]
    cities = ["Rotterdam", "Amsterdam", "Utrecht", "Eindhoven",
              "Groningen", "Maastricht", "Delft", "Leiden", "Nijmegen", "Haarlem"]
    emails = ["gmail.com", "hotmail.com", "outlook.com", "student.hr.nl"]
    travellers = []
    today = datetime.date.today()

    used_dl_numbers = set()
    for i in range(30):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        years_ago = random.randint(18, 80)
        birth_year = today.year - years_ago
        birth_month = random.randint(1, 12)
        birth_day = random.randint(1, 28)
        dob = f"{birth_year}-{birth_month:02d}-{birth_day:02d}"
        gender = random.randint(0, 1)
        street = random.choice(streets)
        house_nr = str(random.randint(1, 200))
        zipcode = f"{random.randint(1000,9999)}{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}"
        city = random.choice(cities)
        email = f"{fn.lower()}.{ln.split()[0].lower()}{i}@{random.choice(emails)}"
        mobile = f"+31-6-{''.join([str(random.randint(0,9)) for _ in range(8)])}"
        reg_date = f"2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}"

        while True:
            dl_first = random.choice(string.ascii_uppercase)
            dl_second = random.choice(string.ascii_uppercase + string.digits)
            dl_digits = ''.join([str(random.randint(0, 9)) for _ in range(7)])
            dl_number = f"{dl_first}{dl_second}{dl_digits}"
            if dl_number not in used_dl_numbers:
                used_dl_numbers.add(dl_number)
                break

        travellers.append(( encryptor.encrypt_data(fn),
                            encryptor.encrypt_data(ln),
                            dob, 
                            gender, 
                            encryptor.encrypt_data(street), 
                            encryptor.encrypt_data(house_nr),
                            zipcode,
                            city,
                            encryptor.encrypt_data(email),
                            encryptor.encrypt_data(mobile),
                            encryptor.encrypt_data(dl_number),
                            reg_date))
    query = f"""
        INSERT INTO Travellers (
            first_name, last_name, date_of_birth, gender, street_name, house_number, zip_code, city,
            email_address, mobile_phone, driving_license_number, registration_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    dbconnect(query, travellers)
    print("Travellers table seeded successfully.")


if __name__ == "__main__":
    create_database()
    seed_users()
    seed_scooters()
    seed_travellers()