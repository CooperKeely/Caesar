import argparse
import string

ALPHABET = string.ascii_uppercase



def get_args():
    parser = argparse.ArgumentParser(
                            prog='Caesar',
                            description='Caesar Cipher Decryption Tool')

    parser.add_argument('-k', '--key', type=int,
                        help="Shift key (0-25) to apply for decryption")

    parser.add_argument('-b', '--bruteforce', action='store_true',
                        help="Try all possible shifts and print all 26 outputs")
    
    parser.add_argument('-i', '--input', type=str, default='-',
                        help='Ciphertext string use (\'-\' for stdin)')

    parser.add_argument('-f', '--file', type=argparse.FileType('r'),
                        help='File containing ciphertext (mutually exclusive with --input)')

    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default='-',
                        help='Write plaintext to this file (default: stdout)')
    
    return parser.parse_args()

def caesar_shift(text: str, shift: int) -> str:
    result = []
    for ch in text:
        if ch.upper() in ALPHABET:
            idx = ALPHABET.index(ch.upper())
            new_char = ALPHABET[(idx - shift) % 26]
            result.append(new_char if ch.isupper() else new_char.lower())
        else:
            result.append(ch)
    return ''.join(result)

def main():
    args = get_args()

    # read cipher text
    if args.file:
        ciphertext = args.file.read()
    elif args.input == '-':
        ciphertext = input("Ciphertext> ")
    else:
        ciphertext = args.input
        
    # decrypt
    outputs = []
    if args.bruteforce:
        for k in range(26):
            pt = caesar_shift(ciphertext, k)
            outputs.append((k, pt))

    else:
        key = args.key % 26
        outputs.append((key, caesar_shift(ciphertext, key)))

    for key, plaintext in outputs:
        header = f"Key = {key}:"
        if args.output == '-':
            print(header)
            print(plaintext)
            print()
        else:
            args.output.write(header + "\n")
            args.output.write(plaintext + "\n\n")

if __name__ == "__main__":
    main()
