import os
import ctypes
import numpy as np
import random

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


def evaluate_by_cfs(dataset_path, population):
    
    # Write population data to a file to the dll read it
    with open('generated-files/HCFS_POPULATION.txt', 'w') as f:
        for row in population:
            f.write(' '.join(map(str, row)) + '\n')

    try:
        # Load the shared library
        merit_dll = ctypes.CDLL('./src/merit.so')  # Adjust the path accordingly

        # Define the argument and return types for the function
        merit_dll.return_cfs.argtypes = [ctypes.c_char_p, ctypes.c_int]
        merit_dll.return_cfs.restype = ctypes.c_int

        # Determine population size
        population_size = len(population)
        dataset_path = bytes(dataset_path, 'utf-8')

        # Call the function
        fitness = merit_dll.return_cfs(dataset_path, population_size)
        print("Fitness:", fitness)

    except OSError as e:
        print("Error:", e)
   


def create_population(population_size: int, default_dataset = False, chromossome_len = 0) -> list[list[int]]:

        len_attributes = chromossome_len
        population = []

        if default_dataset:
            return [[1 for _ in range(len_attributes)] for _ in range(population_size)]

        for _ in range(population_size):
            chromosome = [random.randint(0, 1) for _ in range(len_attributes)]

            # Ensure at least one attributes is selected
            if chromosome.count(1) == 0:
                chromosome[random.randint(0, len_attributes - 1)] = 1

            population.append(chromosome)

        return population


if __name__ == "__main__":

    x = create_population(10, False, 78)

    evaluate_by_cfs("generated-files/best_chromossome_test.arff", x)

