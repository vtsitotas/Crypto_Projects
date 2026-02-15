import random
import math
import concurrent.futures
import gmpy2
from gmpy2 import mpz
from functools import partial

def fermat_test(a, n, n_minus_1):
    a = mpz(a)
    if gmpy2.gcd(a, n) != 1:
        return False
    return gmpy2.powmod(a, n_minus_1, n) == 1

def is_probable_prime(n, k=20):
    n = mpz(n)
    if n < 2:
        return False
    
    # Quick check for small primes
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for p in small_primes:
        if n % p == 0:
            return n == p
    
    n_minus_1 = n - 1
    
    # Create a partial function that includes the arguments we need
    test_func = partial(fermat_test, n=n, n_minus_1=n_minus_1)
    
    # Generate all random bases upfront
    random_bases = [random.randint(2, int(n_minus_1)) for _ in range(k)]
    
    # Use ProcessPoolExecutor for CPU-bound task
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(test_func, a) for a in random_bases]
        for future in concurrent.futures.as_completed(futures):
            if not future.result():
                executor.shutdown(wait=False)
                for f in futures:
                    f.cancel()
                return False
    
    return True

def test_large_number():
    base = mpz(3714089895285)
    exp = 60000
    power_of_two = mpz(1) << exp
    n = base * power_of_two - 1

    print("Έλεγχος Fermat για n = base * 2^exp - 1 ...")
    if is_probable_prime(n, k=20):
        print("Πιθανώς ΠΡΩΤΟΣ (με πιθανότητα σφάλματος ~1e-12)")
        sg_candidate = 2 * n + 1
        print(f"Έλεγχος για Sophie Germain prime (μέγεθος: {sg_candidate.bit_length()} bits)...")
        if is_probable_prime(sg_candidate, k=20):
            print("✅ Είναι πιθανώς Sophie Germain prime!")
        else:
            print("❌ ΔΕΝ είναι Sophie Germain prime.")
    else:
        print("Ο αριθμός είναι ΣΥΝΘΕΤΟΣ.")

if __name__ == "__main__":
    # Initialize gmpy2 context for better performance
    test_large_number()