import os
import time
import multiprocessing

FILE_SIZE = 1 * 1024 * 1024 * 1024  # a gig
CHUNK_SIZE = 4 * 1024 * 1024
DURATION = 30

def write_worker(duration, file_path, result_queue):
    data = os.urandom(CHUNK_SIZE)  # just fill it with random stuff
    bytes_written = 0
    end = time.time() + duration

    with open(file_path, 'wb') as f:
        while time.time() < end:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())  # force write to disk because i dont want errors
            bytes_written += CHUNK_SIZE

    result_queue.put(bytes_written)

def read_worker(duration, file_path, result_queue):
    bytes_read = 0
    end = time.time() + duration

    with open(file_path, 'rb') as f:
        while time.time() < end:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                f.seek(0)  # back to start when file ends
                continue
            bytes_read += len(chunk)

    result_queue.put(bytes_read)

def run_benchmark(label, worker_fn, file_path, num_workers, duration):
    result_queue = multiprocessing.Queue()

    procs = []
    for i in range(num_workers):
        procs.append(multiprocessing.Process(target=worker_fn, args=(duration, f"{file_path}_{i}", result_queue)))

    # print(f"\nRunning {label} benchmark")
    start = time.time()
    for p in procs: p.start()
    for p in procs: p.join()
    elapsed = time.time() - start

    total_bytes = sum(result_queue.get() for _ in procs)
    speed_mb = (total_bytes / elapsed) / (1024 * 1024)
    speed_gb = speed_mb / 1024

    # print(f"  Workers:    {num_workers}")
    # print(f"  Total data: {total_bytes / (1024**3):.2f} GB")
    # print(f"{label} Speed: {speed_gb:.2f} GB/s")
    return [(total_bytes / (1024**3)),(speed_gb)]

def cleanup(file_path, num_workers):
    os.system(f"rm {file_path}_*")

def io_main():
    path = "./LOAD_BEARING_FILE"
    workers = 4

    # make files
    # cleanup(path, workers)
    write_output = run_benchmark("WRITE", write_worker, path, workers, DURATION)

    # read files
    read_output = run_benchmark("READ", read_worker, path, workers, DURATION)

    # get rid of files
    cleanup(path, workers)
    # print("\ngot rid of the files")

    output = {
        "Read Total data(GB)": read_output[0],
        "Read Speed(GB/s)": read_output[1],
        "Write Total data(GB)": write_output[0],
        "Write Speed(GB/s)": write_output[1]
    }
    return output

if(__name__ == "__main__"):
    io_main()
