def karatsuba(x, y):
    # Βασική περιπτωση για αναδρομή
    if x < 10 or y < 10:
        return x * y

    # Υπολογιζσμός του μέγιστου μήκους των δύο αριθμών
    # και του μισού μήκους
    n = max(len(str(x)), len(str(y)))
    half = n // 2

    # Split the numbers
    high_x = x // 10**half
    low_x = x % 10**half
    high_y = y // 10**half
    low_y = y % 10**half

    # Αναδρομική κλήση για τα τρία γινόμενα
    z0 = karatsuba(low_x, low_y)
    z1 = karatsuba((low_x + high_x), (low_y + high_y))
    z2 = karatsuba(high_x, high_y)

    # Συνδυασμός των τριών γινόμενων
    return (z2 * 10**(2*half)) + ((z1 - z2 - z0) * 10**half) + z0

def fast_mod_exp(base, exponent, modulus):
    result = 1
    B = base % modulus

    while exponent > 0:
        if exponent % 2 == 1:
            result = karatsuba(result, B) % modulus
        exponent = exponent // 2
        B = karatsuba(B, B) % modulus

    return result

# Παράδειγμα υπολογισμοων
modulus = 2**107 - 1
part1 = fast_mod_exp(2, 1000, modulus)
part2 = fast_mod_exp(3, 101, modulus)
part3 = fast_mod_exp(5, 47, modulus)

# Τελικό αποτέλεσμα (χρήση Karatsuba στο γινόμενο των τριών μερών)
# και εφαρμογή του mod
intermediate = karatsuba(part1, part2) % modulus
final_result = karatsuba(intermediate, part3) % modulus

print("Result:", final_result)