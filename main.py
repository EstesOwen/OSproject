import os
if(__name__ == "__main__"):
    multiple = input("Would you like to run multiple times?(Y/n): ")
    if(multiple == "y" or multiple == "Y" or multiple == ""):
        # run multiple times
        runs = int(input("Number of runs: "))
        for i in range(runs):
            pass
    else:
        os.system("python3 cpu.py && python3 memory.py && python3 io.py")