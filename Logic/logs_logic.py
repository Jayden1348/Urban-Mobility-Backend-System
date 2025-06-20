from Access import LogAccess
from datetime import datetime
from Models.DataModels import Log


def get_all_logs():
    logs = []
    for row in LogAccess.read_encrypted_logs_csv():
        # Skip empty or malformed rows
        if not row or not row[0].isdigit():
            continue
        log = Log(
            LogID=int(row[0]),
            Date=row[1],
            Time=row[2],
            Username=row[3],
            Description=row[4],
            AdditionalInfo=row[5],
            Suspicious=int(row[6])
        )
        logs.append(log)
    return logs


def get_next_log_id():
    logs = list(LogAccess.read_encrypted_logs_csv())
    if not logs:
        return 1
    last_log = logs[-1]
    try:
        return int(last_log[0]) + 1
    except (IndexError, ValueError):
        return 1


def new_log(username, description, additionalinfo, suspicious):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    log_id = get_next_log_id()
    log_row = [log_id, date_str, time_str, username,
               description, additionalinfo, suspicious]
    LogAccess.write_encrypted_log_csv(log_row)
