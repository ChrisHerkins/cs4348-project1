import sys
from datetime import datetime

def main():
    log_file = sys.argv[1]

    with open(log_file, "a", encoding="utf8") as f:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            if line.lower() == "quit":
                break

            # Split only on first space: first word is action, rest is message
            parts = line.split(" ", 1)
            action = parts[0]
            message = parts[1] if len(parts) > 1 else ""

            # Required format: YYYY-MM-DD HH:MM [ACTION] MESSAGE
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            entry = f"{now} [{action}] {message}".strip()

            f.write(entry + "\n")
            f.flush()  # Force write to disk so entries appear immediately

if __name__ == "__main__":
    main()