import numpy as np
import time

def bandwidth_benchmark():
    # large array — well beyond L3 cache size (~1GB)
    arr = np.random.rand(128 * 1024 * 1024)
    DURATION = 30
    count = 0

    end = time.time() + DURATION
    while time.time() < end:
        np.sum(arr)   # read pass
        arr *= 2.0    # write pass
        count += 1

    array_size_gb = arr.nbytes / 1e9
    bytes_per_op = array_size_gb * 2  # one read + one write
    total_gb = count * bytes_per_op
    bandwidth = total_gb / DURATION

    print(f"Bandwidth: {bandwidth:.2f} GB/s")

if __name__ == "__main__":
    print("running memory test")
    bandwidth_benchmark()