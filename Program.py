from Logic.loginlogic import validate_login


def main_menu():
    while True:
        print("\nMain Menu")
        print("1. Option 1")
        print("2. Option 2")
        print("3. Option 3")
        choice = input("Select an option (1-3): ")

        if choice == "1":
            print("1")
        elif choice == "2":
            username = input("Username: ")
            password = input("Password: ")
            if not validate_login(username, password):
                print("wrong")
            else:
                print("right")
        elif choice == "3":
            print("3")
        else:
            print("Invalid option. Please try again.")


def start():
    username = input("Username: ")
    password = input("Password: ")


if __name__ == "__main__":
    main_menu()
