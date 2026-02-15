def int_to_bin_list(x, bits=5):
    return [int(b) for b in format(x, f'0{bits}b')]

def bin_list_to_int(b):
    return int(''.join(map(str, b)), 2)

def dot_product_mod2(a, b):
    return sum(x & y for x, y in zip(a, b)) % 2

def hamming_weight(v):
    return sum(v)

# Ορισμός του S-box
S_box = [int_to_bin_list((x * x + 3) % 32) for x in range(32)]

# Υπολογισμός LBN
nonzero_vectors = [int_to_bin_list(i) for i in range(1, 32)]
min_lbn = float('inf')
best_details = []

for alpha in nonzero_vectors:
    for beta in nonzero_vectors:
        correlation_sum = 0
        steps = []

        for x in range(32):
            x_bin = int_to_bin_list(x)
            s_x = S_box[x]
            dot_beta_sx = dot_product_mod2(beta, s_x)
            dot_alpha_x = dot_product_mod2(alpha, x_bin)
            exponent = (dot_beta_sx + dot_alpha_x) % 2
            term = (-1) ** exponent
            correlation_sum += term

            steps.append(
                f"x={x:2d} ({''.join(map(str,x_bin))}) | "
                f"S(x)={''.join(map(str,s_x))} | "
                f"β·S(x)={dot_beta_sx}, α·x={dot_alpha_x} → "
                f"exp={exponent}, (-1)^exp={term}"
            )

        if correlation_sum != 0:
            wt = hamming_weight(alpha) + hamming_weight(beta)
            if wt < min_lbn:
                min_lbn = wt
                best_details = [(alpha, beta, correlation_sum, steps)]
            elif wt == min_lbn:
                best_details.append((alpha, beta, correlation_sum, steps))

# Εκτύπωση αποτελεσμάτων
print(f"Ελάχιστο Linear Branch Number (LBN): {min_lbn}\n")
for idx, (alpha, beta, corr, steps) in enumerate(best_details, start=1):
    print(f"----- Περίπτωση {idx} -----")
    print(f"α = {''.join(map(str, alpha))}  (Hamming weight = {hamming_weight(alpha)})")
    print(f"β = {''.join(map(str, beta))}  (Hamming weight = {hamming_weight(beta)})")
    print(f"Correlation Sum = {corr}")
    print("Αναλυτικά Βήματα:")
    for step in steps:
        print(step)
    print("\n")

