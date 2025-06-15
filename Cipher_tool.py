import sys
import random
from math import gcd

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

# Encryption algorithms
def caesar_cipher(text, key, alphabet):
    result = ''
    n = len(alphabet)

    # C = (P + K) % n - Fixed shift
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

    # C = (P + K) % n - Repeating key
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

def affine_cipher(text, keya, keyb, alphabet):
    n = len(alphabet)
    a = int(keya)
    if gcd(a, n) != 1:
        print(f"\n⚠️  Key 'a' must be coprime with alphabet length (Z={n})!\n")
        return None
    b = int(keyb)
    if not a or not b:
        return None
    
    # C = (a*P + b) % n
    return ''.join([
        alphabet[
            ((a * alphabet.index(char.upper()) + b) % n)].lower() if char.islower() 
            else alphabet[((a * alphabet.index(char.upper()) + b) % n)]
        if char.upper() in alphabet else char
        for char in text
    ])

def otp_cipher(text, key, alphabet):
    result = ''
    n = len(alphabet)
    key_indices = [alphabet.index(k.upper()) for k in key if k.upper() in alphabet]
    if not key_indices:
        return None
    j = 0

    # C = (P ⊕ K) % n
    # Simulated OTP for Z26 or Z24 using XOR on indices
    for char in text:
        if char.upper() in alphabet:
            idx = alphabet.index(char.upper())
            shift = key_indices[j]
            new_idx = (idx ^ shift) % n  # XOR 
            new_char = alphabet[new_idx]
            if char.islower():
                new_char = new_char.lower()
            result += new_char
            j += 1
        else:
            result += char
    return result


def get_input(prompt, valid_options=None, program_end=False):
    while True:
        value = input(prompt)
        if valid_options:
            if value.lower() in valid_options:
                return value
            else:
                print(f"\n⚠️  Please choose from {valid_options}!\n")
        else:
            if value.strip():
                return value
            else:
                if not program_end:
                    print("\n⚠️  Input cannot be empty!\n")
                else:
                    return

def main():
    while True:
        print("\n--- Cipher Tool ---")
        alphabet_choice = get_input("Choose alphabet (type '1' for english or '2' for greek): ", ['1', '2'])
        alphabet = get_alphabet(alphabet_choice)
        if not alphabet:
            print("\n⚠️  Invalid alphabet choice!\n")
            continue        
        while True:
            text = get_input("Enter the text to cipher: ")
            if text.isnumeric():
                print("\n⚠️  Input cannot be only numbers!\n")
                continue
            letters_in_text = [c for c in text if c.isalpha()]
            if all(c.upper() in alphabet for c in letters_in_text):
                break
            else:
                print(f"\n⚠️  Text must only contain letters from the chosen alphabet ({'[English]' if alphabet_choice == '1' else '[Greek]'})!\n")
        
        print("\n~ Available Algorithms ~\n")
        print("1. Caesar: Shifts each letter by a fixed number of positions in the alphabet.\nKey is a single integer.")
        print("2. Vigenere: Shifts each letter by a value based on a repeating keyword.\nKey is a word using only letters from the chosen alphabet.")
        print("3. Affine: Applies a mathematical transformation to each letter using two keys (a, b).\nKeys are words using only letters from the chosen alphabet.")
        print("4. Vernam/OTP: Each letter is shifted by a value based on a one-time pad key of the same length as the text.\nKey must be the same length as the text and use only letters from the chosen alphabet.\n")

        algo = get_input("Choose an algorithm from the above (type the name or it's number): ", ['caesar', 'vigenere', 'affine', 'verman', 'otp', 'verman/otp', '1', '2', '3', '4'])

        if algo == 'caesar' or algo == '1':
            while True:
                key_input = get_input(f"Enter key (integer 0-{len(alphabet)-1}): ")
                if key_input.isdigit() and 0 <= int(key_input) < len(alphabet):
                    key = int(key_input)
                    break
                else:
                    print("\n⚠️  Invalid key!\n")
            ciphered = caesar_cipher(text, key, alphabet)
        elif algo == 'vigenere' or algo == '2':
            while True:
                key = get_input(f"Enter key (word using {'[English]' if alphabet_choice == '1' else '[Greek]'} letters): ")
                if all(k.upper() in alphabet for k in key if k.isalpha()):
                    break
                else:
                    print("\n⚠️  Key must only contain letters from the chosen alphabet!\n")
            ciphered = vigenere_cipher(text, key, alphabet)
            if ciphered is None:
                print("\n⚠️  Invalid key for Vigenere cipher!\n")
                continue
        elif algo == 'affine' or algo == '3':
            while True:
                keya = get_input(f"Enter key 'a' (a number): ")
                keyb = get_input(f"And enter key 'b' (a number): ")
                if keya.isnumeric() and keyb.isnumeric():
                    break
                else:
                    print("\n⚠️  Keys must only contain a number!\n")
            ciphered = affine_cipher(text, keya, keyb, alphabet)
            if ciphered is None:
                print("\n⚠️  Invalid key for Affine cipher!\n")
                continue
        elif algo == '4' or algo == 'otp' or algo == 'verman' or algo == 'verman/otp':
            while True:
                print("Generating Random Key...")
                while True:
                    key = ''.join(random.choice(alphabet) if c.isalpha() else c for c in text)
                    if key:
                        print(f"Key generated: {key}")
                        satisfied = get_input("Are you satisfied with the generated key? (y/n): ", ['y', 'Y', 'n', 'N'])
                        if satisfied.lower() == 'y':
                            break
                        else:
                            print("")
                            continue
                    else:
                        print("❌  Something went wrong generating the key!")
                if all(k.upper() in alphabet for k in key if k.isalpha()):
                    letters_in_text = [c for c in text if c.isalpha()]
                    if len(key) >= len(letters_in_text):
                        break
                    else:
                        print("\n⚠️  Key must be the same size as the text or longer!\n")
                else:
                    print("\n⚠️  Key must only contain letters from the chosen alphabet!\n")
            ciphered = otp_cipher(text, key, alphabet)
            if ciphered is None:
                print("\n⚠️  Invalid key for Verman/OTP cipher!\n")
                continue
        print(f"\nCiphered text for Z{len(alphabet)}{'[English]' if alphabet_choice == '1' else '[Greek]'} alphabet: {ciphered}")
        print(f"\nKey used: {key if 'key' in locals() else (keya + ', ' + keyb if 'keya' in locals() and 'keyb' in locals() else '')}")
        print(f"Plaintext: {text}\n")

        next_action = get_input("➡️  Type 'exit' to quit or press any key to start again: ", None, True)
        if next_action == 'exit' or next_action == 'EXIT':
            print("Exiting program...")
            sys.exit()
        key = ''
        keya = keyb = ''

if __name__ == "__main__":
    main()