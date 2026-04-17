import multiprocessing
import time

def worker(duration, result_queue):
    count = 0
    end = time.time() + duration
    while time.time() < end:
        _ = 2 ** 1000000
        count += 1
    result_queue.put(count)
    return

if __name__ == "__main__":
    duration = 30  # seconds
    num_cores = multiprocessing.cpu_count()
    result_queue = multiprocessing.Queue()

    procs = []
    for i in range(num_cores):
        procs.append(multiprocessing.Process(target=worker, args=(duration, result_queue)))

    print("running cpu test")

    start = time.time()
    for p in procs: p.start()
    for p in procs: p.join()
    elapsed = time.time() - start

    results = [result_queue.get() for i in procs]
    total = sum(results)

    print(f"Cores:     {num_cores}")
    print(f"Total ops: {total:,}")
    print(f"Ops/core:  {total // num_cores:,}")
    print(f"Ops/sec:   {int(total / elapsed):,}")

