from src.call_nbayes import *
import multiprocessing
import time
import os

def call_nbayes_wrapper(train_filepath, test_filepath):
    result = call_nbayes(train_filepath, test_filepath)
    return result

if __name__ == "__main__":
    os.system("clear")

    train_filepaths = [
        "generated-files/chromossome_train_1.arff", 

   


    ]

    test_filepaths = [
        "generated-files/chromossome_test_1.arff", 




    ]

    time_start = time.time()

    pool = multiprocessing.Pool(processes=len(train_filepaths))
    results = pool.starmap(call_nbayes_wrapper, zip(train_filepaths, test_filepaths))
    pool.close()
    pool.join()

    for result in results:
        print(result)

    Thread_time = time.time() - time_start
    print("Time taken Threaded: ", Thread_time)

    time_start = time.time()

    # Sequential execution
    for i in range(len(train_filepaths)):
        print(call_nbayes(train_filepaths[i], test_filepaths[i]))

    Sequential_time = time.time() - time_start
    print("Time taken Sequential: ", Sequential_time)

    percentage = (Thread_time - Sequential_time) / Sequential_time * 100
    print(f"Threaded execution was {percentage:.2f}% faster than Sequential execution")

    print((4.10-2.26)/2.26*100)