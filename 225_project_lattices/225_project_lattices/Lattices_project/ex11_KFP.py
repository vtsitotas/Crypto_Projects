import numpy as np
import math

def gram_schmidt(B_basis):
    """
    Υπολογίζει τους συντελεστές Gram-Schmidt (mu) και τα τετραγωνικά μήκη (B_sq).
    B_basis: Πίνακας όπου κάθε γραμμή είναι ένα διάνυσμα της βάσης.
    """
    n, m = B_basis.shape
    mu = np.zeros((n, n))
    B_sq = np.zeros(n)
    b_star = np.zeros((n, m))

    for i in range(n):
        b_star[i] = B_basis[i].astype(float)  # Βεβαιώνουμε ότι είναι float
        for j in range(i):
            if B_sq[j] > 1e-14:  # Αποφυγή διαίρεσης με πολύ μικρούς αριθμούς
                mu[i, j] = np.dot(B_basis[i], b_star[j]) / B_sq[j]
            else:
                mu[i, j] = 0
            b_star[i] = b_star[i] - mu[i, j] * b_star[j]
        
        B_sq[i] = np.dot(b_star[i], b_star[i])
        
    return mu, B_sq

def kfp_enumeration(Basis, R):
    """
    Υλοποίηση του Αλγορίθμου 14.6.1 (KFP enumeration algorithm).
    Επιστρέφει τα μισά διανύσματα - τα αντίθετα προστίθενται μετά.
    """
    n = len(Basis)
    R_sq = R**2
    
    # Line 01
    mu, B = gram_schmidt(Basis)
    
    # Line 02
    x = np.zeros(n, dtype=int)
    c = np.zeros(n)
    l = np.zeros(n)
    sumli = 0
    S = []
    k = 0  # i=1 στον ψευδοκώδικα -> k=0 εδώ

    # Ασφαλής τερματισμός
    max_iterations = 10000
    iteration = 0
    
    # Line 03
    while k < n and iteration < max_iterations:
        iteration += 1
        
        # Line 04
        sum_mu_x = 0.0
        for j in range(k + 1, n):
            sum_mu_x += x[j] * mu[j, k]
        c[k] = -sum_mu_x
        
        # Line 05
        l[k] = B[k] * (x[k] - c[k])**2
        
        # Line 06
        sumli = 0.0
        for j in range(k, n):
            sumli += l[j]
            
        # Line 07
        if sumli <= R_sq + 1e-10:  # Μικρή ανοχή για αριθμητικά σφάλματα
            # Line 08
            if k == 0:  # i=1
                # Line 09
                vec = np.zeros(Basis.shape[1])
                for j in range(n):
                    vec += x[j] * Basis[j]
                
                # Αποθήκευση αποτελέσματος
                S.append(tuple(vec)) 
                
                # Line 10
                x[0] += 1
            else:
                # Line 11 & 12
                k -= 1 
                # Line 13 (Υπολογισμός κάτω άκρου)
                sum_l_next = 0.0
                for j in range(k + 1, n):
                    sum_l_next += l[j]
                
                sum_mu_x_next = 0.0
                for j in range(k + 1, n):
                    sum_mu_x_next += mu[j, k] * x[j]
                
                # Έλεγχος για να αποφύγουμε ρίζα αρνητικού
                if R_sq - sum_l_next >= 0:
                    term_sqrt = math.sqrt((R_sq - sum_l_next) / B[k])
                else:
                    term_sqrt = 0.0
                
                val = -sum_mu_x_next - term_sqrt
                x[k] = math.ceil(val) if val < 0 else math.floor(val)
        else:
            # Line 15 & 16
            k += 1
            # Line 17
            if k < n:
                x[k] += 1

    return S

# ==========================================
# Βελτιωμένη εκτύπωση αποτελεσμάτων
# ==========================================

# 1. Ορισμός Βάσης
my_basis = np.array([
    [1.0, 0.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0]
])

# 2. Ορισμός Ακτίνας
radius = 1.1

print(f"Εκτέλεση αλγορίθμου με R = {radius}")
print("-" * 50)

# 3. Κλήση Αλγορίθμου (Επιστρέφει τα μισά)
found_vectors = kfp_enumeration(my_basis, radius)

print(f"Βρέθηκαν {len(found_vectors)} βασικά διανύσματα:")
for i, v in enumerate(found_vectors, 1):
    # Μετατροπή των numpy τύπων σε απλούς float για καθαρότερη έξοδο
    v_clean = tuple(float(x) for x in v)
    norm = math.sqrt(sum(x*x for x in v_clean))
    print(f"  {i}. {v_clean} (νόρμα = {norm:.3f})")

# 4. Υπολογισμός ΟΛΩΝ των διανυσμάτων (μαζί με τα αντίθετα)
full_set = set()

for v in found_vectors:
    v_clean = tuple(float(x) for x in v)
    full_set.add(v_clean)
    
    # Προσθήκη αντιθέτου για μη μηδενικά διανύσματα
    if any(val != 0 for val in v_clean):
        neg_v = tuple(-val for val in v_clean)
        full_set.add(neg_v)

# Ταξινόμηση για ωραία εκτύπωση
sorted_full_vectors = sorted(full_set, key=lambda v: (math.sqrt(sum(x*x for x in v)), v))

print(f"\nΣυνολικά διανύσματα (με αντίθετα): {len(sorted_full_vectors)}")
for i, v in enumerate(sorted_full_vectors, 1):
    norm = math.sqrt(sum(x*x for x in v))
    print(f"  {i}. {v} (νόρμα = {norm:.3f})")

# 5. Επαλήθευση
print(f"\nΕπαλήθευση:")
print(f"  - Μη μηδενικά διανύσματα αναμενόμενα: 6")
print(f"  - Μη μηδενικά διανύσματα που βρέθηκαν: {len([v for v in sorted_full_vectors if any(x != 0 for x in v)])}")
print(f"  - Συντομότερο μη μηδενικό διάνυσμα: {min([v for v in sorted_full_vectors if any(x != 0 for x in v)], key=lambda v: sum(x*x for x in v))}")