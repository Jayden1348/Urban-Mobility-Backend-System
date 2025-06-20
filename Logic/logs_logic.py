from Access import DataAccess
from datetime import datetime


def get_all_logs():
    return DataAccess.get_all_from_table("Logs")


def new_log(username, description, additionalinfo, suspicious):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    suspicious_int = 1 if suspicious else 0

    DataAccess.add_item_to_table("Logs", {
        "Date": date_str,
        "Time": time_str,
        "Username": username,
        "Description": description,
        "AdditionalInfo": additionalinfo,
        "Suspicious": suspicious_int
    })
