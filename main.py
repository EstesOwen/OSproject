import os
import memory
import cpu
import io_test
import json
if(__name__ == "__main__"):
    multiple = input("Would you like to run multiple times?(Y/n): ")
    if(multiple == "y" or multiple == "Y" or multiple == ""):
        #logging stuff
        os.makedirs("logs", exist_ok=True)

        # run multiple times
        runs = int(input("Number of runs: "))

        print()

        # cpu test
        cpu_results = {}
        cores = 0
        total_ops = 0
        ops_per_core = 0
        ops_per_sec = 0
        for i in range(runs):
            print(f"CPU test ({i+1}/{runs})")
            cpu_results[f"Run {i+1}"] = cpu.cpu_main()
            cores += cpu_results[f"Run {i+1}"]["Cores"]
            total_ops += cpu_results[f"Run {i+1}"]["Total Ops"]
            ops_per_core += cpu_results[f"Run {i+1}"]["Ops/core"]
            ops_per_sec += cpu_results[f"Run {i+1}"]["Ops/sec"] 
        cpu_results["Averages"] = {
            "Cores": (cores / runs),
            "Total Ops": (total_ops / runs),
            "Ops/core": (ops_per_core / runs),
            "Ops/sec": (ops_per_sec / runs)
        }
        with open("logs/cpu.json", "w") as f:
            json.dump(cpu_results, f, indent=2)

        # io test
        io_results = {}
        read_total = 0
        read_speed = 0
        write_total = 0
        write_speed = 0
        for i in range(runs):
            print(f"IO test ({i+1}/{runs})")
            io_results[f"Run {i+1}"] = io_test.io_main()
            read_total += io_results[f"Run {i+1}"]["Read Total data(GB)"]
            read_speed += io_results[f"Run {i+1}"]["Read Speed(GB/s)"]
            write_total += io_results[f"Run {i+1}"]["Write Total data(GB)"]
            write_speed += io_results[f"Run {i+1}"]["Write Speed(GB/s)"]
        io_results["Averages"] = {
            "Read Total data(GB)": (read_total/runs),
            "Read Speed(GB/s)": (read_speed/runs),
            "Write Total data(GB)": (write_total/runs),
            "Write Speed(GB/s)": (write_speed/runs)
        }
        with open("logs/io.json", "w") as f:
            json.dump(io_results, f, indent=2)
        
        # memory test
        mem_results = {}
        total_gb = 0
        bandwidth = 0
        for i in range(runs):
            print(f"Memory test ({i+1}/{runs})")
            mem_results[f"Run {i+1}"] = memory.memory_benchmark()
            total_gb += mem_results[f"Run {i+1}"]["Total GB"]
            bandwidth += mem_results[f"Run {i+1}"]["Bandwidth(GB/s)"]
        mem_results["Averages"] = {
            "Total GB": (total_gb / runs),
            "Bandwidth(GB/s)": (bandwidth / runs)
        }
        with open("logs/memory.json", "w") as f:
            json.dump(mem_results, f, indent=2)
    else:
        # run once
        print("CPU Test")
        cpu.cpu_main()
        print("IO Test")
        io_test.io_main()
        print("Memory Test")
        memory.memory_benchmark()