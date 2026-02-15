# Ορισμός του S-box σε μονοδιάστατη λίστα
S = [
    0, 2, 3, 7, 9, 12, 15, 7, 6, 15, 15, 1, 7, 3, 1, 0,
    1, 5, 6, 13, 4, 1, 5, 11, 7, 8, 7, 1, 1, 3, 2, 13,
    5, 3, 5, 12, 11, 1, 1, 5, 13, 0, 15, 7, 2, 2, 13, 0,
    3, 12, 3, 11, 2, 2, 2, 4, 6, 5, 5, 0, 4, 3, 1, 0
]

# Αρχικοποίηση πίνακα διαφορών (64x16) με μηδενικά
diff_table = [[0 for _ in range(16)] for _ in range(64)]

# Υπολογισμός πίνακα διαφορών
for x in range(1, 64):  # Δεν επιτρέπεται x = 0
    for z in range(64):
        z_xor = z ^ x
        if z_xor < 64:
            y = S[z] ^ S[z_xor]
            diff_table[x][y] += 1

# Εύρεση διαφορικής ομοιομορφίας
max_uniformity = max(max(row) for row in diff_table)

# Εκτύπωση πίνακα διαφορών
print("Πίνακας Διαφορικής Κατανομής (Difference Distribution Table):\n")
print("     " + " ".join(f"{y:2}" for y in range(16)))
print("    " + "---" * 16)

for x in range(1, 64):
    print(f"{x:2} | " + " ".join(f"{diff_table[x][y]:2}" for y in range(16)))

# Εκτύπωση τελικού αποτελέσματος
print("\n" + "="*50)
print(f"Η διαφορική ομοιομορφία του S-box είναι: Diff(S) = {max_uniformity}")
print("Όσο μικρότερη είναι αυτή η τιμή, τόσο πιο ανθεκτικό είναι το S-box στη διαφορική κρυπτανάλυση.")
print("="*50)
