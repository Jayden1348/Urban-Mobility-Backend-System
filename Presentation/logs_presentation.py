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
        log_id = log.log_id
        date = log.date
        time = log.time
        username = log.username
        description = log.description
        additionalinfo = log.additional_info
        suspicious = log.suspicious
        print(
            f"{str(log_id):<4} {str(date):<12} {str(time):<10} {str(username or '-'): <15} {str(description)[:28]:<30} {str(additionalinfo)[:23]:<25} {suspicious:<10}"
        )

    input("\nPress Enter to return...")
    clear_screen()
