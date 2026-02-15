import random

# Πίνακας αντιστοίχισης χαρακτήρων σε 5-bit δυαδικές συμβολοσειρές
char_to_bits = {
    'A': '00000', 'B': '00001', 'C': '00010', 'D': '00011', 'E': '00100',
    'F': '00101', 'G': '00110', 'H': '00111', 'I': '01000', 'J': '01001',
    'K': '01010', 'L': '01011', 'M': '01100', 'N': '01101', 'O': '01110',
    'P': '01111', 'Q': '10000', 'R': '10001', 'S': '10010', 'T': '10011',
    'U': '10100', 'V': '10101', 'W': '10110', 'X': '10111', 'Y': '11000',
    'Z': '11001', '.': '11010', '!': '11011', '?': '11100', '(': '11101',
    ')': '11110', '-': '11111'
}

# Αντίστροφος πίνακας: από 5-bit δυαδική συμβολοσειρά στον αντίστοιχο χαρακτήρα
bits_to_char = {v: k for k, v in char_to_bits.items()}

def text_to_bits(text):
    """Μετατρέπει κείμενο σε συμβολοσειρά bits χρησιμοποιώντας τον πίνακα κωδικοποίησης"""
    bits = []
    for char in text.upper():  # μετατροπή σε κεφαλαία
        if char in char_to_bits:
            bits.append(char_to_bits[char])  # προσθήκη δυαδικής μορφής
        else:
            raise ValueError(f"Character '{char}' not in encoding table")  # έλεγχος έγκυρων χαρακτήρων
    return ''.join(bits)  # ένωση όλων των bits σε μία συμβολοσειρά

def bits_to_text(bits):
    """Μετατρέπει δυαδική συμβολοσειρά πίσω σε κείμενο με βάση τον πίνακα κωδικοποίησης"""
    # Χωρισμός της συμβολοσειράς σε 5-bit τμήματα
    chunks = [bits[i:i+5] for i in range(0, len(bits), 5)]
    text = []
    for chunk in chunks:
        if chunk in bits_to_char:
            text.append(bits_to_char[chunk])  # μετατροπή σε χαρακτήρα
        else:
            raise ValueError(f"Invalid bit sequence: {chunk}")  # έλεγχος εγκυρότητας bit
    return ''.join(text)

def generate_key(length):
    """Δημιουργεί ένα τυχαίο κλειδί (bit string) ίδιου μήκους με το μήνυμα"""
    return ''.join(random.choice('01') for _ in range(length))

def xor_bits(a, b):
    """Υλοποιεί bitwise XOR σε δύο συμβολοσειρές bits ίδιου μήκους"""
    if len(a) != len(b):
        raise ValueError("Binary strings must be of equal length")
    return ''.join(str(int(x) ^ int(y)) for x, y in zip(a, b))  # XOR ανά bit

def encrypt(plaintext):
    """Κρυπτογραφεί ένα μήνυμα χρησιμοποιώντας One-Time Pad"""
    # Μετατροπή του μηνύματος σε bits
    plaintext_bits = text_to_bits(plaintext)
    
    # Δημιουργία τυχαίου κλειδιού
    key = generate_key(len(plaintext_bits))
    
    # Κρυπτογράφηση με XOR ανάμεσα στο μήνυμα και το κλειδί
    ciphertext_bits = xor_bits(plaintext_bits, key)
    
    # Μετατροπή του κρυπτογραφημένου bit string πίσω σε χαρακτήρες
    ciphertext = bits_to_text(ciphertext_bits)
    
    return ciphertext, key  # Επιστροφή κρυπτογραφημένου μηνύματος και κλειδιού

def decrypt(ciphertext, key):
    """Αποκρυπτογραφεί ένα μήνυμα με χρήση του OTP και του αρχικού κλειδιού"""
    # Μετατροπή του κρυπτογραφημένου κειμένου σε bits
    ciphertext_bits = text_to_bits(ciphertext)
    
    # XOR με το ίδιο κλειδί για να ανακτηθούν τα αρχικά bits
    plaintext_bits = xor_bits(ciphertext_bits, key)
    
    # Μετατροπή πίσω σε αρχικό κείμενο
    plaintext = bits_to_text(plaintext_bits)
    
    return plaintext

# Παράδειγμα χρήσης του αλγορίθμου
if __name__ == "__main__":
    message = "HELLOMRDRAZIWTH"
    print(f"Original message: {message}")
    
    # Κρυπτογράφηση
    ciphertext, key = encrypt(message)
    print(f"Ciphertext: {ciphertext}")
    print(f"Key (binary): {key}")
    
    # Αποκρυπτογράφηση
    decrypted = decrypt(ciphertext, key)
    print(f"Decrypted message: {decrypted}")
