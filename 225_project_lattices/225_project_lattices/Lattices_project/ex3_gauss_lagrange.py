import numpy as np

def gauss_lagrange(b1, b2, verbose=False):
    b1 = np.array(b1, dtype=float)
    b2 = np.array(b2, dtype=float)

    if verbose:
        print(f"Εκκίνηση: b1={b1}, b2={b2}")

    B1 = np.dot(b1, b1)
    mu = np.dot(b1, b2) / B1
    b2 = b2 - round(mu) * b1
    B2 = np.dot(b2, b2)

    if verbose:
        print(f"Μετά αρχική αναγωγή: b1={b1}, b2={b2}, μ={mu:.2f} (στρογγυλοποιημένο: {round(mu)})")

    iterations = 0
    while B2 < B1:
        iterations += 1
        # Ανταλλαγή
        b1, b2 = b2.copy(), b1.copy()  # Χρήση copy() για σαφήνεια
        B1 = B2
        
        mu = np.dot(b1, b2) / B1
        b2 = b2 - round(mu) * b1
        B2 = np.dot(b2, b2)
        
        if verbose:
            print(f"Επανάληψη {iterations}: b1={b1}, b2={b2}, μ={mu:.2f}")

    if verbose:
        print(f"Τελική βάση: b1={b1} (νόρμα: {np.linalg.norm(b1):.2f}), b2={b2} (νόρμα: {np.linalg.norm(b2):.2f})")
    
    return b1, b2

def lambda1(b1, b2):
    """
    Υπολογίζει το λ1(L) - το μήκος του μικρότερου μη μηδενικού διανύσματος
    """
    reduced_b1, reduced_b2 = gauss_lagrange(b1, b2)
    return np.linalg.norm(reduced_b1)

# Παραδείγματα
print("=" * 60)
print("ΠΑΡΑΔΕΙΓΜΑ i: b1 = (1, 1), b2 = (3, 4)")
print("=" * 60)
b1_i = (1, 1)
b2_i = (3, 4)
B1_i, B2_i = gauss_lagrange(b1_i, b2_i, verbose=True)
λ1_i = lambda1(b1_i, b2_i)
print(f"λ1(L) = {λ1_i}")

print("\n" + "=" * 60)
print("ΠΑΡΑΔΕΙΓΜΑ ii: b1 = (-1, 1), b2 = (300, 400)")
print("=" * 60)
b1_ii = (-1, 1)
b2_ii = (300, 400)
B1_ii, B2_ii = gauss_lagrange(b1_ii, b2_ii, verbose=True)
λ1_ii = lambda1(b1_ii, b2_ii)
print(f"λ1(L) = {λ1_ii}")