import sys

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        if line.lower() == "quit":
            break

        parts = line.split(" ", 1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd in ["pass", "encrypt", "decrypt"]:
            print(f"Success {cmd} {arg}".strip())
        else:
            print("ERROR Unknown command " + cmd)

if __name__ == "__main__":
    main()