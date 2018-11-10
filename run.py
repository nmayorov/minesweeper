import os
import minesweeper
import ctypes as c
from multiprocessing import Process, Queue, Manager

def process(genomes):
    minesweeper.run(os.path.join(os.path.dirname(__file__), 'state'), genomes)

if __name__ == '__main__':
    cores = 16

    manager = Manager()
    genomes = manager.list()

    processes = []

    for i in range(cores):
        p = Process(target=process, args=(genomes,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print("Genomes collected:" + str(len(genomes)))
    print(genomes)
    print("Done!")


# This is a comment to test whether Austin can commit
