import numpy as np
from sympy import Matrix, sqrt

# Ορισμός πίνακα A (ή B, αφού έχουν το ίδιο πλέγμα)
A = Matrix([
    [1, 2, 3, 4],
    [-1, 1, 2, 3],
    [4, 3, 2, 1],
    [0, 0, 1, 1]
])

# Απόλυτη τιμή ορίζουσας (για τετραγωνικό αντιστρέψιμο πίνακα)
det_A = A.det()
vol_method1 = abs(det_A)

print("Μέθοδος 1 (από |det(A)|):")
print(f"  det(A) = {det_A}")
print(f"  |det(A)| = {vol_method1}")
print(f"  → Όγκος πλέγματος = {vol_method1}")

# ΕΠΑΛΗΘΕΥΣΗ: Υπολογισμός και για τον B (πρέπει να είναι ίδιος)

B = Matrix([
    [5, 8, 11, 13],
    [4, 6, 8, 9],
    [8, 9, 10, 10],
    [4, 6, 9, 10]
])

det_B = B.det()
vol_B = abs(det_B)

print("\n" + "="*50)
print("ΕΠΑΛΗΘΕΥΣΗ με πίνακα B (ίδιο πλέγμα):")
print(f"  det(B) = {det_B}")
print(f"  |det(B)| = {vol_B}")
print(f"  → Όγκος πλέγματος από B = {vol_B}")

if vol_method1 == vol_B:
    print("  ✅ Οι όγκοι συμφωνούν (επιπρόσθετη απόδειξη ότι L(A)=L(B)).")
else:
    print("  ❌ Διαφέρουν (θα έπρεπε να είναι ίδιοι).")
