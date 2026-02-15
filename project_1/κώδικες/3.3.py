import matplotlib.pyplot as plt

# Παράμετροι LCG
m = 2**10  # 1024
a = 5
c = 3
x0 = 1     # Αρχική τιμή (x0 != 0)

# Δημιουργία της ακολουθίας
def lcg_sequence(x0, a, c, m, n):
    sequence = []
    x = x0
    for _    in range(n):
        x = (a * x + c) % m
        sequence.append(x)
    return sequence

# Υπολογισμός 150 αριθμών
sequence = lcg_sequence(x0, a, c, m, 150)

# Δημιουργία ιστογράμματος
plt.hist(sequence, bins=10, edgecolor='black', range=(0, m))
plt.title('Ιστόγραμμα συχνοτήτων των 150 πρώτων αριθμών LCG')
plt.xlabel('Διάστημα τιμών')
plt.ylabel('Συχνότητα')
plt.xticks([i * (m/10) for i in range(11)], labels=[f"{int(i * (m/10))}" for i in range(11)])
plt.grid(axis='y', alpha=0.5)
plt.show()