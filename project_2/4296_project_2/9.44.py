def is_prime(n):
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def is_strong_pseudoprime(n, a):
    if n < 2 or n == a:
        return False

    # Γράφουμε n - 1 = 2^r * d με d περιττό
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True

    for _ in range(r - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return True

    return False

def main():
    a = 32
    n = 3
    while True:
        if not is_prime(n) and is_strong_pseudoprime(n, a):
            print(f"Μικρότερος ισχυρός ψευδοπρώτος ως προς τη βάση {a} είναι: {n}")
            break
        n += 2  # εξετάζουμε μόνο περιττούς

if __name__ == "__main__":
    main()
