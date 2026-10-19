import sys

def main():
    log_file = sys.argv[1]

    with open(log_file, "a", encoding="utf8") as f:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            if line.lower() == "quit":
                break

            f.write("LOG: " + line + "\n")

if __name__ == "__main__":
    main()