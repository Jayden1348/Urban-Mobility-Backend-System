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
    print(f"{'ID':<4} {'Date':<12} {'Time':<10} {'Username':<15} {'Description':<30} {'AdditionalInfo':<25} {'Suspicious':<10}")
    print("-" * 120)
    for log in logs:
        log_id = getattr(log, "LogID", getattr(log, "logid", ""))
        date = getattr(log, "Date", getattr(log, "date", ""))
        time = getattr(log, "Time", getattr(log, "time", ""))
        username = getattr(log, "Username", getattr(log, "username", ""))
        description = getattr(log, "Description",
                              getattr(log, "description", ""))
        additionalinfo = getattr(log, "AdditionalInfo",
                                 getattr(log, "additionalinfo", ""))
        suspicious = getattr(log, "Suspicious", getattr(log, "suspicious", 0))
        suspicious_str = "Yes" if suspicious else "No"
        print(
            f"{str(log_id):<4} {str(date):<12} {str(time):<10} {str(username or '-'): <15} {str(description)[:28]:<30} {str(additionalinfo)[:23]:<25} {suspicious_str:<10}"
        )

    input("\nPress Enter to return...")
    clear_screen()
