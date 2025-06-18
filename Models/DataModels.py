from datetime import datetime


class User:
    def __init__(self, Username, Password, FirstName, LastName, UserRole, RegistrationDate):
        self.username = Username
        self.password = Password
        self.first_name = FirstName
        self.last_name = LastName
        self.user_role = UserRole  # 0 = Super Admin, 1 = System Admin, 2 = Service Engineer
        self.registration_date = RegistrationDate

    def __repr__(self):
        return f"User(username={self.username}, role={self.user_role})"


class Traveller:
    def __init__(
        self, FirstName, LastName, DateOfBirth, Gender, StreetName, HouseNumber,
        ZipCode, City, EmailAddress, MobilePhone, DrivingLicenseNumber, RegistrationDate
    ):
        self.first_name = FirstName
        self.last_name = LastName
        self.date_of_birth = DateOfBirth
        self.gender = Gender
        self.street_name = StreetName
        self.house_number = HouseNumber
        self.zip_code = ZipCode
        self.city = City
        self.email_address = EmailAddress
        self.mobile_phone = MobilePhone
        self.driving_license_number = DrivingLicenseNumber
        self.registration_date = RegistrationDate

    def __repr__(self):
        return f"Traveller({self.first_name} {self.last_name}, {self.city})"


class Scooter:
    def __init__(
        self, Brand, Model, SerialNumber, TopSpeed, BatteryCapacity, StateOfCharge,
        TargetRangeSoCMin, TargetRangeSoCMax, Latitude, Longitude, OutOfService,
        Mileage, LastMaintenanceDate, InServiceDate
    ):
        self.brand = Brand
        self.model = Model
        self.serial_number = SerialNumber
        self.top_speed = TopSpeed
        self.battery_capacity = BatteryCapacity
        self.state_of_charge = StateOfCharge
        self.target_range_soc_min = TargetRangeSoCMin
        self.target_range_soc_max = TargetRangeSoCMax
        self.latitude = Latitude
        self.longitude = Longitude
        self.out_of_service = OutOfService
        self.mileage = Mileage
        self.last_maintenance_date = LastMaintenanceDate
        self.in_service_date = InServiceDate

    def __repr__(self):
        return f"Scooter({self.brand} {self.model}, SN={self.serial_number})"


class Log:
    def __init__(
        self, LogID, Date, Time, Username, Description, AdditionalInfo, Suspicious
    ):
        self.log_id = LogID
        self.date = Date
        self.time = Time
        self.username = Username
        self.description = Description
        self.additional_info = AdditionalInfo
        self.suspicious = Suspicious  # 0 = No, 1 = Yes

    def __repr__(self):
        return f"Log({self.log_id}, {self.date} {self.time}, user={self.username})"
