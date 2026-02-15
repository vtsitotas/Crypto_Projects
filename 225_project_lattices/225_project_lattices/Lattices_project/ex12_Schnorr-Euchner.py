import numpy as np

def schnorr_euchner_svp_pruned_final(basis):
    """
    Υλοποίηση Αλγορίθμου 14.6.2 (SVP) με Pruning (Άσκηση 14.23).
    
    Arguments:
        basis: Πίνακας (ή λίστα λιστών) που αναπαριστά τη βάση του πλέγματος.
        
    Returns:
        best_sol: Το συντομότερο μη μηδενικό διάνυσμα που βρέθηκε.
        best_norm_sq: Το τετράγωνο της ευκλείδειας νόρμας του.
    """
    basis = np.array(basis, dtype=float)
    n = len(basis)
    
    # --- 1. Gram-Schmidt Orthogonalization ---
    # Υπολογισμός των μ_{ji} και των τετραγώνων νόρμας ||b*_i||^2
    mu = np.zeros((n, n))
    B = np.zeros(n)  # Squared norms of orthogonal vectors
    b_star = np.zeros_like(basis)
    
    for i in range(n):
        b_star[i] = basis[i].copy()
        for j in range(i):
            mu[i][j] = np.dot(basis[i], b_star[j]) / B[j]
            b_star[i] -= mu[i][j] * b_star[j]
        B[i] = np.dot(b_star[i], b_star[i])
    
    # --- 2. Initialization ---
    # Αρχικοποίηση R^2 με τη νόρμα του πρώτου διανύσματος της βάσης.
    # Καθώς βρίσκουμε μικρότερα διανύσματα, αυτό θα μειώνεται (SVP strategy).
    best_norm_sq = B[0]
    best_sol = basis[0].copy()
    
    # Χρησιμοποιούμε πίνακες μεγέθους n+1 για να συμβαδίζουμε με το 1-based indexing
    # των αλγορίθμων στη βιβλιογραφία (και στον ψευδοκώδικα).
    x = np.zeros(n + 1, dtype=int)
    c = np.zeros(n + 1)
    ell = np.zeros(n + 1)
    
    Delta_x = np.zeros(n + 1, dtype=int)
    Delta2_x = np.zeros(n + 1, dtype=int)
    
    # Αρχική κατεύθυνση Zig-Zag (Γραμμή 3 ψευδοκώδικα)
    Delta_x[1] = 1
    Delta2_x[1] = 1
    for j in range(2, n + 1): 
        Delta2_x[j] = -1
        
    # --- Pruning Vector (Άσκηση 14.23) ---
    # a_i = min{1, sqrt(1.05 * i / n)}
    a = np.zeros(n + 1)
    for i in range(1, n + 1):
        val = np.sqrt(1.05 * i / n)
        a[i] = min(1.0, val)
    
    i = 1
    
    # --- 3. Main Enumeration Loop (While i <= n) ---
    while i <= n:
        # Γραμμή 5: Υπολογισμός κέντρου c_i
        # ΠΡΟΣΟΧΗ: Το πρόσημο είναι αρνητικό (-) σύμφωνα με τον αλγόριθμο 14.6.3
        # c_i = - sum_{j=i+1}^n x_j * mu_{ji}
        current_sum = 0.0
        for j in range(i + 1, n + 1):
            current_sum += x[j] * mu[j-1][i-1] # (indices adjusted for 0-based matrix)
        c[i] = -current_sum 
        
        # Γραμμή 6: Υπολογισμός μήκους στο επίπεδο i
        ell[i] = B[i-1] * (x[i] - c[i]) ** 2
        
        # Γραμμή 7: Μερικό άθροισμα μηκών (sumli) από i έως n
        sumli = 0.0
        for j in range(i, n + 1):
            sumli += ell[j]
        
        # --- Pruning Condition ---
        # Η άσκηση λέει: Έλεγχος με R_{n+1-i}^2 = a_{n+1-i}^2 * R^2
        # Το R^2 εδώ είναι το τρέχον 'best_norm_sq'.
        current_pruning_bound = (a[n + 1 - i] ** 2) * best_norm_sq
        
        # Γραμμή 11 (τροποποιημένη με pruning): 
        # Αν είμαστε εντός ορίων ΚΑΙ δεν είμαστε σε φύλλο (i > 1) -> Κατεβαίνουμε
        if sumli < current_pruning_bound and i > 1:
            i -= 1 # Move Down
            
            # Γραμμές 13-16: Προετοιμασία επόμενου επιπέδου
            # Υπολογισμός κέντρου για το νέο i
            current_sum = 0.0
            for j in range(i + 1, n + 1):
                current_sum += x[j] * mu[j-1][i-1]
            c[i] = -current_sum
            
            x[i] = round(c[i]) # Closest Integer (Babai point)
            
            # Reset ZigZag variables
            Delta_x[i] = 0
            if c[i] < x[i]: 
                Delta2_x[i] = -1
            else: 
                Delta2_x[i] = 1
            
        else:
            # Εδώ φτάνουμε σε δύο περιπτώσεις:
            # 1. Είμαστε σε φύλλο (i == 1) και το μήκος είναι valid.
            # 2. Το μήκος ξεπέρασε το όριο (Pruned or out of bounds).
            
            # Έλεγχος Λύσης (SVP Update)
            if i == 1 and sumli < best_norm_sq:
                # Βεβαιωνόμαστε ότι δεν είναι το μηδενικό διάνυσμα
                if sumli > 1e-9:
                    best_norm_sq = sumli
                    # Ανακατασκευή του διανύσματος
                    vec = np.zeros(len(basis[0]))
                    for idx in range(1, n + 1):
                        vec += x[idx] * basis[idx-1]
                    best_sol = vec.copy()
            
            # Γραμμές 21-28: Backtracking (Move Up)
            if i == n:
                break # Τέλος αλγορίθμου
            else:
                i += 1 # Ανεβαίνουμε επίπεδο
                
                # Zig-Zag Enumeration Logic
                # Ενημερώνουμε το x[i] για την επόμενη κοντινότερη τιμή
                Delta2_x[i] = -Delta2_x[i]
                Delta_x[i] = -Delta_x[i] + Delta2_x[i]
                x[i] += Delta_x[i]

    return best_sol, best_norm_sq

# ==========================================
#              TEST CASES
# ==========================================

def run_test(name, basis, expected_sq_norm):
    print(f"\n--- {name} ---")
    basis_arr = np.array(basis)
    print(f"Basis:\n{basis_arr}")
    
    vec, sq_norm = schnorr_euchner_svp_pruned_final(basis)
    
    print(f"-> Found Vector: {vec}")
    print(f"-> Squared Norm: {sq_norm:.6f}")
    
    # Επιτρέπουμε μικρή απόκλιση λόγω floating point arithmetic
    if abs(sq_norm - expected_sq_norm) < 1e-5:
        print("✅ TEST PASSED")
    else:
        print(f"❌ TEST FAILED (Expected ~{expected_sq_norm})")

if __name__ == "__main__":
    # Test 1: Ορθογώνιο Πλέγμα
    # Το μικρότερο είναι το [0, 2] (norm^2 = 4)
    run_test("Test 1: Simple Orthogonal", [[5, 0], [0, 2]], 4.0)

    # Test 2: Skewed Basis (Η παγίδα)
    # Βάση: [10, 0], [11, 1]. 
    # Διαφορά: [11, 1] - [10, 0] = [1, 1]. Norm^2 = 1^2 + 1^2 = 2.
    run_test("Test 2: Skewed Basis (Backtracking check)", [[10, 0], [11, 1]], 2.0)

    # Test 3: 4D Lattice
    # Εδώ το [1,1,1,1] έχει norm^2 = 4.
    basis_4d = [
        [2, 0, 0, 0],
        [0, 2, 0, 0],
        [0, 0, 2, 0],
        [1, 1, 1, 1]
    ]
    run_test("Test 3: 4D Lattice", basis_4d, 4.0)