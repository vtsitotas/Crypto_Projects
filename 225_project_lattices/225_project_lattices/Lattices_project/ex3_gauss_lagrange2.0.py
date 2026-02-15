import numpy as np
import matplotlib.pyplot as plt

def gauss_lagrange(b1, b2):
    """
    Υλοποίηση του αλγορίθμου Gauss-Lagrange
    """
    b1 = np.array(b1, dtype=float)
    b2 = np.array(b2, dtype=float)

    B1 = np.dot(b1, b1)
    mu = np.dot(b1, b2) / B1
    b2 = b2 - round(mu) * b1
    B2 = np.dot(b2, b2)

    while B2 < B1:
        b1, b2 = b2, b1
        B1 = B2
        mu = np.dot(b1, b2) / B1
        b2 = b2 - round(mu) * b1
        B2 = np.dot(b2, b2)

    return b1, b2

def calculate_angle(v1, v2):
    """
    Υπολογισμός γωνίας μεταξύ δύο διανυσμάτων σε μοίρες
    """
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    
    # Αποφυγή διαίρεσης με μηδέν
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    
    cos_theta = dot_product / (norm_v1 * norm_v2)
    # Φράσμα για αριθμητική αστάθεια
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    
    angle_rad = np.arccos(cos_theta)
    angle_deg = np.degrees(angle_rad)
    
    return angle_deg

# Πείραμα με 50 τυχαία διανύσματα
np.random.seed(42)  # Για αναπαραγωγή αποτελεσμάτων
n_experiments = 50
angles = []

print("ΠΕΙΡΑΜΑ: Γωνίες μετά από Gauss-Lagrange σε 50 τυχαία διανύσματα")
print("=" * 60)

for i in range(n_experiments):
    # Δημιουργία τυχαίων διανυσμάτων στο Z² με συντελεστές από -20 έως 20
    b1 = np.random.randint(-20, 21, 2)
    b2 = np.random.randint(-20, 21, 2)
    
    # Εφαρμογή Gauss-Lagrange
    reduced_b1, reduced_b2 = gauss_lagrange(b1, b2)
    
    # Υπολογισμός γωνίας
    angle = calculate_angle(reduced_b1, reduced_b2)
    angles.append(angle)
    
    if i < 5:  # Εμφάνιση πρώτων 5 cases για επίδειξη
        print(f"Πείραμα {i+1}:")
        print(f"  Αρχική βάση: {b1}, {b2}")
        print(f"  Ανηγμένη βάση: {reduced_b1}, {reduced_b2}")
        print(f"  Γωνία: {angle:.2f}°")
        print()

# Στατιστικά
mean_angle = np.mean(angles)
min_angle = np.min(angles)
max_angle = np.max(angles)
std_angle = np.std(angles)

print("ΣΤΑΤΙΣΤΙΚΑ ΑΠΟΤΕΛΕΣΜΑΤΑ:")
print(f"Μέση γωνία: {mean_angle:.2f}°")
print(f"Ελάχιστη γωνία: {min_angle:.2f}°")
print(f"Μέγιστη γωνία: {max_angle:.2f}°")
print(f"Τυπική απόκλιση: {std_angle:.2f}°")

# Ιστόγραμμα γωνιών
plt.figure(figsize=(10, 6))
plt.hist(angles, bins=15, alpha=0.7, color='skyblue', edgecolor='black')
plt.axvline(mean_angle, color='red', linestyle='--', linewidth=2, label=f'Μέση γωνία: {mean_angle:.2f}°')
plt.axvline(90, color='green', linestyle='--', linewidth=2, label='Ορθογωνία (90°)')
plt.xlabel('Γωνία (μοίρες)')
plt.ylabel('Συχνότητα')
plt.title('Κατανομή Γωνιών μετά από Αλγόριθμο Gauss-Lagrange\n(50 πειράματα)')
plt.legend()
plt.grid(alpha=0.3)
plt.show()

# Απάντηση στο θεωρητικό ερώτημα
print("\n" + "=" * 60)
print("ΘΕΩΡΗΤΙΚΟ ΕΡΩΤΗΜΑ:")
print("Αν υπάρχει ορθογώνια βάση στο πλέγμα, θα την βρει ο αλγόριθμος;")
print("=" * 60)
print("ΑΠΑΝΤΗΣΗ:")
print("ΝΑΙ, ο αλγόριθμος Gauss-Lagrange ΘΑ βρει ορθογώνια βάση αν αυτή υπάρχει στο πλέγμα.")
print("\nΛόγοι:")
print("1. Ο αλγόριθμος ελαχιστοποιεί τις νόρμες των διανυσμάτων βάσης")
print("2. Αν υπάρχουν ορθογώνια διανύσματα με μικρές νόρμες, ο αλγόριθμος θα τα προτιμήσει")
print("3. Η συνθήκη τερματισμού εγγυάται ότι τα διανύσματα είναι όσο το δυνατόν πιο ορθογώνια")
print("4. Σε 2 διαστάσεις, ο αλγόριθμος είναι βέλτιστος και βρίσκει πάντα τα δύο μικρότερα")
print("   γραμμικά ανεξάρτητα διανύσματα του πλέγματος")