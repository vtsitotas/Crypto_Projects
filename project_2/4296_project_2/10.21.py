import random
import math
import time
import multiprocessing

def pollard_worker(N, queue):
    if N % 2 == 0:
        queue.put(2)
        return

    f = lambda x: (x * x + 1) % N

    while True:
        x = random.randrange(2, N - 1)
        y = x
        d = 1

        while d == 1:
            x = f(x)
            y = f(f(y))
            d = math.gcd(abs(x - y), N)

        if d != N:
            queue.put(d)
            return

def parallel_pollard(N, num_processes=4):
    manager = multiprocessing.Manager()
    queue = manager.Queue()
    processes = []

    for _ in range(num_processes):
        p = multiprocessing.Process(target=pollard_worker, args=(N, queue))
        p.start()
        processes.append(p)

    divisor = queue.get()

    for p in processes:
        p.terminate()

    return divisor

# ΠΡΕΠΕΙ να τυλιχθεί αυτό το κομμάτι με if __name__ == "__main__":
if __name__ == "__main__":
    multiprocessing.freeze_support()  # Δεν είναι απαραίτητο εδώ, αλλά βοηθά σε frozen apps

    N = 2**257 - 1
    start_time = time.time()
    divisor = parallel_pollard(N, num_processes=8)
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("Ένας μη τετριμμένος διαιρέτης του N είναι:", divisor)
    print("Χρόνος εκτέλεσης: {:.6f} δευτερόλεπτα".format(elapsed_time))
