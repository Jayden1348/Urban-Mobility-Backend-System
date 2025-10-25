from datetime import datetime, date
from Models.DataModels import Scooter, User, Traveller
from Logic import scooter_logic, user_logic, traveller_logic, logs_logic, backup_logic


# Date functions
def get_today_date():
    return date.today().strftime("%Y-%m-%d")


def validate_date_format(date_str):
    if date_str in ("t", "today", "now"):
        return True, get_today_date()
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        if date_obj.date() <= date.today():
            return True, date_obj.strftime("%Y-%m-%d")
        else:
            return False, "Date cannot be in the future"
    except ValueError:
        return False, "Wrong date format. Please use YYYY-MM-DD."
    

def check_is_digit_valid(entered, min_val, max_val):
    if entered.isdigit():
        num = int(entered)
        if min_val <= num <= max_val:
            return True
    return False


def validate_char_string(input_string, letters, numbers, others=''):
    if not input_string:
        return False
    
    for char in input_string:
        if char.isalpha():
            if not letters:
                return False
        elif char.isdigit():
            if not numbers:
                return False
        else:
            if char not in others:
                return False
    
    return True


# Object functions
def get_class(object_type):
    classes = {
        'scooter': Scooter,
        'user': User,
        'traveller': Traveller,
    }
    return classes[object_type]


def get_logic_files(object_type):
    logic_files = {
        'scooter': scooter_logic,
        'user': user_logic,
        'traveller': traveller_logic,
        'log': logs_logic,
        'restore code': backup_logic,
        'backup file': backup_logic,
    }
    return logic_files.get(object_type)



