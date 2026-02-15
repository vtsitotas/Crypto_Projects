#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fractions import Fraction
import random
import math


class LLLFinder:
    
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
                numerator = sum(Fraction(basis[i][k]) * orthogonal[j][k] 
                              for k in range(m))
                denominator = sum(orthogonal[j][k] * orthogonal[j][k] 
                                for k in range(m))
                
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
    
    def is_lll_reduced(self, basis):
        n = len(basis)
        if n <= 1:
            return True
        
        B = [[Fraction(x) for x in row] for row in basis]
        orthogonal, mu = self.gram_schmidt(B)
        
        for i in range(n):
            for j in range(i):
                if abs(mu[i][j]) > Fraction(1, 2):
                    return False
        
        for i in range(1, n):
            norm_i = sum(orthogonal[i][k] * orthogonal[i][k] for k in range(len(orthogonal[0])))
            norm_i_minus_1 = sum(orthogonal[i-1][k] * orthogonal[i-1][k] for k in range(len(orthogonal[0])))
            mu_sq = mu[i][i-1] * mu[i][i-1]
            
            if norm_i < (self.delta - mu_sq) * norm_i_minus_1:
                return False
        
        return True
    
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


def main():
    print("Παράδειγμα πλέγματος όπου ‖b1‖ > ‖b2‖ μετά LLL:\n")
    
    finder = LLLFinder()
    
    # Το παράδειγμα που βρήκαμε
    basis = [[-9, 4], [-6, 13]]
    
    print(f"Αρχική βάση:")
    print(f"  b1 = {basis[0]}, ‖b1‖ = {math.sqrt(basis[0][0]**2 + basis[0][1]**2):.6f}")
    print(f"  b2 = {basis[1]}, ‖b2‖ = {math.sqrt(basis[1][0]**2 + basis[1][1]**2):.6f}")
    print(f"  ‖b1‖ > ‖b2‖: {math.sqrt(basis[0][0]**2 + basis[0][1]**2) > math.sqrt(basis[1][0]**2 + basis[1][1]**2)}")
    
    # Εφαρμογή LLL
    lll_basis, _ = finder.lll_exact(basis)
    
    print(f"\nΜετά LLL:")
    print(f"  b1 = {lll_basis[0]}, ‖b1‖ = {math.sqrt(lll_basis[0][0]**2 + lll_basis[0][1]**2):.6f}")
    print(f"  b2 = {lll_basis[1]}, ‖b2‖ = {math.sqrt(lll_basis[1][0]**2 + lll_basis[1][1]**2):.6f}")
    print(f"  ‖b1‖ > ‖b2‖: {math.sqrt(lll_basis[0][0]**2 + lll_basis[0][1]**2) > math.sqrt(lll_basis[1][0]**2 + lll_basis[1][1]**2)} ✓")
    
    # Άλλο γνωστό παράδειγμα
    print("\n" + "="*50)
    print("Γνωστό παράδειγμα: [[10, 3], [2, 1]]")
    
    basis2 = [[10, 3], [2, 1]]
    lll_basis2, _ = finder.lll_exact(basis2)
    
    print(f"\nΑρχική: {basis2}")
    print(f"LLL: {lll_basis2}")
    print(f"  ‖b1‖ = {math.sqrt(lll_basis2[0][0]**2 + lll_basis2[0][1]**2):.6f}")
    print(f"  ‖b2‖ = {math.sqrt(lll_basis2[1][0]**2 + lll_basis2[1][1]**2):.6f}")
    print(f"  ‖b1‖ > ‖b2‖: {math.sqrt(lll_basis2[0][0]**2 + lll_basis2[0][1]**2) > math.sqrt(lll_basis2[1][0]**2 + lll_basis2[1][1]**2)} ✓")


if __name__ == "__main__":
    main()