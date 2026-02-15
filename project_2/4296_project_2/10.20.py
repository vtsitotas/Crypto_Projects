import random

# Δεδομένα του προβλήματος
p = 3571
g = 2
y = 2763

# Συνάρτηση f(x, a, b) για το Pollard's Rho
def f(X, a, b):
    r = X % 3
    if r == 0:
        X = (X * X) % p
        a = (2 * a) % (p - 1)
        b = (2 * b) % (p - 1)
    elif r == 1:
        X = (X * g) % p
        a = (a + 1) % (p - 1)
    else:
        X = (X * y) % p
        b = (b + 1) % (p - 1)
    return X, a, b

# Υλοποίηση Pollard's p
def pollard_p_dlog(p, g, y, max_tries=100):
    for attempt in range(max_tries):
        # Τυχαία αρχικοποίηση
        a = random.randint(0, p-2)
        b = random.randint(0, p-2)
        X = (pow(g, a, p) * pow(y, b, p)) % p

        A, B = a, b
        Y = X

        for i in range(1, p):
            # Slow
            X, a, b = f(X, a, b)
            # Fast (2 βήματα)
            Y, A, B = f(Y, A, B)
            Y, A, B = f(Y, A, B)

            if X == Y:
                r = (a - A) % (p - 1)
                s = (B - b) % (p - 1)

                if s == 0:
                    break  # Δεν έχει αντίστροφο

                try:
                    s_inv = pow(s, -1, p - 1)
                except ValueError:
                    break  # Δεν υπάρχει αντίστροφο

                x = (r * s_inv) % (p - 1)
                if pow(g, x, p) == y:
                    print(f"Λύση βρέθηκε στη προσπάθεια {attempt + 1}")
                    return x
                else:
                    break  # Λανθασμένη λύση – επανάληψη

    raise Exception("Αποτυχία εύρεσης διακριτού λογαρίθμου μετά από πολλές προσπάθειες.")

# Εκτέλεση
x = pollard_p_dlog(p, g, y)
print(f"Ο διακριτός λογάριθμος x είναι: {x}")
