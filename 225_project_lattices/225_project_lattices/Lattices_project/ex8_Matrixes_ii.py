import numpy as np
from sympy import Matrix, symbols, linsolve

# Ορισμός πίνακα A και διανύσματος v
A = Matrix([
    [1, 2, 3, 4],
    [-1, 1, 2, 3],
    [4, 3, 2, 1],
    [0, 0, 1, 1]
])

v = Matrix([43, 69, 95, 110])

# Σύμβολα για τους συντελεστές (x1, x2, x3, x4)
x1, x2, x3, x4 = symbols('x1 x2 x3 x4', integer=True)

# Κατασκευή εξισώσεων: x1*A[0] + x2*A[1] + x3*A[2] + x4*A[3] = v
equations = []
for j in range(4):  # Για κάθε στήλη
    eq = x1*A[0, j] + x2*A[1, j] + x3*A[2, j] + x4*A[3, j] - v[j]
    equations.append(eq)

# Επίλυση του γραμμικού συστήματος
solution = linsolve(equations, (x1, x2, x3, x4))

print("Λύση του συστήματος X * A = v:")
print(solution)

# Εξαγωγή της λύσης και έλεγχος ακεραιότητας
if solution:
    sol = next(iter(solution))  # Παίρνουμε τη λύση (πλειάδα)
    print(f"\nΣυντελεστές: x1 = {sol[0]}, x2 = {sol[1]}, x3 = {sol[2]}, x4 = {sol[3]}")

    # Έλεγχος αν όλοι οι συντελεστές είναι ακέραιοι
    all_integers = all(coeff.is_Integer for coeff in sol)
    if all_integers:
        print("✅ Όλοι οι συντελεστές είναι ακέραιοι.")
        print("✅ Το διάνυσμα v = (43, 69, 95, 110) ΑΝΗΚΕΙ στο πλέγμα L(A).")

        # Επαλήθευση: Υπολογισμός του συνδυασμού
        v_calc = sol[0]*A.row(0) + sol[1]*A.row(1) + sol[2]*A.row(2) + sol[3]*A.row(3)
        print(f"\nΕπαλήθευση: {sol[0]}*A[0] + {sol[1]}*A[1] + {sol[2]}*A[2] + {sol[3]}*A[3] = {v_calc}")
        if v_calc == v:
            print("Η επαλήθευση επιβεβαιώνει το αποτέλεσμα.")
    else:
        print("❌ Οι συντελεστές δεν είναι όλοι ακέραιοι.")
        print("❌ Το διάνυσμα v ΔΕΝ ανήκει στο πλέγμα L(A).")
else:
    print("❌ Δεν υπάρχει λύση (ούτε καν με ρητούς συντελεστές).")