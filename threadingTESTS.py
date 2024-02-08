from src.call_nbayes import *
from src.dataset import DatasetManipulator
import multiprocessing
import time
import os

def call_nbayes_wrapper(args) -> list:
    train_filepath, test_filepath = args
    result = call_nbayes(train_filepath, test_filepath)
    if result == -1:
        print(f"Error in {train_filepath} and {test_filepath}")

    return result

def call_threaded(train_filepaths, test_filepaths):
    while True:
        num_threads = len(train_filepaths)
        with multiprocessing.Pool(processes=num_threads) as pool:
            results = pool.map(call_nbayes_wrapper, zip(train_filepaths, test_filepaths))

        return results



if __name__ == "__main__":
    os.system("clear")

    train_filepaths = [
        "/home/yksh/Desktop/Bases particionadas/bases_particionadas/CellCycle/10-folds/fold0/CellCycle_train.arff",
        "/home/yksh/Desktop/Bases particionadas/bases_particionadas/CellCycle/10-folds/fold1/CellCycle_train.arff",
        "/home/yksh/Desktop/Bases particionadas/bases_particionadas/CellCycle/10-folds/fold2/CellCycle_train.arff",
        "/home/yksh/Desktop/Bases particionadas/bases_particionadas/CellCycle/10-folds/fold3/CellCycle_train.arff",
        "/home/yksh/Desktop/Bases particionadas/bases_particionadas/CellCycle/10-folds/fold4/CellCycle_train.arff",
        "/home/yksh/Desktop/Bases particionadas/bases_particionadas/CellCycle/10-folds/fold5/CellCycle_train.arff",
        "/home/yksh/Desktop/Bases particionadas/bases_particionadas/CellCycle/10-folds/fold6/CellCycle_train.arff",
        "/home/yksh/Desktop/Bases particionadas/bases_particionadas/CellCycle/10-folds/fold7/CellCycle_train.arff",
        "/home/yksh/Desktop/Bases particionadas/bases_particionadas/CellCycle/10-folds/fold8/CellCycle_train.arff",
        "/home/yksh/Desktop/Bases particionadas/bases_particionadas/CellCycle/10-folds/fold9/CellCycle_train.arff",
    ]

    test_filepaths = [
        "/home/yksh/Desktop/Bases particionadas/bases_particionadas/CellCycle/10-folds/fold0/CellCycle_test.arff",
        "/home/yksh/Desktop/Bases particionadas/bases_particionadas/CellCycle/10-folds/fold1/CellCycle_test.arff",
        "/home/yksh/Desktop/Bases particionadas/bases_particionadas/CellCycle/10-folds/fold2/CellCycle_test.arff",
        "/home/yksh/Desktop/Bases particionadas/bases_particionadas/CellCycle/10-folds/fold3/CellCycle_test.arff",
        "/home/yksh/Desktop/Bases particionadas/bases_particionadas/CellCycle/10-folds/fold4/CellCycle_test.arff",
        "/home/yksh/Desktop/Bases particionadas/bases_particionadas/CellCycle/10-folds/fold5/CellCycle_test.arff",
        "/home/yksh/Desktop/Bases particionadas/bases_particionadas/CellCycle/10-folds/fold6/CellCycle_test.arff",
        "/home/yksh/Desktop/Bases particionadas/bases_particionadas/CellCycle/10-folds/fold7/CellCycle_test.arff",
        "/home/yksh/Desktop/Bases particionadas/bases_particionadas/CellCycle/10-folds/fold8/CellCycle_test.arff",
        "/home/yksh/Desktop/Bases particionadas/bases_particionadas/CellCycle/10-folds/fold9/CellCycle_test.arff",

    ]

        
    time_start = time.time()
    threads_values = call_threaded(train_filepaths, test_filepaths)    
    Thread_time = time.time() - time_start

    time_start = time.time()
    sequential_values = []
    for i in range(len(train_filepaths)):
        sequential_values.append(call_nbayes(train_filepaths[i], test_filepaths[i]))
    Sequential_time = time.time() - time_start


    percentage = (Thread_time - Sequential_time) / Sequential_time * 100
    print(f"Threaded execution took {Thread_time:.2f} seconds")
    print(f"Sequential execution took {Sequential_time:.2f} seconds")
    print(f"Threaded execution was {percentage:.2f}% faster than Sequential execution")

    print("Threaded values are equal to sequential values: ", threads_values == sequential_values)