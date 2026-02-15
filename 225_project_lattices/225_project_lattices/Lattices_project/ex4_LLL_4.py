#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Άσκηση: LLL vs SVP σε 4 διαστάσεις.
Φτιάχνουμε τυχαία πλέγματα και συγκρίνουμε το αποτέλεσμα του LLL
με το πραγματικό ελάχιστο (λ1) που βρίσκουμε με δοκιμές.
"""

from fractions import Fraction
import random
import math
from itertools import product

class MyLLL:
    def __init__(self, delta=Fraction(3, 4)):
        self.delta = delta
    
    # Υπολογισμός Gram-Schmidt (ορθογωνιοποίηση)
    def gram_schmidt(self, basis):
        n = len(basis)
        m = len(basis[0])
        orthogonal = []
        # Πίνακας για τους συντελεστές μ
        mu = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            # Παίρνουμε το τρέχον διάνυσμα
            orth = [Fraction(x) for x in basis[i]]
            
            for j in range(i):
                # Υπολογίζουμε προβολές
                numerator = sum(Fraction(basis[i][k]) * orthogonal[j][k] for k in range(m))
                denominator = sum(orthogonal[j][k] * orthogonal[j][k] for k in range(m))
                
                if denominator != 0:
                    mu[i][j] = numerator / denominator
                else:
                    mu[i][j] = Fraction(0)
                
                # Αφαιρούμε την προβολή
                for k in range(m):
                    orth[k] -= mu[i][j] * orthogonal[j][k]
            
            orthogonal.append(orth)
        
        return orthogonal, mu
    
    # Στρογγυλοποίηση στον πλησιέστερο ακέραιο
    def my_round(self, frac):
        num = frac.numerator
        den = frac.denominator
        # Ακέραιο μέρος
        q = num // den
        r = num % den
        # Έλεγχος για το αν είμαστε πάνω από το μισό
        if 2 * abs(r) >= den:
            return q + 1 if num >= 0 else q - 1
        return q
    
    # Έλεγχος συνθήκης Lovasz (για τα swaps)
    def check_lovasz(self, orthogonal, mu, i):
        m = len(orthogonal[0])
        norm_i = sum(orthogonal[i][k] * orthogonal[i][k] for k in range(m))
        norm_i_prev = sum(orthogonal[i-1][k] * orthogonal[i-1][k] for k in range(m))
        mu_sq = mu[i][i-1] * mu[i][i-1]
        
        # Ο τύπος της συνθήκης
        return norm_i >= (self.delta - mu_sq) * norm_i_prev
    
    # Ο κυρίως αλγόριθμος LLL
    def run_lll(self, basis):
        n = len(basis)
        m = len(basis[0])
        # Μετατροπή σε κλάσματα για ακρίβεια
        B = [[Fraction(x) for x in row] for row in basis]
        
        k = 1
        while k < n:
            # Τρέχουμε GSO κάθε φορά
            orthogonal, mu = self.gram_schmidt(B)
            
            # Size Reduction (μείωση μεγέθους)
            for j in range(k - 1, -1, -1):
                mu_kj = mu[k][j]
                rounded = self.my_round(mu_kj)
                
                if rounded != 0:
                    for i in range(m):
                        B[k][i] -= Fraction(rounded) * B[j][i]
            
            # Ενημέρωση GSO μετά τη μείωση
            orthogonal, mu = self.gram_schmidt(B)
            
            # Έλεγχος για Swap (Lovasz)
            if not self.check_lovasz(orthogonal, mu, k):
                # Ανταλλαγή
                B[k], B[k-1] = B[k-1], B[k]
                k = max(k - 1, 1) # Πάμε πίσω
            else:
                k += 1 # Προχωράμε
        
        # Επιστροφή σε ακεραίους
        return [[int(x) for x in row] for row in B]

# Βοηθητική για το Ευκλείδειο μήκος
def get_norm(v):
    return math.sqrt(sum(x**2 for x in v))

# Συνάρτηση που βρίσκει το ΠΡΑΓΜΑΤΙΚΟ μικρότερο διάνυσμα (SVP)
# Ψάχνει όλους τους συνδυασμούς γύρω από τη βάση
def find_true_shortest(basis, lll_basis):
    # Παίρνουμε τη βάση του LLL γιατί είναι πιο "καλή" και βοηθάει στο ψάξιμο
    n = len(basis)
    shortest_norm = float('inf')
    
    # Ψάχνουμε συντελεστές από -2 έως 2 (μικρό εύρος αρκεί μετά τον LLL)
    range_limit = 2
    coeffs_range = range(-range_limit, range_limit + 1)
    
    # Δοκιμάζουμε όλους τους συνδυασμούς
    for coeffs in product(coeffs_range, repeat=n):
        # Αγνοούμε το μηδενικό διάνυσμα
        if all(c == 0 for c in coeffs):
            continue
        
        # Φτιάχνουμε το διάνυσμα v = c1*b1 + ... + cn*bn
        v = [0] * n
        for i in range(n):
            for j in range(n):
                v[j] += coeffs[i] * lll_basis[i][j]
        
        # Ελέγχουμε μήκος
        norm = get_norm(v)
        if norm < shortest_norm:
            shortest_norm = norm
            
    return shortest_norm

# Συνάρτηση που φτιάχνει ΣΙΓΟΥΡΑ πλέγμα βαθμίδας 4
# Αν τύχει και βγει ορίζουσα 0, ξαναπροσπαθεί
def generate_rank4_lattice():
    reducer = MyLLL()
    while True:
        # Τυχαίοι αριθμοί από -10 έως 10
        basis = [[random.randint(-10, 10) for _ in range(4)] for _ in range(4)]
        
        # Χρησιμοποιούμε το Gram-Schmidt για να δούμε αν είναι ανεξάρτητα
        orth, _ = reducer.gram_schmidt(basis)
        
        # Αν κάποιο ορθογώνιο διάνυσμα είναι 0, τα διανύσματα είναι εξαρτημένα
        is_full_rank = True
        for vec in orth:
            if all(x == 0 for x in vec):
                is_full_rank = False
                break
        
        if is_full_rank:
            return basis

def run_experiment():
    print("=== Ξεκινάμε το πείραμα για 4D Πλέγματα ===")
    print("Συγκρίνουμε το πρώτο διάνυσμα του LLL με το πραγματικό λ1.\n")
    
    reducer = MyLLL()
    fails = 0
    num_tests = 15 # Πόσες φορές θα τρέξουμε το πείραμα
    
    results = []

    for i in range(1, num_tests + 1):
        # 1. Φτιάχνουμε σωστό πλέγμα
        basis = generate_rank4_lattice()
        
        # 2. Τρέχουμε LLL
        lll_basis = reducer.run_lll(basis)
        lll_norm = get_norm(lll_basis[0])
        
        # 3. Βρίσκουμε το πραγματικό λ1 με ψάξιμο
        true_lambda1 = find_true_shortest(basis, lll_basis)
        
        # Συγκρίνουμε (με μικρή ανοχή λόγω float)
        diff = lll_norm - true_lambda1
        is_optimal = diff < 0.001
        
        if not is_optimal:
            fails += 1
            status = "ΟΧΙ"
        else:
            status = "ΝΑΙ"
            
        print(f"Πείραμα {i:2d}: LLL= {lll_norm:.3f}, λ1= {true_lambda1:.3f} | Βρήκε το ελάχιστο; {status}")
        
        if not is_optimal:
            results.append(diff)

    print("\n=== Συμπεράσματα ===")
    print(f"Σύνολο πειραμάτων: {num_tests}")
    print(f"Φορές που ο LLL απέτυχε να βρει το λ1: {fails}")
    print(f"Ποσοστό αποτυχίας LLL: {(fails/num_tests)*100:.1f}%")
    
    if results:
        avg_error = sum(results) / len(results)
        print(f"Μέσος όρος σφάλματος (όταν αποτυγχάνει): {avg_error:.3f}")
        print(f"Μεγαλύτερο σφάλμα που βρήκαμε: {max(results):.3f}")

if __name__ == "__main__":
    run_experiment()