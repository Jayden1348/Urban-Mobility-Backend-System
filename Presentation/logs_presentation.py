from .general_presentation import *

columns = ["date", "time", "username",
           "description", "additional_info", "suspicious"]


def show_all_logs():  # Done
    display_objects_table(columns, "log", selection=False, only_display=True)


# Maybe red line when suspicious
