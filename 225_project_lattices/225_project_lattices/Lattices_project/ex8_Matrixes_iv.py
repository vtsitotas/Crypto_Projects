import numpy as np
from sympy import Matrix

# Αρχικός πίνακας
A = Matrix([
    [1, 2, 3, 4],
    [-1, 1, 2, 3],
    [4, 3, 2, 1],
    [0, 0, 1, 1]
])

# === ΤΟ ΜΥΣΤΙΚΟ: LLL REDUCTION ===
A_lll = A.lll()
print("Αρχική Βάση A:\n", A)
print("\nΒελτιστοποιημένη Βάση (LLL):\n", A_lll)

# Μετατροπή σε numpy
basis_np = np.array(A_lll).astype(np.float64)

def count_points(radius_sq, side_val):  # ΔΙΟΡΘΩΣΗ: Αφαίρεση του ":abai"
    # Με LLL βάση, το εύρος -6 έως 6 είναι υπερ-αρκετό!
    search_range = range(-6, 7)

    count_ball = 0
    count_cube = 0

    for z1 in search_range:
        for z2 in search_range:
            for z3 in search_range:
                for z4 in search_range:
                    z = np.array([z1, z2, z3, z4])
                    x = z @ basis_np

                    # 1. Έλεγχος Σφαίρας
                    norm_sq = np.dot(x, x)
                    if norm_sq <= radius_sq:
                        count_ball += 1

                    # 2. Έλεγχος Κύβου
                    if np.all(np.abs(x) <= side_val):
                        count_cube += 1

    return count_ball, count_cube

# Παράμετροι
R = 10
radius_sq = R**2
side = 5

print("="*50)
print("Υπολογισμός με LLL Βάση...")
c_ball, c_cube = count_points(radius_sq, side)

print(f"Σημεία στη Σφαίρα (R=10): {c_ball}")
print(f"Σημεία στον Κύβο (Side=10): {c_cube}")

# Θεωρητική Σύγκριση
det_L = 5.0
V_ball = (np.pi**2 / 2) * (R**4)
V_cube = (2 * side)**4

est_ball = V_ball / det_L
est_cube = V_cube / det_L

print("\n" + "="*50)
print("ΣΥΓΚΡΙΣΗ")
print(f"Σφαίρα: Βρέθηκαν {c_ball} vs Θεωρητικά ~{est_ball:.0f}")
print(f"Κύβος:  Βρέθηκαν {c_cube} vs Θεωρητικά ~{est_cube:.0f}")