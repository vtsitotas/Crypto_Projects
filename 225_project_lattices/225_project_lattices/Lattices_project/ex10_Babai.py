import numpy as np

def gram_schmidt(B):
    """Βήμα 2: Υπολογισμός GSO"""
    B = np.array(B, dtype=float)
    B_star = []
    for v in B:
        # Προβολή του v στους ήδη υπολογισμένους ορθογώνιους
        w = v - sum(np.dot(v, b) / np.dot(b, b) * b for b in B_star)
        B_star.append(w)
    return np.array(B_star)

def babai_nearest_plane_exact(B, t):
    """
    Υλοποίηση ακριβώς βάσει του Αλγορίθμου 14.7.1
    """
    # Μετατροπή σε numpy arrays για ευκολία πράξεων
    B = np.array(B, dtype=float)
    t = np.array(t, dtype=float)
    n = len(B)

    # Βήμα 1: B <- LLL(B). 
    # Εδώ το παραλείπουμε. Αν η βάση δεν είναι reduced, 
    # πρέπει να καλέσετε μια συνάρτηση LLL πριν περάσετε το B.
    
    # Βήμα 2: B* <- GSO(B)
    B_star = gram_schmidt(B)
    
    # Βήμα 3: b <- t (Προσοχή: εδώ το b του ψευδοκώδικα είναι προσωρινή μεταβλητή, όχι η βάση)
    b_vec = t.copy()
    
    # Βήμα 4: for j = n to 1 do (Στην Python: n-1 έως 0)
    for j in range(n - 1, -1, -1):
        
        # Βήμα 5: υπολογισμός c_j = round( <b_vec, b*_j> / ||b*_j||^2 )
        # Ο ψευδοκώδικας γράφει b * b*_j, εννοεί το τρέχον υπόλοιπο (b_vec)
        
        dot_product = np.dot(b_vec, B_star[j])
        norm_sq = np.dot(B_star[j], B_star[j])
        
        # Ο τελεστής [x] (nearest integer)
        c_j = round(dot_product / norm_sq)
        
        # Βήμα 6: b <- b - c_j * b_j
        b_vec = b_vec - c_j * B[j]
    
    # Βήμα 7: return t - b
    # (To b_vec τώρα περιέχει το "σφάλμα". Αφαιρώντας το σφάλμα από το t, παίρνουμε το σημείο του πλέγματος)
    return t - b_vec

# --- ΠΑΡΑΔΕΙΓΜΑ ---
if __name__ == "__main__":
    # Παράδειγμα βάσης (ας υποθέσουμε ότι είναι ήδη σχετικά καλή/reduced)
    basis = np.array([[1, 2], [3, 5]])
    target = np.array([12.1, 19.8])

    result = babai_nearest_plane_exact(basis, target)
    
    print(f"Target t: {target}")
    print(f"Result x: {result}")
    
    # Επαλήθευση
    # Το [11, 20] είναι 5*[1,2] + 2*[3,5]
    diff = np.linalg.norm(target - result)
    print(f"Distance: {diff}")