import math

# Συνάρτηση που υπολογίζει το άθροισμα των θετικών διαιρετών του n
def sigma(n):
    return sum(d for d in range(1, n + 1) if n % d == 0)

# Σταθερά Euler–Mascheroni (προσέγγιση)
gamma = 0.5772156649
e_gamma = math.exp(gamma)

# Έλεγχος για όλους τους περιττούς n < 220
for n in range(3, 220, 2):  # μόνο περιττοί ακέραιοι
    try:
        ln_ln_n = math.log(math.log(n))
        lhs = sigma(n) / n # left-hand side
        rhs = (e_gamma / 2) * ln_ln_n + 0.74 / ln_ln_n # right-hand side

        # Έλεγχος αν η ανισότητα ισχύει
        if lhs >= rhs:
            print(f"❌ Η ανισότητα ΔΕΝ ισχύει για n = {n}: σ(n)/n = {lhs:.4f}, όριο = {rhs:.4f}")
        else:
            print(f"✔️  Ισχύει για n = {n}: σ(n)/n = {lhs:.4f}, όριο = {rhs:.4f}")

    except ValueError:
        # Αν η ln ln n δεν ορίζεται (π.χ. για πολύ μικρά n), αγνοούμε την περίπτωση
        print(f"Παράλειψη για n = {n} (ln ln n μη ορισμένο)")
