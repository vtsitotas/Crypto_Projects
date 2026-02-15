import random

def cyclic_left_shift(x, shift, bits=16):
    shift %= bits
    return ((x << shift) | (x >> (bits - shift))) & 0xFFFF

def encode(m):
    return m ^ cyclic_left_shift(m, 6) ^ cyclic_left_shift(m, 10)

def decode(c):
    m = 0
    for _ in range(16):  # Αρκούν 16 επαναλήψεις για σύγκλιση
        m = c ^ cyclic_left_shift(m, 6) ^ cyclic_left_shift(m, 10)
    return m

# Δημιουργία τυχαίου 16-bit μηνύματος

m_original = random.randint(0, 0xFFFF)
print(f"Αρχικό μήνυμα (m): {m_original:04x}h ({m_original})")

# Κωδικοποίηση
c = encode(m_original)
print(f"Κωδικοποιημένο (c): {c:04x}h ({c})")

# Αποκωδικοποίηση
m_decoded = decode(c)
print(f"Αποκωδικοποιημένο (m'): {m_decoded:04x}h ({m_decoded})")

# Επαλήθευση
assert m_original == m_decoded, "Η αποκωδικοποίηση απέτυχε!"
print("\nΕπαλήθευση: Το αποκωδικοποιημένο μήνυμα ταυτίζεται με το αρχικό!")