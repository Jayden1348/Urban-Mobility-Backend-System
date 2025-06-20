from .generaltools import *
from Logic import logs_logic


def show_all_logs():
    clear_screen()
    logs = logs_logic.get_all_logs()
    if not logs:
        print("No logs found.")
        wait(2)
        return

    print("All Logs:\n")
    print(f"{'ID':<4} {'Date':<12} {'Time':<10} {'Username':<15} {'Description':<30} {'Suspicious':<10}")
    print("-" * 90)
    for log in logs:
        log_id = log.logid if hasattr(
            log, "logid") else getattr(log, "LogID", "")
        date = log.date if hasattr(log, "date") else getattr(log, "Date", "")
        time = log.time if hasattr(log, "time") else getattr(log, "Time", "")
        username = log.username if hasattr(
            log, "username") else getattr(log, "Username", "")
        description = log.description if hasattr(
            log, "description") else getattr(log, "Description", "")
        suspicious = log.suspicious if hasattr(
            log, "suspicious") else getattr(log, "Suspicious", 0)
        suspicious_str = "Yes" if suspicious else "No"
        print(
            f"{log_id:<4} {date:<12} {time:<10} {username or '-':<15} {description[:28]:<30} {suspicious_str:<10}")

    input("\nPress Enter to return...")
    clear_screen()
