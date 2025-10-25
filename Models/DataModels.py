

class User:
    def __init__(self, user_id, username, password, first_name, last_name, user_role, registration_date):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.user_role = "Super Admin" if user_role == 0 else "System Admin" if user_role == 1 else "Service Engineer" if user_role == 2 else "Unknown Role"
        self.registration_date = registration_date

    def __repr__(self):
        return str(self.user_id)


class Traveller:
    def __init__(
        self, customer_id, first_name, last_name, date_of_birth, gender, street_name, house_number,
        zip_code, city, email_address, mobile_phone, driving_license_number, registration_date
    ):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = "Female" if gender == 1 else "Male"
        self.street_name = street_name
        self.house_number = house_number
        self.zip_code = zip_code
        self.city = city
        self.email_address = email_address
        self.mobile_phone = mobile_phone
        self.driving_license_number = driving_license_number
        self.registration_date = registration_date

    def __repr__(self):
        return str(self.customer_id)


class Scooter:
    def __init__(
        self, scooter_id, brand, model, serial_number, top_speed, battery_capacity, state_of_charge,
        target_range_soc_min, target_range_soc_max, latitude, longitude, out_of_service,
        mileage, last_maintenance_date, in_service_date
    ):
        self.scooter_id = scooter_id
        self.brand = brand
        self.model = model
        self.serial_number = serial_number
        self.top_speed = top_speed
        self.battery_capacity = battery_capacity
        self.state_of_charge = state_of_charge
        self.target_range_soc = f"{target_range_soc_min} - {target_range_soc_max}"
        self.latitude = f"{float(latitude):.5f}"
        self.longitude = f"{float(longitude):.5f}"
        self.out_of_service = "Yes" if out_of_service == 1 else "No"
        self.mileage = mileage
        self.last_maintenance_date = last_maintenance_date
        self.in_service_date = in_service_date
    
    def __repr__(self):
        return str(self.scooter_id)


class Log:
    def __init__(
        self, date, time, username, description, additional_info, suspicious
    ):
        self.date = date
        self.time = time
        self.username = username
        self.description = description
        self.additional_info = additional_info
        self.suspicious = "Yes" if suspicious == 1 else ("No" if suspicious == 0 else "-")

    def __repr__(self):
        return (f"date={self.date}, time={self.time}, "
                f"username={self.username}, description={self.description}, "
                f"additional_info={self.additional_info}, suspicious={self.suspicious})")

class RestoreCode:
    def __init__(self, code_id, generated_for_user_id, backup_filename, restore_code):
        self.code_id = code_id
        self.generated_for_user_id = generated_for_user_id
        self.backup_filename = backup_filename
        self.restore_code = restore_code

    def __repr__(self):
        return str(self.code_id)