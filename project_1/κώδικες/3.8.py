from collections import deque
from itertools import product

# Λεξικό χαρακτήρων σε δυαδικά
aDict = dict(zip('abcdefghijklmnopqrstuvwxyz.!?()-ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                 ['00000', '00001', '00010', '00011', '00100',
                  '00101', '00110', '00111', '01000', '01001', '01010', '01011', '01100', '01101', '01110', '01111',
                  '10000', '10001', '10010', '10011', '10100', '10101', '10110', '10111', '11000', '11001',
                  '11010', '11011', '11100', '11101', '11110', '11111',
                  '00000', '00001', '00010', '00011', '00100', '00101', '00110', '00111', '01000', '01001',
                  '01010', '01011', '01100', '01101', '01110', '01111', '10000', '10001', '10010', '10011',
                  '10100', '10101', '10110', '10111', '11000', '11001']))

# Μετατροπή λίστας σε συμβολοσειρά
def list_to_string(l):
    return ''.join(str(e) for e in l)

# XOR δυο δυαδικών συμβολοσειρών
def string_xor(btext, key):
    if len(btext) != len(key):
        print("Το κλειδί και το μήνυμα πρέπει να έχουν το ίδιο μήκος!")
        return ''
    return ''.join(str(int(btext[i]) ^ int(key[i])) for i in range(len(btext)))

# Κείμενο -> δυαδικό
def text_enc(text):
    text = text.lower()
    return ''.join(aDict[ch] for ch in text if ch in aDict)

# Δυαδικό -> κείμενο
def text_dec(binary_string):
    inv_map = {v: k for k, v in aDict.items()}
    decoded = ''
    for i in range(0, len(binary_string), 5):
        chunk = binary_string[i:i + 5]
        if chunk in inv_map:
            decoded += inv_map[chunk]
        else:
            decoded += '?'
    return decoded

# XOR όλων των τιμών μιας λίστας
def sumxor(l):
    r = 0
    for v in l:
        r ^= v
    return r

# Παράγει δυαδικό ρεύμα από seed με LFSR
def lfsr(seed, feedback, bits, flag=1):
    seed = deque(seed)
    output = []
    for _ in range(bits):
        output.append(seed[0])
        feedback_bit = sumxor([seed[i] for i in feedback])
        seed.popleft()
        seed.append(feedback_bit)
    return output

# Βρίσκει το σωστό seed με βάση plaintext και ciphertext
def find_seed(plaintext, ciphertext, feedback, aDict):
    binary_plaintext = text_enc(plaintext)
    binary_ciphertext = text_enc(ciphertext)
    expected_keystream = string_xor(binary_plaintext, binary_ciphertext)
    expected_keystream_bits = [int(b) for b in expected_keystream]

    print(f"Δυαδικό plaintext '{plaintext}': {binary_plaintext}")
    print(f"Δυαδικό ciphertext '{ciphertext}': {binary_ciphertext}")
    print(f"Αναμενόμενο keystream: {expected_keystream_bits}")

    for candidate in product([0, 1], repeat=10):
        seed = list(candidate)
        print(f"Δοκιμή seed: {candidate}")
        generated_keystream = lfsr(seed, feedback, len(expected_keystream_bits))
        print(f"Keystream από το seed: {generated_keystream}")

        if generated_keystream == expected_keystream_bits:
            print(f"✅ Βρέθηκε σωστό seed: {seed}")
            return seed

    print("❌ Δεν βρέθηκε σωστό seed.")
    return None

# Κύρια ρουτίνα
def main():
    message = "i!))aiszwykqnfcyc!?secnncvch"
    message = message.lower()
    binary_message = text_enc(message)

    plaintext = "ab"
    ciphertext = "sq"

    feedback_taps = [0, 4, 6, 7]

    seed = find_seed(plaintext, ciphertext, feedback_taps, aDict)

    if seed is None:
        print("Δεν βρέθηκε έγκυρο seed. Τερματισμός...")
        return

    key_bits = lfsr(seed, feedback_taps, len(binary_message))
    key = ''.join(str(b) for b in key_bits)

    decrypted_binary = string_xor(binary_message, key)
    decrypted_text = text_dec(decrypted_binary)

    print("Αρχικό Κρυπτογραφημένο Μήνυμα:", message)
    print("Αποκωδικοποιημένο Μήνυμα:", decrypted_text)

if __name__ == "__main__":
    main()
