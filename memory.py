import numpy as np
import multiprocessing
import time

def worker(duration, result_queue):
    # big array
    big_array = np.random.rand(32 * 1024 * 1024)
    count = 0
    end = time.time() + duration
    while time.time() < end:
        np.sum(big_array)
        big_array *= 2.0
        count += 1
    result_queue.put(count)

if __name__ == "__main__":
    duration = 30
    arraySize = 0.256
    num_cores = multiprocessing.cpu_count()
    result_queue = multiprocessing.Queue()

    print("running memory test")

    procs = []
    for i in range(num_cores):
        procs.append(multiprocessing.Process(target=worker, args=(duration, result_queue)))
    
    for p in procs: p.start()
    for p in procs: p.join()

    results = [result_queue.get() for i in procs]
    total_ops = sum(results)

    # each op does one read pass and one write
    bytes_per_op = arraySize * 2 * 1e9
    total_bytes = total_ops * bytes_per_op
    bandwidth_gb = total_bytes / (duration * 1e9)

    print(f"Total ops:       {total_ops:,}")
    print(f"Bandwidth:       {bandwidth_gb:.2f} GB/s")
