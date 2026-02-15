import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import numpy as np


def hamming_distance(a, b):
    return sum(bin(byte_a ^ byte_b).count('1') for byte_a, byte_b in zip(a, b))


# Παράμετροι
key = os.urandom(16)  # 128-bit κλειδί
iv = os.urandom(16)  # IV για CBC
num_pairs = 30
msg_length = 32  # 256 bits (2 blocks)

# Αποθήκευση αποτελεσμάτων
ecb_distances = []
cbc_distances = []

for _ in range(num_pairs):
    # Δημιουργία τυχαίου μηνύματος m1
    m1 = os.urandom(msg_length)

    # Δημιουργία m2 που διαφέρει σε 1 bit από το m1
    flip_pos = np.random.randint(0, msg_length * 8)  # Θέση bit για αλλαγή
    flip_byte = flip_pos // 8
    flip_bit = flip_pos % 8
    m2 = bytearray(m1)
    m2[flip_byte] ^= (1 << flip_bit)
    m2 = bytes(m2)

    # Κρυπτογράφηση ECB
    cipher_ecb = AES.new(key, AES.MODE_ECB)
    c1_ecb = cipher_ecb.encrypt(pad(m1, AES.block_size))
    c2_ecb = cipher_ecb.encrypt(pad(m2, AES.block_size))
    ecb_dist = hamming_distance(c1_ecb, c2_ecb)
    ecb_distances.append(ecb_dist)

    # Κρυπτογράφηση CBC
    cipher_cbc = AES.new(key, AES.MODE_CBC, iv)
    c1_cbc = cipher_cbc.encrypt(pad(m1, AES.block_size))
    cipher_cbc = AES.new(key, AES.MODE_CBC, iv)
    c2_cbc = cipher_cbc.encrypt(pad(m2, AES.block_size))
    cbc_dist = hamming_distance(c1_cbc, c2_cbc)
    cbc_distances.append(cbc_dist)

# Στατιστικά
print("ECB Mode:")
print(f"Μέση διαφορά bits: {np.mean(ecb_distances):.2f}")
print(f"Ελάχιστη διαφορά: {min(ecb_distances)}")
print(f"Μέγιστη διαφορά: {max(ecb_distances)}")
print(f"Τυπική απόκλιση: {np.std(ecb_distances):.2f}")

print("\nCBC Mode:")
print(f"Μέση διαφορά bits: {np.mean(cbc_distances):.2f}")
print(f"Ελάχιστη διαφορά: {min(cbc_distances)}")
print(f"Μέγιστη διαφορά: {max(cbc_distances)}")
print(f"Τυπική απόκλιση: {np.std(cbc_distances):.2f}")  