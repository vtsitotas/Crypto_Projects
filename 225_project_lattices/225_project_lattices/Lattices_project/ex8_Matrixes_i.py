import numpy as np
from sympy import Matrix, linsolve, symbols

# Ορισμός των πινάκων A και B
A = np.array([
    [1, 2, 3, 4],
    [-1, 1, 2, 3],
    [4, 3, 2, 1],
    [0, 0, 1, 1]
])

B = np.array([
    [5, 8, 11, 13],
    [4, 6, 8, 9],
    [8, 9, 10, 10],
    [4, 6, 9, 10]
])

# Μετατροπή σε αντικείμενα Matrix για ακριβείς ακέραιους υπολογισμούς
A_sym = Matrix(A)
B_sym = Matrix(B)

# Υπολογισμός της ανηγμένης κλιμακωτής μορφής (γραμμικής ανεξαρτησίας)
rref_A = A_sym.rref()
rref_B = B_sym.rref()

print("Ανηγμένη κλιμακωτή μορφή του A:")
print(rref_A[0])
print("\nΑνηγμένη κλιμακωτή μορφή του B:")
print(rref_B[0])

# Έλεγχος γραμμικής ανεξαρτησίας και διάστασης
rank_A = np.linalg.matrix_rank(A)
rank_B = np.linalg.matrix_rank(B)
print(f"\nΒαθμός του A: {rank_A}")
print(f"Βαθμός του B: {rank_B}")

if rank_A != rank_B:
    print("\nΟι πίνακες έχουν διαφορετικό βαθμό, επομένως δεν παράγουν το ίδιο πλέγμα.")
else:
    print("\nΟι πίνακες έχουν τον ίδιο βαθμό. Προχωράμε σε περαιτέρω έλεγχο...")

    # ===================================================================
    # ΑΛΓΟΡΙΘΜΟΣ ΕΛΕΓΧΟΥ ΙΣΟΔΥΝΑΜΙΑΣ ΠΛΕΓΜΑΤΩΝ
    # ===================================================================
    # Για να παράγουν τα πλέγματα L(A) και L(B) το ίδιο σύνολο, πρέπει:
    # 1. Κάθε γραμμή του B να είναι ακέραιος γραμμικός συνδυασμός των γραμμών του A
    # 2. Κάθε γραμμή του A να είναι ακέραιος γραμμικός συνδυασμός των γραμμών του B
    # ===================================================================

    m, n = A_sym.shape  # Διαστάσεις πίνακα (γραμμές, στήλες)

    # Δημιουργία συμβόλων για τους συντελεστές (μία μεταβλητή για κάθε γραμμή της βάσης)
    coeffs = symbols('c0:%d' % m)

    # ΕΛΕΓΧΟΣ 1: B[i] ∈ L(A) για κάθε γραμμή i του B
    print("\n" + "="*60)
    print("ΈΛΕΓΧΟΣ 1: Είναι κάθε γραμμή του B στο πλέγμα L(A)?")
    B_in_L_A = True

    for i in range(m):
        # Για την i-οστή γραμμή του B, λύνουμε το σύστημα: c0*A[0] + c1*A[1] + ... = B[i]
        equations = []
        for col in range(n):
            eq = sum(coeffs[j] * A_sym[j, col] for j in range(m)) - B_sym[i, col]
            equations.append(eq)

        # Επίλυση του συστήματος γραμμικών εξισώσεων
        solution = linsolve(equations, coeffs)

        # Ελέγχουμε αν υπάρχει λύση ΚΑΙ αν όλοι οι συντελεστές είναι ακέραιοι
        if solution:
            sol_tuple = next(iter(solution))  # Παίρνουμε τη λύση (μία πλειάδα)
            all_integers = all(val.is_Integer for val in sol_tuple)

            if not all_integers:
                B_in_L_A = False
                print(f"  Γραμμή B[{i}] = {B_sym.row(i)}: ΔΕΝ είναι ακέραιος συνδυασμός των γραμμών του A.")
                print(f"    Λύση (συντελεστές): {sol_tuple}")
                break
            else:
                print(f"  Γραμμή B[{i}] = {B_sym.row(i)}: ΕΙΝΑΙ ακέραιος συνδυασμός. Συντελεστές: {sol_tuple}")
        else:
            B_in_L_A = False
            print(f"  Γραμμή B[{i}] = {B_sym.row(i)}: ΔΕΝ υπάρχει λύση (ούτε καν ρητή).")
            break

    # ΕΛΕΓΧΟΣ 2: A[i] ∈ L(B) για κάθε γραμμή i του A
    print("\n" + "="*60)
    print("ΈΛΕΓΧΟΣ 2: Είναι κάθε γραμμή του A στο πλέγμα L(B)?")
    A_in_L_B = True

    for i in range(m):
        # Για την i-οστή γραμμή του A, λύνουμε: c0*B[0] + c1*B[1] + ... = A[i]
        equations = []
        for col in range(n):
            eq = sum(coeffs[j] * B_sym[j, col] for j in range(m)) - A_sym[i, col]
            equations.append(eq)

        solution = linsolve(equations, coeffs)

        if solution:
            sol_tuple = next(iter(solution))
            all_integers = all(val.is_Integer for val in sol_tuple)

            if not all_integers:
                A_in_L_B = False
                print(f"  Γραμμή A[{i}] = {A_sym.row(i)}: ΔΕΝ είναι ακέραιος συνδυασμός των γραμμών του B.")
                print(f"    Λύση (συντελεστές): {sol_tuple}")
                break
            else:
                print(f"  Γραμμή A[{i}] = {A_sym.row(i)}: ΕΙΝΑΙ ακέραιος συνδυασμός. Συντελεστές: {sol_tuple}")
        else:
            A_in_L_B = False
            print(f"  Γραμμή A[{i}] = {A_sym.row(i)}: ΔΕΝ υπάρχει λύση.")
            break

    print("\n" + "="*60)
    print("ΑΠΟΤΕΛΕΣΜΑ ΕΛΕΓΧΟΥ ΙΣΟΔΥΝΑΜΙΑΣ ΠΛΕΓΜΑΤΩΝ:")
    if B_in_L_A and A_in_L_B:
        print("✓ ΚΑΙ οι δύο προϋποθέσεις ισχύουν.")
        print("✓ Επομένως: L(A) = L(B) → Τα πλέγματα είναι ΙΔΙΑ.")
    else:
        print("✗ ΔΕΝ ισχύουν και οι δύο προϋποθέσεις.")
        print(f"   B ∈ L(A); {B_in_L_A}")
        print(f"   A ∈ L(B); {A_in_L_B}")
        print("✗ Επομένως: L(A) ≠ L(B) → Τα πλέγματα είναι ΔΙΑΦΟΡΕΤΙΚΑ.")