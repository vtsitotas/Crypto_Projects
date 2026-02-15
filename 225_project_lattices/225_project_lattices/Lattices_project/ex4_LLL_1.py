from fractions import Fraction
from copy import deepcopy

def gso_exact(B):
    """
    Gram-Schmidt Orthogonalization - Ακριβής έκδοση
    """
    n = len(B)
    m = len(B[0])

    # Μετατροπή σε Fractions
    B_frac = [[Fraction(x) for x in vec] for vec in B]

    B_star = [[Fraction(0)] * m for _ in range(n)]
    mu = [[Fraction(0)] * n for _ in range(n)]

    for i in range(n):
        B_star[i] = B_frac[i][:]

        for j in range(i):
            # Εσωτερικό γινόμενο <b_i, b_j^*>
            inner_num = sum(B_frac[i][k] * B_star[j][k] for k in range(m))
            # Εσωτερικό γινόμενο <b_j^*, b_j^*>
            inner_den = sum(B_star[j][k] * B_star[j][k] for k in range(m))

            if inner_den == 0:
                mu[i][j] = Fraction(0)
            else:
                mu[i][j] = inner_num / inner_den

            # Αφαίρεση προβολής
            for k in range(m):
                B_star[i][k] -= mu[i][j] * B_star[j][k]

        mu[i][i] = Fraction(1)

    return B_star, mu

def lll_exact(B, delta=Fraction(3, 4)):
    """
    LLL αλγόριθμος - Ακριβής έκδοση χωρίς floats
    """
    n = len(B)
    if n <= 1:
        return deepcopy(B)

    # Μετατροπή σε Fractions
    basis = [[Fraction(x) for x in vec] for vec in B]

    # Αρχικοποίηση
    k = 1

    while k < n:
        # Υπολογισμός GSO
        B_star, mu = gso_exact(basis)

        # Size Reduction για το b_k
        for j in range(k-1, -1, -1):
            if abs(mu[k][j]) > Fraction(1, 2):
                # Στρογγυλοποίηση χωρίς floats - χρησιμοποιώντας round() για Fractions
                c = round(mu[k][j])
                if c != 0:
                    # b_k = b_k - c * b_j
                    for i in range(len(basis[k])):
                        basis[k][i] -= c * basis[j][i]
                    # Επαναϋπολογισμός GSO
                    B_star, mu = gso_exact(basis)

        # Συνθήκη Lovász
        if k > 0:
            norm_k_minus_1 = sum(x*x for x in B_star[k-1])
            norm_k = sum(x*x for x in B_star[k])
            μ_k_k_minus_1 = mu[k][k-1]

            rhs = μ_k_k_minus_1 * μ_k_k_minus_1 * norm_k_minus_1 + norm_k

            if delta * norm_k_minus_1 > rhs:
                # Αντιμετάθεση
                basis[k], basis[k-1] = basis[k-1], basis[k]
                k = max(1, k - 1)
                B_star, mu = gso_exact(basis)
            else:
                k += 1
        else:
            k += 1

    # Μετατροπή πίσω σε ακέραιους
    return [[int(x) for x in vec] for vec in basis]



    # Δοκιμή
if __name__ == "__main__":
    print("=== Δοκιμή LLL χωρίς floats ===")

    B1 = [[1, 1], [3, 4]]
    print("Βάση 1:")
    for row in B1:
        print(row)

    result1 = lll_exact(B1)
    print("LLL-αναγωγισμένη:")
    for row in result1:
        print([int(x) for x in row])

    print("\nΒάση 2:")
    B2 = [[1, 1, 0], [0, 1, 1], [1, 0, 1]]
    for row in B2:
        print(row)

    result2 = lll_exact(B2)
    print("LLL-αναγωγισμένη:")
    for row in result2:
        print([int(x) for x in row])

    # Δοκιμή με μεγαλύτερα νούμερα
    print("\nΒάση 3:")
    B3 = [[15, 23, 17], [46, 15, 32], [12, 45, 28]]
    for row in B3:
        print(row)

    result3 = lll_exact(B3)
    print("LLL-αναγωγισμένη:")
    for row in result3:
        print([int(x) for x in row])