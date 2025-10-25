from Access import LogAccess
from datetime import datetime
from Models.DataModels import Log


def get_log(filters):
    logs = []
    for row in LogAccess.read_encrypted_logs_csv():
        log = Log(row[0], row[1],
                  row[2], row[3], row[4], int(row[5]) if row[5].isdigit() else "-")
        logs.append(log)
    if filters:
        for key, value in filters.items():
            logs = [log for log in logs if getattr(log, key) == value]
    return logs


def new_log(username, description, additionalinfo, suspicious=0):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    log_row = [date_str, time_str, username,
               description, additionalinfo, suspicious]
    LogAccess.write_encrypted_log_csv(log_row)
