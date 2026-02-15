import time
import math
#  έλεγχος για πρώτους αριθμούς

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
# Συνάρτηση για τον υπολογισμό του επόμενου τέλειου αριθμού
def next_perfect_number(start_from=8128):
    start_time = time.perf_counter()

    p = 17 # Ξεκινάμε από p = 17 γιατί το p = 13 δίνει το 8128
    while True:
        mersenne = 2**p - 1
        if is_prime(mersenne):
            perfect = 2**(p - 1) * mersenne
            if perfect > start_from:
                end_time = time.perf_counter()
                print(f"Ο επόμενος τέλειος αριθμός > {start_from} είναι: {perfect}")
                print(f"Χρόνος εκτέλεσης: {end_time - start_time:.10f} δευτερόλεπτα")
                return perfect
        p += 1

next_perfect_number()
