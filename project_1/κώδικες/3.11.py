aDict = dict(zip('abcdefghijklmnopqrstuvwxyz.!?()-ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                 ['00000', '00001', '00010', '00011', '00100',
                  '00101', '00110', '00111', '01000', '01001', '01010', '01011', '01100', '01101', '01110', '01111',
                  '10000', '10001', '10010', '10011', '10100', '10101', '10110', '10111', '11000', '11001',
                  '11010', '11011', '11100', '11101', '11110', '11111',
                  '00000', '00001', '00010', '00011', '00100', '00101', '00110', '00111', '01000', '01001',
                  '01010', '01011', '01100', '01101', '01110', '01111', '10000', '10001', '10010', '10011',
                  '10100', '10101', '10110', '10111', '11000', '11001']))

reverseDict = {v: k for k, v in aDict.items()}

# RC4 Key Scheduling Algorithm (KSA)
def ksa(key):
    key = [ord(c) for c in key]
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    return S

# RC4 Pseudo-Random Generation Algorithm (PRGA)
def prga(S, n):
    i = j = 0
    keystream = []
    for _ in range(n):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        keystream.append(S[(S[i] + S[j]) % 256])
    return keystream

# Κωδικοποίηση μηνύματος σε δυαδικό
def text_to_binary(text):
    return ''.join(aDict[c] for c in text)

# Αποκωδικοποίηση δυαδικού σε κείμενο
def binary_to_text(binary):
    return ''.join(reverseDict[binary[i:i+5]] for i in range(0, len(binary), 5))

# XOR δυαδικών strings
def xor(bin_str, keystream):
    return ''.join(str(int(b)^int(k)) for b, k in zip(bin_str, keystream))

# Μετατροπή keystream byte σε 8-bit δυαδικό
def keystream_to_binary(keystream, length):
    bits = ''.join(f'{byte:08b}' for byte in keystream)
    return bits[:length]  # κόβουμε για να ταιριάζει

# Μήνυμα
plaintext = "MISTAKESAREASSERIOUSASTHERESULTSTHEYCAUSE"

#Μετατροπή σε binary
binary_msg = text_to_binary(plaintext)

#Δημιουργία keystream
key = "HOUSE"
S = ksa(key)
ks = prga(S, (len(binary_msg) + 7) // 8)  # υπολογισμός byte-length
ks_binary = keystream_to_binary(ks, len(binary_msg))

#Κρυπτογράφηση
cipher_binary = xor(binary_msg, ks_binary)

#Αποκρυπτογράφηση (XOR πάλι)
decrypted_binary = xor(cipher_binary, ks_binary)

#Επιστροφή σε αρχικό μήνυμα
decrypted_text = binary_to_text(decrypted_binary)

print("Original:   ", plaintext)
print("Encrypted:  ", cipher_binary)
print("Decrypted:  ", decrypted_text)
