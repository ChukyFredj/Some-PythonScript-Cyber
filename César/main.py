def code_cesar(text, shift):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet + alphabet.upper(), shifted_alphabet + shifted_alphabet.upper())
    return text.translate(table)

def decode_cesar(text, shift):
    return code_cesar(text, -shift)

def main():
    text = "Hello, World!"
    shift = 3
    coded = code_cesar(text, shift)
    print(coded)
    decoded = decode_cesar(coded, shift)
    print(decoded)

if __name__ == "__main__":
    main()