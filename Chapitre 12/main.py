import multiprocessing
import random
import time
import os

def generate_random_number():

    num = random.randint(0, 100)

    print(f'PID: {os.getpid()}, Random Number: {num}')
    time.sleep(10)

if __name__ == "__main__":

    processes = []


    for _ in range(5):
        p = multiprocessing.Process(target=generate_random_number)
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print("Tous les processus se sont terminés proprement.")
