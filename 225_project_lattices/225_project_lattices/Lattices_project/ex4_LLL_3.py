#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Σύγκριση LLL και Gauss-Lagrange σε τυχαία πλέγματα βαθμίδας 2.
"""

from fractions import Fraction
import random
import math


class LLLReducer:
    
    def __init__(self, delta=Fraction(3, 4)):
        self.delta = delta
    
    def gram_schmidt(self, basis):
        n = len(basis)
        m = len(basis[0])
        orthogonal = []
        mu = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            orth = [Fraction(x) for x in basis[i]]
            
            for j in range(i):
                numerator = sum(Fraction(basis[i][k]) * orthogonal[j][k] for k in range(m))
                denominator = sum(orthogonal[j][k] * orthogonal[j][k] for k in range(m))
                
                if denominator != 0:
                    mu[i][j] = numerator / denominator
                else:
                    mu[i][j] = Fraction(0)
                
                for k in range(m):
                    orth[k] -= mu[i][j] * orthogonal[j][k]
            
            orthogonal.append(orth)
        
        return orthogonal, mu
    
    def round_fraction(self, frac):
        num = frac.numerator
        den = frac.denominator
        q = num // den
        r = num % den
        if 2 * abs(r) >= den:
            return q + 1 if num >= 0 else q - 1
        return q
    
    def lovasz_condition(self, orthogonal, mu, i):
        m = len(orthogonal[0])
        norm_i = sum(orthogonal[i][k] * orthogonal[i][k] for k in range(m))
        norm_i_minus_1 = sum(orthogonal[i-1][k] * orthogonal[i-1][k] for k in range(m))
        mu_sq = mu[i][i-1] * mu[i][i-1]
        return norm_i >= (self.delta - mu_sq) * norm_i_minus_1
    
    def lll_exact(self, basis):
        n = len(basis)
        if n == 0:
            return [], 0
        
        m = len(basis[0])
        B = [[Fraction(x) for x in row] for row in basis]
        k = 1
        iterations = 0
        
        while k < n and iterations < 1000:
            iterations += 1
            orthogonal, mu = self.gram_schmidt(B)
            
            for j in range(k - 1, -1, -1):
                mu_kj = mu[k][j]
                rounded = self.round_fraction(mu_kj)
                if rounded != 0:
                    for i in range(m):
                        B[k][i] -= Fraction(rounded) * B[j][i]
            
            orthogonal, mu = self.gram_schmidt(B)
            
            if not self.lovasz_condition(orthogonal, mu, k):
                B[k], B[k-1] = B[k-1], B[k]
                k = max(k - 1, 1)
            else:
                k += 1
        
        return [[int(x) for x in row] for row in B], iterations


def gauss_lagrange(b1, b2):
    v1 = [Fraction(b1[0]), Fraction(b1[1])]
    v2 = [Fraction(b2[0]), Fraction(b2[1])]
    
    def norm_sq(v):
        return v[0]*v[0] + v[1]*v[1]
    
    while True:
        if norm_sq(v2) < norm_sq(v1):
            v1, v2 = v2, v1
        
        dot = v1[0]*v2[0] + v1[1]*v2[1]
        n1_sq = norm_sq(v1)
        
        if n1_sq == 0:
            break
        
        mu = Fraction(round(dot / n1_sq))
        
        if mu == 0:
            break
        
        v2[0] -= mu * v1[0]
        v2[1] -= mu * v1[1]
    
    if norm_sq(v2) < norm_sq(v1):
        v1, v2 = v2, v1
    
    return [[int(v1[0]), int(v1[1])], [int(v2[0]), int(v2[1])]]


def vector_norm(v):
    return math.sqrt(v[0]**2 + v[1]**2)


def generate_random_lattice():
    while True:
        b1 = [random.randint(-20, 20) for _ in range(2)]
        b2 = [random.randint(-20, 20) for _ in range(2)]
        
        det = b1[0] * b2[1] - b1[1] * b2[0]
        if det != 0:
            return [b1, b2]


def compare_algorithms(num_tests=100):
    reducer = LLLReducer()
    
    same_basis = 0
    lll_better = 0
    gl_better = 0
    total_diff = 0.0
    max_diff = 0.0
    examples_with_diff = []
    
    for i in range(num_tests):
        basis = generate_random_lattice()
        
        lll_result, _ = reducer.lll_exact(basis)
        gl_result = gauss_lagrange(basis[0], basis[1])
        
        lll_sorted = sorted(lll_result, key=lambda v: vector_norm(v))
        gl_sorted = sorted(gl_result, key=lambda v: vector_norm(v))
        
        lll_norm1 = vector_norm(lll_sorted[0])
        gl_norm1 = vector_norm(gl_sorted[0])
        
        diff = gl_norm1 - lll_norm1
        total_diff += diff
        
        def basis_equal(b1, b2):
            for v1, v2 in zip(sorted(b1), sorted(b2, key=lambda v: vector_norm(v))):
                if abs(vector_norm(v1) - vector_norm(v2)) > 0.001:
                    return False
            return True
        
        if basis_equal(lll_result, gl_result):
            same_basis += 1
        else:
            if abs(diff) < 0.001:
                same_basis += 1
            elif diff > 0.001:
                lll_better += 1
                if diff > max_diff:
                    max_diff = diff
                    if len(examples_with_diff) < 3:
                        examples_with_diff.append((basis, lll_result, gl_result, diff))
            else:
                gl_better += 1
                if abs(diff) > max_diff:
                    max_diff = abs(diff)
                    if len(examples_with_diff) < 3:
                        examples_with_diff.append((basis, lll_result, gl_result, diff))
    
    mean_diff = total_diff / num_tests
    
    return {
        'total_tests': num_tests,
        'same_basis': same_basis,
        'lll_better': lll_better,
        'gl_better': gl_better,
        'mean_diff': mean_diff,
        'max_diff': max_diff,
        'examples': examples_with_diff
    }


def main():
    stats = compare_algorithms(num_tests=500)
    
    total = stats['total_tests']
    same = stats['same_basis']
    lll_better = stats['lll_better']
    gl_better = stats['gl_better']
    
    print(f"Σύνολο δοκιμών: {total}")
    print(f"Πλέγματα με ίδια βάση: {same} ({same/total*100:.1f}%)")
    print(f"LLL βέλτιστος: {lll_better} ({lll_better/total*100:.1f}%)")
    print(f"Gauss-Lagrange βέλτιστος: {gl_better} ({gl_better/total*100:.1f}%)")
    print(f"Μέση διαφορά μήκους πρώτου διανύσματος (G-L - LLL): {stats['mean_diff']:.6f}")
    print(f"Μέγιστη απόλυτη διαφορά: {stats['max_diff']:.6f}")
    
    if stats['examples']:
        print("\nΠαραδείγματα με διαφορές:")
        for i, (basis, lll, gl, diff) in enumerate(stats['examples'], 1):
            print(f"Παράδειγμα {i}:")
            print(f"  Αρχική: {basis}")
            print(f"  LLL: {lll}, ‖b1‖ = {vector_norm(sorted(lll, key=lambda v: vector_norm(v))[0]):.6f}")
            print(f"  G-L: {gl}, ‖b1‖ = {vector_norm(sorted(gl, key=lambda v: vector_norm(v))[0]):.6f}")
            print(f"  Διαφορά: {diff:.6f} ({'LLL καλύτερος' if diff > 0 else 'G-L καλύτερος'})")


if __name__ == "__main__":
    main()