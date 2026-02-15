"""
Αξιόπιστη επίλυση knapsack με LLL για n=30, H=15, density≈1
"""

import math
import random
import numpy as np
from fpylll import LLL, IntegerMatrix

# Βοηθητικές συναρτήσεις
def dot_product(a, b):
    return sum(x * y for x, y in zip(a, b))

def rand_bin_array(K, N):
    arr = [0] * K + [1] * (N - K)
    random.shuffle(arr)
    return arr

def find(n, d, hamming):
    if n % 2 == 1:
        return "enter an even integer"
    
    a = [random.randint(1, math.floor(2**((2 - d) * n))) for _ in range(n)]
    density = float(n / math.log(max(a), 2))
    solution = rand_bin_array(n - hamming, n)
    a0 = dot_product(solution, a)
    
    return a, a0, density, sum(solution), len(solution), solution

def solve_knapsack_with_lll(a, a0, H, max_N=100):
    """Επιλύει knapsack με δοκιμή διαφορετικών N και μορφών λύσεων"""
    n = len(a)
    
    # Διαφορετικές τιμές N να δοκιμάσουμε
    base_N = int(math.sqrt(n)) + 1
    N_values = [base_N, base_N*2, base_N*3, base_N*5, base_N*10, 50, 100]
    N_values = sorted(set(N_values))  # Αφαίρεση διπλότυπων
    
    for N in N_values:
        # Κατασκευή πίνακα B_{N,H}
        rows = n + 1
        cols = n + 3
        B = np.zeros((rows, cols), dtype=np.int64)
        
        # Πρώτες n γραμμές
        for i in range(n):
            B[i, i] = 2
            B[i, n] = N * a[i]
            B[i, n + 2] = N
        
        # Τελευταία γραμμή
        for j in range(n):
            B[n, j] = 1
        B[n, n] = N * a0
        B[n, n + 1] = 1
        B[n, n + 2] = H * N
        
        # LLL
        M = IntegerMatrix.from_matrix(B.tolist())
        LLL.reduction(M)
        
        # Αναζήτηση λύσης με διαφορετικές μορφές
        for i in range(M.nrows):
            row = list(M[i])
            
            # Μορφή 1: (2x_i-1, 0, -1, 0)
            if row[n] == 0 and row[n + 2] == 0 and row[n + 1] == -1:
                candidate = []
                valid = True
                for j in range(n):
                    x = (row[j] + 1) // 2
                    if x not in [0, 1]:
                        valid = False
                        break
                    candidate.append(x)
                if valid and sum(candidate) == H:
                    return N, candidate, "Μορφή 1"
            
            # Μορφή 2: (1-2x_i, 0, 1, 0) - συμπλήρωμα
            elif row[n] == 0 and row[n + 2] == 0 and row[n + 1] == 1:
                candidate = []
                valid = True
                for j in range(n):
                    x = (1 - row[j]) // 2
                    if x not in [0, 1]:
                        valid = False
                        break
                    candidate.append(x)
                if valid and sum(candidate) == H:
                    return N, candidate, "Μορφή 2"
            
            # Μορφή 3: (x_i, 0, 0, 0) - απευθείας δυαδική
            elif row[n] == 0 and row[n+1] == 0 and row[n+2] == 0:
                candidate = []
                valid = True
                for j in range(n):
                    if row[j] not in [0, 1]:
                        valid = False
                        break
                    candidate.append(row[j])
                if valid and sum(candidate) == H:
                    return N, candidate, "Μορφή 3"
    
    return None, None, None

# Κύριο πρόγραμμα
def main():
    n = 30
    H = 15
    density = 1.0
    
    print(f"Επίλυση knapsack: n={n}, H={H}, density≈{density}")
    print("=" * 50)
    
    # Δοκιμή μέχρι να βρεθεί λύση
    for attempt in range(1, 11):  # Μέχρι 10 προσπάθειες
        print(f"\nΠροσπάθεια {attempt}:")
        print("-" * 30)
        
        # Δημιουργία προβλήματος
        a, a0, real_density, hamming_weight, n_items, true_solution = find(n, density, H)
        
        print(f"Πυκνότητα: {real_density:.3f}")
        print(f"Στόχος a0: {a0}")
        print(f"Πραγματική λύση (Hamming weight {H}): {true_solution[:10]}...")
        
        # Επίλυση με LLL
        N_used, found_solution, solution_type = solve_knapsack_with_lll(a, a0, H)
        
        if found_solution is not None:
            print(f"\n✅ ΒΡΕΘΗΚΕ ΛΥΣΗ!")
            print(f"Χρησιμοποιήθηκε N = {N_used}")
            print(f"Τύπος λύσης: {solution_type}")
            print(f"Βρέθηκε λύση: {found_solution}")
            
            # Έλεγχος
            calculated_a0 = dot_product(a, found_solution)
            matches_true = (found_solution == true_solution)
            matches_complement = ([1-x for x in found_solution] == true_solution)
            
            print(f"\nΕπαλήθευση:")
            print(f"Σ(a_i * x_i) = {calculated_a0}")
            print(f"Στόχος a0 = {a0}")
            print(f"Ταιριάζουν; {calculated_a0 == a0}")
            print(f"Ταιριάζει με πραγματική λύση; {matches_true}")
            print(f"Ταιριάζει με συμπλήρωμα; {matches_complement}")
            
            if calculated_a0 == a0:
                print(f"\n🎉 ΕΠΙΤΥΧΙΑ! Η λύση ικανοποιεί τον στόχο.")
                break
            else:
                print(f"\n⚠️  Προσοχή: Η λύση ΔΕΝ ικανοποιεί τον στόχο.")
        else:
            print(f"❌ Δεν βρέθηκε λύση για αυτό το πρόβλημα. Δοκιμή νέου...")
    
    if found_solution is None:
        print(f"\n😞 Δεν βρέθηκε λύση μετά από 10 προσπάθειες.")
    
    return found_solution is not None

# Εκτέλεση
if __name__ == "__main__":
    main()