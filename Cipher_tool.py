import sys

# Supported alphabets
ENGLISH_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
GREEK_ALPHABET = 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'

def get_alphabet(choice):
    if choice == '1':
        return ENGLISH_ALPHABET
    elif choice == '2':
        return GREEK_ALPHABET
    else:
        return None

def caesar_cipher(text, key, alphabet):
    result = ''
    n = len(alphabet)
    for char in text:
        if char.upper() in alphabet:
            idx = alphabet.index(char.upper())
            new_idx = (idx + key) % n
            new_char = alphabet[new_idx]
            if char.islower():
                new_char = new_char.lower()
            result += new_char
        else:
            result += char
    return result

def vigenere_cipher(text, key, alphabet):
    result = ''
    n = len(alphabet)
    key_indices = [alphabet.index(k.upper()) for k in key if k.upper() in alphabet]
    if not key_indices:
        return None
    key_len = len(key_indices)
    j = 0
    for char in text:
        if char.upper() in alphabet:
            idx = alphabet.index(char.upper())
            shift = key_indices[j % key_len]
            new_idx = (idx + shift) % n
            new_char = alphabet[new_idx]
            if char.islower():
                new_char = new_char.lower()
            result += new_char
            j += 1
        else:
            result += char
    return result

def get_input(prompt, valid_options=None):
    while True:
        value = input(prompt)
        if valid_options:
            if value.lower() in valid_options:
                return value
            else:
                print(f"Please choose from {valid_options}.")
        else:
            if value.strip():
                return value
            else:
                print("Input cannot be empty.")

def main():
    while True:
        print("\n--- Cipher Tool ---")
        alphabet_choice = get_input("Choose alphabet (type '1' for english or '2' for greek): ", ['1', '2'])
        alphabet = get_alphabet(alphabet_choice)
        if not alphabet:
            print("Invalid alphabet choice.")
            continue
        
        while True:
            text = get_input("Enter the text to cipher: ")
            if text.isnumeric():
                print("Input cannot be only numbers.")
                continue
            # Check if all letters in text are in the chosen alphabet (ignore non-letters)
            letters_in_text = [c for c in text if c.isalpha()]
            if all(c.upper() in alphabet for c in letters_in_text):
                break
            else:
                print(f"Text must only contain letters from the chosen alphabet ({alphabet_choice}).")
        
        print("~ Available Algorithms ~")
        algo = get_input("1. Caesar\n2. Vigenere\nChoose an algorithm from the above (type the name or it's number): ", ['caesar', 'vigenere', '1', '2'])

        if algo == 'caesar' or algo == '1':
            while True:
                key_input = get_input(f"Enter key (integer 0-{len(alphabet)-1}): ")
                if key_input.isdigit() and 0 <= int(key_input) < len(alphabet):
                    key = int(key_input)
                    break
                else:
                    print("Invalid key.")
            ciphered = caesar_cipher(text, key, alphabet)
        elif algo == 'vigenere' or algo == '2':
            while True:
                key = get_input(f"Enter key (word using {alphabet_choice} letters): ")
                if all(k.upper() in alphabet for k in key):
                    break
                else:
                    print("Key must only contain letters from the chosen alphabet.")
            ciphered = vigenere_cipher(text, key, alphabet)
            if ciphered is None:
                print("Invalid key for Vigenere cipher.")
                continue

        print(f"\nCiphered text: {ciphered}")

        next_action = get_input("Type 'exit' to quit or 'continue' to start again: ", ['exit', 'continue'])
        if next_action == 'exit':
            print("Exiting program.")
            sys.exit()

if __name__ == "__main__":
    main()