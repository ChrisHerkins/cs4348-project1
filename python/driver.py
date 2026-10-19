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
        self.history = []

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
    def is_valid_letters(self, text):
        return len(text) > 0 and text.isalpha()

    def get_user_string(self, prompt_label):
        print(f"\nSelect input source for {prompt_label}:")
        print("1. Enter a new string")
        print("2. Choose from history")
        choice = input("Enter choice (1-2): ").strip()

        if choice == "2":
            if len(self.history) == 0:
                print("History is currently empty. Please enter a new string.")
            else:
                print("\n--- History ---")
                for idx, item in enumerate(self.history, 1):
                    print(f"{idx}. {item}")
                print("0. Cancel and enter a new string")

                sub_choice = input(f"Select item (0-{len(self.history)}): ").strip()
                if sub_choice.isdigit():
                    selected_idx = int(sub_choice)
                    if 1 <= selected_idx <= len(self.history):
                        return self.history[selected_idx - 1]
                    elif selected_idx == 0:
                        print("Cancelled history selection.")
                    else:
                        print("Invalid selection number.")
                else:
                    print("Invalid input.")

        # Fallback to entering a new string
        val = input(f"Enter {prompt_label} (letters only): ").strip()
        if not self.is_valid_letters(val):
            print("Error: Input must contain letters only (no spaces, numbers, or symbols).")
            return None
        return val.upper()



def main():
    if len(sys.argv) < 2:
        print("Not a valid logging file. Try again.")
        sys.exit(1)
    log_file = sys.argv[1]
    driver = Driver(log_file)

    while True:
        print("\nCommands: password | encrypt | decrypt | history | quit")
        cmd = input("Enter command: ").strip().lower()

        if cmd == "quit":
            driver.log_event("COMMAND", "quit")
            break

        elif cmd == "password":
            driver.log_event("COMMAND", "password")
            pwd = driver.get_user_string("password")
            if pwd:
                resp = driver.send_cipher_cmd(f"PASS {pwd}")
                print("Output: " + resp)
                if resp.startswith("RESULT"):
                    # Privacy rule: NEVER log the actual password!
                    driver.log_event("RESULT", "Password set successfully.")
                else:
                    driver.log_event("ERROR", resp)
            else:
                driver.log_event("ERROR", "Invalid password input")

        elif cmd == "encrypt":
            driver.log_event("COMMAND", "encrypt")
            text = driver.get_user_string("string to encrypt")
            if text:
                driver.log_event("INPUT", f"Encrypting: {text}")
                resp = driver.send_cipher_cmd(f"ENCRYPT {text}")
                driver.log_event("RESULT", resp)
                print("Output: " + resp)
                if resp.startswith("RESULT"):
                    parts = resp.split(" ", 1)
                    cipher_res = parts[1] if len(parts) > 1 else ""
                    if text not in driver.history:
                        driver.history.append(text)
                    if cipher_res and cipher_res not in driver.history:
                        driver.history.append(cipher_res)
            else:
                driver.log_event("ERROR", "Invalid encryption input string")
                        

        elif cmd == "decrypt":
            driver.log_event("COMMAND", "decrypt")
            text = driver.get_user_string("string to decrypt")
            if text:
                driver.log_event("INPUT", f"Decrypting: {text}")
                resp = driver.send_cipher_cmd(f"DECRYPT {text}")
                driver.log_event("RESULT", resp)
                print("Output: " + resp)
                if resp.startswith("RESULT"):
                    parts = resp.split(" ", 1)
                    plain_res = parts[1] if len(parts) > 1 else ""
                    if text not in driver.history:
                        driver.history.append(text)
                    if plain_res and plain_res not in driver.history:
                        driver.history.append(plain_res)
            else:
                driver.log_event("ERROR", "Invalid decryption input string")

        elif cmd == "history":
            driver.log_event("COMMAND", "history")
            print("\n--- Current Session History ---")
            if len(driver.history) == 0:
                print("(History is empty)")
            else:
                for idx, item in enumerate(driver.history, 1):
                    print(f"{idx}. {item}")
            print("-------------------------------")
            driver.log_event("RESULT", f"Displayed history with {len(driver.history)} items.")
        
        else:
            print(f"Unknown command '{cmd}'.")

    driver.shutdown()
    print("Driver shut down.")

if __name__ == "__main__":
    main()