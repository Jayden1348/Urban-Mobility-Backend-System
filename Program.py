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
            print("2")
        elif choice == "3":
            print("3")
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main_menu()
