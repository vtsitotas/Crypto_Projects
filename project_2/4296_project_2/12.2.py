import base64
from fractions import Fraction
from math import isqrt

def rational_to_contfrac(x, y):
    contfrac = []
    while y:
        a = x // y
        contfrac.append(a)
        x, y = y, x - a * y
    return contfrac

def convergents_from_contfrac(frac):
    convs = []
    for i in range(len(frac)):
        convs.append(contfrac_to_rational(frac[:i+1]))
    return convs

def contfrac_to_rational(frac):
    num, denom = 1, 0
    for a in reversed(frac):
        num, denom = denom + a * num, num
    return (num, denom)

def is_perfect_square(n):
    h = n & 0xF
    if h > 9:
        return False
    if h in {2, 3, 5, 6, 7, 8}:
        return False
    t = isqrt(n)
    return t * t == n

def wiener_attack(e, N):
    frac = rational_to_contfrac(e, N)
    convs = convergents_from_contfrac(frac)
    for k, d in convs:
        if k == 0:
            continue
        # check if d is the private exponent
        phi_guess = (e * d - 1) // k
        s = N - phi_guess + 1
        discr = s*s - 4*N
        if discr >= 0 and is_perfect_square(discr):
            return d
    return None

def rsa_decrypt(c, d, N):
    return pow(c, d, N)

def decode_ascii_from_int(m):
    bytes_out = []
    while m > 0:
        bytes_out.append(m % 256)
        m //= 256
    return bytes(bytearray(reversed(bytes_out)))

# === PARAMETERS ===
N = 194749497518847283
e = 50736902528669041

# === STEP 1: GET d ===
d = wiener_attack(e, N)
if d is None:
    print("Wiener attack failed.")
    exit()

print(f"[+] Found d = {d}")

# === STEP 2: DECRYPT CIPHERTEXT ===
# Paste your base64-encoded ciphertext here:
b64_ciphertext = "Qz1bNDc0MDYyNjMxOTI2OTM1MDksNTEwNjUxNzgyMDExNzIyMjMsMzAyNjA1NjUyMzUxMjg3MDQsODIzODU5NjMzMzQ0MDQyNjgNCjgxNjkxNTY2NjM5Mjc5MjksNDc0MDYyNjMxOTI2OTM1MDksMTc4Mjc1OTc3MzM2Njk2NDQyLDEzNDQzNDI5NTg5NDgwMzgwNg0KMTEyMTExNTcxODM1NTEyMzA3LDExOTM5MTE1MTc2MTA1MDg4MiwzMDI2MDU2NTIzNTEyODcwNCw4MjM4NTk2MzMzNDQwNDI2OA0KMTM0NDM0Mjk1ODk0ODAzODA2LDQ3NDA2MjYzMTkyNjkzNTA5LDQ1ODE1MzIwOTcyNTYwMjAyLDE3NDYzMjIyOTMxMjA0MTI0OA0KMzAyNjA1NjUyMzUxMjg3MDQsNDc0MDYyNjMxOTI2OTM1MDksMTE5MzkxMTUxNzYxMDUwODgyLDU3MjA4MDc3NzY2NTg1MzA2DQoxMzQ0MzQyOTU4OTQ4MDM4MDYsNDc0MDYyNjMxOTI2OTM1MDksMTE5MzkxMTUxNzYxMDUwODgyLDQ3NDA2MjYzMTkyNjkzNTA5DQoxMTIxMTE1NzE4MzU1MTIzMDcsNTI4ODI4NTEwMjYwNzI1MDcsMTE5MzkxMTUxNzYxMDUwODgyLDU3MjA4MDc3NzY2NTg1MzA2DQoxMTkzOTExNTE3NjEwNTA4ODIsMTEyMTExNTcxODM1NTEyMzA3LDgxNjkxNTY2NjM5Mjc5MjksMTM0NDM0Mjk1ODk0ODAzODA2DQo1NzIwODA3Nzc2NjU4NTMwNiw0NzQwNjI2MzE5MjY5MzUwOSwxODU1ODIxMDUyNzUwNTA5MzIsMTc0NjMyMjI5MzEyMDQxMjQ4DQoxMzQ0MzQyOTU4OTQ4MDM4MDYsODIzODU5NjMzMzQ0MDQyNjgsMTcyNTY1Mzg2MzkzNDQzNjI0LDEwNjM1NjUwMTg5MzU0NjQwMQ0KODE2OTE1NjY2MzkyNzkyOSw0NzQwNjI2MzE5MjY5MzUwOSwxMDM2MTA1OTcyMDYxMDgxNiwxMzQ0MzQyOTU4OTQ4MDM4MDYNCjExOTM5MTE1MTc2MTA1MDg4MiwxNzI1NjUzODYzOTM0NDM2MjQsNDc0MDYyNjMxOTI2OTM1MDksODE2OTE1NjY2MzkyNzkyOQ0KNTI4ODI4NTEwMjYwNzI1MDcsMTE5MzkxMTUxNzYxMDUwODgyLDgxNjkxNTY2NjM5Mjc5MjksNDc0MDYyNjMxOTI2OTM1MDkNCjQ1ODE1MzIwOTcyNTYwMjAyLDE3NDYzMjIyOTMxMjA0MTI0OCwzMDI2MDU2NTIzNTEyODcwNCw0NzQwNjI2MzE5MjY5MzUwOQ0KNTI4ODI4NTEwMjYwNzI1MDcsMTE5MzkxMTUxNzYxMDUwODgyLDExMTUyMzQwODIxMjQ4MTg3OSwxMzQ0MzQyOTU4OTQ4MDM4MDYNCjQ3NDA2MjYzMTkyNjkzNTA5LDExMjExMTU3MTgzNTUxMjMwNyw1Mjg4Mjg1MTAyNjA3MjUwNywxMTkzOTExNTE3NjEwNTA4ODINCjU3MjA4MDc3NzY2NTg1MzA2LDExOTM5MTE1MTc2MTA1MDg4MiwxMTIxMTE1NzE4MzU1MTIzMDcsODE2OTE1NjY2MzkyNzkyOQ0KMTM0NDM0Mjk1ODk0ODAzODA2LDU3MjA4MDc3NzY2NTg1MzA2XQ=="
cipher_bytes = base64.b64decode(b64_ciphertext)

# Fix: decode as text, extract the list of integers
cipher_text = cipher_bytes.decode('utf-8')
import re
cipher_blocks = list(map(int, re.findall(r'\d+', cipher_text)))

# Decrypt each block
plaintext = b''
for c in cipher_blocks:
    m = rsa_decrypt(c, d, N)
    block = decode_ascii_from_int(m)
    plaintext += block

print("[+] Plaintext recovered:")
print(plaintext.decode('utf-8', errors='ignore'))
