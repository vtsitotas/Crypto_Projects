def trial_division(n):
    factors = []
    if n < 2:
        return factors
    # Έλεγχος για 2 ξεχωριστά
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    # Έλεγχος για περιττούς διαιρέτες μέχρι sqrt(n)
    d = 3
    max_factor = int(n**0.5) + 1
    while d <= max_factor:
        while n % d == 0:
            factors.append(d)
            n //= d
            max_factor = int(n**0.5) + 1  # Ενημέρωση του max_factor
        d += 2
    if n > 1:
        factors.append(n)
    return factors

# Παραγοντοποίηση 2^62 - 1
n1 = 2**62 - 1
factors1 = trial_division(n1)
print(f"Παραγοντοποίηση του 2^62 - 1 = {n1}:")
print(factors1)

# Παραγοντοποίηση 2^102 - 1
n2 = 2**102 - 1
factors2 = trial_division(n2)
print(f"\nΠαραγοντοποίηση του 2^102 - 1 = {n2}:")
print(factors2)