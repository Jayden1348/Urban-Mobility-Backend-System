from Access import DataAccess


def get_all_logs():
    return DataAccess.get_all_from_table("Logs")
