import sys
import subprocess

class Driver:
    def __init__(self, log_file):
        self.log_file = log_file

        # Spawn logger process with piped stdin
        self.logger_proc = subprocess.Popen(
            [sys.executable, "logger.py", self.log_file],
            stdin=subprocess.PIPE,
            encoding="utf8"
        )

        # Log startup per instructions
        self.log_event("START", "Logging Started.")

    def log_event(self, action, message=""):
        line = f"{action} {message}".strip()
        self.logger_proc.stdin.write(line + "\n")
        self.logger_proc.stdin.flush()

    def shutdown(self):
        self.log_event("STOP", "Driver stopped.")
        self.logger_proc.stdin.write("QUIT\n")
        self.logger_proc.stdin.flush()
        self.logger_proc.wait()

def main():
    log_file = sys.argv[1]
    driver = Driver(log_file)

    while True:
        print("\nCommands: password | encrypt | decrypt | history | quit")
        cmd = input("Enter command: ").strip().lower()

        if cmd == "quit":
            break
        elif cmd in ["password", "encrypt", "decrypt", "history"]:
            print(f"Command '{cmd}' received (encryptor not connected yet).")
        else:
            print(f"Unknown command '{cmd}'.")

    driver.shutdown()
    print("Driver cleanly shut down.")

if __name__ == "__main__":
    main()