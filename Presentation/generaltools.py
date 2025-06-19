import os
import time


def clear_screen():
    os.system('cls')
    print("\n")


def wait(waittime):
    time.sleep(waittime)


def areyousure(message):
    while True:
        clear_screen()
        choice = input(
            f"Are you sure you want to {message}? (y/n): ").strip().lower()
        if choice in ("y", "yes"):
            clear_screen()
            return True
        elif choice in ("n", "no"):
            clear_screen()
            return False
        else:
            print("\nPlease enter 'y' or 'n'.")
            time.sleep(2)
