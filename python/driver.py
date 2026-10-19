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

        #Spawn encryptor process with piped stdin and stdout
        self.cipher_proc = subprocess.Popen(
            [sys.executable, "encryptor.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            encoding="utf8"
        )

        # Log startup per instructions
        self.log_event("START", "Logging Started.")

    def log_event(self, action, message=""):
        line = f"{action} {message}".strip()
        self.logger_proc.stdin.write(line + "\n")
        self.logger_proc.stdin.flush()

    def send_cipher_cmd(self, command_line):
            self.cipher_proc.stdin.write(command_line.strip() + "\n")
            self.cipher_proc.stdin.flush()
            return self.cipher_proc.stdout.readline().strip()

    def shutdown(self):
        self.log_event("STOP", "Driver stopped.")
        self.cipher_proc.stdin.write("QUIT\n")
        self.cipher_proc.stdin.flush()
        self.logger_proc.stdin.write("QUIT\n")
        self.logger_proc.stdin.flush()

        self.cipher_proc.wait()
        self.logger_proc.wait()


def main():
    log_file = sys.argv[1]
    driver = Driver(log_file)

    while True:
        print("\nCommands: password | encrypt | decrypt | history | quit")
        cmd = input("Enter command: ").strip().lower()

        if cmd == "quit":
            break
        elif cmd == "password":
            p = input("Input: ").strip()
            resp = driver.send_cipher_cmd(f"PASS {p}")
            print("Output: " + resp)
        elif cmd == "encrypt":
            text = input("Input: ").strip()
            resp = driver.send_cipher_cmd(f"ENCRYPT {text}")
            print(resp)

        elif cmd == "decrypt":
            text = input("Input: ").strip()
            resp = driver.send_cipher_cmd(f"DECRYPT {text}")
            print("Output: " + resp)

        elif cmd == "history":
            print("Not yet implemented.")
        else:
            print(f"Unknown command '{cmd}'.")

    driver.shutdown()
    print("Driver shut down.")

if __name__ == "__main__":
    main()