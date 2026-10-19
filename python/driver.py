import sys

def main():
    log_file = sys.argv[1]
    print("Driver started. Log file:", log_file)

    while True:
        print("\nCommands: password | encrypt | decrypt | history | quit")
        cmd = input("Enter command: ").strip().lower()

        if cmd == "quit":
            print("Exiting driver.")
            break
        elif cmd in ["password", "encrypt", "decrypt", "history"]:
            print(f"Command '{cmd}' received.")
        else:
            print(f"Unknown command '{cmd}'.")

if __name__ == "__main__":
    main()