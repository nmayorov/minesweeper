import os
import minesweeper
import ctypes as c
from multiprocessing import Process, Queue, Manager

def process(pid, genomes):
    minesweeper.run(os.path.join(os.path.dirname(__file__), 'state'), pid, genomes)

if __name__ == '__main__':
    # Number of processes to run
    cores = 16

    # Safe shared memory object
    manager = Manager()
    genomes = manager.list()

    processes = []
    pid = 0

    # Start our processes
    for i in range(cores):
        p = Process(target=process, args=(pid,genomes,))
        pid += 1
        processes.append(p)
        p.start()

    # Wait synchronously
    for p in processes:
        p.join()

    # Print out the results
    print("Genomes collected:" + str(len(genomes)))
    print(genomes)
    print("Done!")