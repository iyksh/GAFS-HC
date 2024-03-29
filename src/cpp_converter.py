import os
import ctypes
import numpy as np
import random
import threading
import multiprocessing

def call_nbayes(training_dataset:str, test_dataset:str, result_file:str = './result.arff', mlnp:str = 'n', usf:str = 'y') -> float:
    """Call nbayes function from nbayes.so, read docs/GMNB_2009_Silla.pdf for more information.
    
    `Args:`
        - mlnp (char 'y' or 'n'): Mandatory Leaf Node Prediction
        - usf (char 'y' or 'n'): Usefulness
        - training_dataset (str): path
        - test_dataset (str): path
        - result_file (str): path

    `Returns:`
        - result (float): the result of the nbayes algorithm

    """

    if not os.path.exists('./src/nbayes.so'):
        raise Exception("Error: nbayes.so not found. Please compile the call_nbayes.cpp file.")
    
    if os.name == 'nt':
        raise Exception("Error: nbayes.so is not compatible with Windows, try to compile to nbayes.dll.")

    nbayes_dll = ctypes.CDLL('./src/nbayes.so')

    nbayes_dll.call_nbayes.argtypes = [ctypes.c_char, ctypes.c_char, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    nbayes_dll.call_nbayes.restype = ctypes.c_float

    # Use 'b' to create bytes-like objects 
    mlnp = bytes(mlnp, 'utf-8')
    usf = bytes(usf, 'utf-8')
    training_dataset = bytes(training_dataset, 'utf-8')
    test_dataset = bytes(test_dataset, 'utf-8')
    result_file = bytes(result_file, 'utf-8')

    result = float(nbayes_dll.call_nbayes(mlnp, usf, training_dataset, test_dataset, result_file))
    
    return result


if __name__ == '__main__':
    def run_nbayes(training_dataset:str, test_dataset:str):
        result = call_nbayes(training_dataset, test_dataset)
        print(result)

    if __name__ == '__main__':
        processes = []
                
        datasets = [('generated-files/0/chromossome_train.arff', 'generated-files/0/chromossome_test.arff'),
                    ('generated-files/1/chromossome_train.arff', 'generated-files/1/chromossome_test.arff'),
                    ('generated-files/2/chromossome_train.arff', 'generated-files/2/chromossome_test.arff')]

        for dataset in datasets:
            p = multiprocessing.Process(target=run_nbayes, args=dataset)
            processes.append(p)
            p.start()

        for process in processes:
            process.join()
