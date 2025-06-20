import os
import time


def clear_screen():
    os.system('cls')
    print("\n")


def wait(waittime):
    time.sleep(waittime)


def areyousure(message, added_info=""):
    while True:
        clear_screen()
        choice = input(
            f"{added_info}Are you sure you want to {message}? (y/n): ").strip().lower()
        if choice in ("y", "yes"):
            clear_screen()
            return True
        elif choice in ("n", "no"):
            clear_screen()
            return False
        else:
            print("\nPlease enter 'y' or 'n'.")
            time.sleep(2)


def areyousure_custommessage(message):
    while True:
        clear_screen()
        choice = input(message).strip().lower()
        if choice in ("y", "yes"):
            return True
        elif choice in ("n", "no"):
            return False
        else:
            print("\nPlease enter 'y' or 'n'.")
            time.sleep(2)
