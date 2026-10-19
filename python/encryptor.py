import sys

def vigenere(text, key, decrypt=False):
    result = []
    text = text.upper()
    key = key.upper()
    k_len = len(key)

    for i, char in enumerate(text):
        if 'A' <= char <= 'Z':
            shift = ord(key[i % k_len]) - ord('A')
            if decrypt:
                shift = -shift
            new_code = (ord(char) - ord('A') + shift) % 26 + ord('A')
            result.append(chr(new_code))
        else:
            result.append(char)

    return "".join(result)

def main():
    passkey = None

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        if line.lower() == "quit":
            break

        parts = line.split(" ", 1)
        cmd = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if cmd == "pass":
            if not arg:
                print("ERROR No password provided")
            else:
                passkey = arg.upper()
                print("RESULT")
        elif cmd == "encrypt":
            if not passkey:
                print("ERROR No password set")
            else:
                ciphertext = vigenere(arg, passkey, decrypt=False)
                print("RESULT " + ciphertext)
        elif cmd == "decrypt":
            if not passkey:
                print("ERROR No password set")
            else:
                plaintext = vigenere(arg, passkey, decrypt=True)
                print("RESULT " + plaintext)
        else:
            print("ERROR Unknown command " + cmd)
        sys.stdout.flush()

if __name__ == "__main__":
    main()