from .general_presentation import *
from Presentation.users_presentation import display_user_fields

columns = ["date", "time", "username",
           "description", "additional_info", "suspicious"]


def show_all_logs():
    display_objects_table(columns, "log", selection=False, only_display=True)


def show_user_logs():
    search_user = display_objects_table(
        display_user_fields, "user", selection=True)
    if search_user is None:
        return
    display_objects_table(columns, "log", selection=False, only_display=True, filters={"username": search_user.username})


def show_sus_logs():
    display_objects_table(columns, "log", selection=False, only_display=True, filters={"suspicious":"Yes"})