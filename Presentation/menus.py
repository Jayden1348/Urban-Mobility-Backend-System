from .generaltools import *


def super_admin_menu():
    while True:
        print("Main Menu (Super Admin)\n")
        print("1. Option 1")
        print("2. Option 2")
        print("3. Log out")
        choice = input("\nSelect an option: ")

        if choice == "1":
            clear_screen()
            # Option1
        elif choice == "2":
            clear_screen()
            # Option1
        elif choice == "3":
            if areyousure("log out"):
                return
        else:
            print("\nInvalid option. Please try again.")
            wait(2)
            clear_screen()


def system_admin_menu():
    while True:
        print("Main Menu (System Admin)\n")
        print("1. Option 1")
        print("2. Option 2")
        print("3. Log out")
        choice = input("\nSelect an option: ")

        if choice == "1":
            clear_screen()
            # Option1
        elif choice == "2":
            clear_screen()
            # Option1
        elif choice == "3":
            if areyousure("log out"):
                return
        else:
            print("\nInvalid option. Please try again.")
            wait(2)
            clear_screen()


def service_engineer_menu():
    while True:
        print("Main Menu (System Engineer)\n")
        print("1. Option 1")
        print("2. Option 2")
        print("3. Log out")
        choice = input("\nSelect an option: ")

        if choice == "1":
            clear_screen()
            # Option1
        elif choice == "2":
            clear_screen()
            # Option1
        elif choice == "3":
            if areyousure("log out"):
                return
        else:
            print("\nInvalid option. Please try again.")
            wait(2)
            clear_screen()
