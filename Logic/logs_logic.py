from Access import LogAccess
from datetime import datetime
from Models.DataModels import Log


def get_all_logs():
    logs = []
    try:
        for row in LogAccess.read_encrypted_logs_csv():
            log = Log(int(row[0]), row[1], row[2],
                      row[3], row[4], row[5], int(row[6]))
            logs.append(log)
        return logs
    except Exception as e:
        return e


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
