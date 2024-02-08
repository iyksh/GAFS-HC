from population_manipulator import Population
import multiprocessing
import time
import os

def create_folder(folder_name:str):
    try:
        folder_path = "./generated-files/" + folder_name

        os.mkdir(folder_path)
        print(f"Folder '{folder_path}' created successfully.")

    except Exception as e:
        if Exception != FileExistsError:
            print(f"An error occurred in create_folder: {e}")


def get_fitness(pop_class: Population, population_list) -> list:
    """
    Calculate the fitness of a chromosome using cross-validation.

    Parameters:
        pop_class (Population): An instance of the Population class.
        *args: Arbitrary arguments.

    Returns:
        list: List of fitness values for the chromosome.
    """
    list_of_lists = [] # List of lists of chromosomes, each list is a fold
    list_of_lists.append(population_list)

    return pop_class.cross_validation(list_of_lists)



def cross_validation_threading(population_list: list[list[int]], train_filepaths: str, test_filepaths: str):
    population_classes = []
    num_threads = len(population_list)

    for i in range(len(population_list)):
        folder = f"thread_{i}"
        create_folder(folder)
        population_classes.append(Population(train_filepaths, test_filepaths, folder))

    while True:

        start = time.time()

        with multiprocessing.Pool(processes=num_threads) as pool:
            results = pool.starmap(get_fitness, zip(population_classes, population_list))

        

        results = [item for sublist in results for item in sublist]

        thread_time = time.time() - start

        print(f"Thread time: {thread_time:.2f} seconds")
        start = time.time() 

        sequential = Population(train_filepaths, test_filepaths)
        sequential_values = sequential.cross_validation(population_list)

        sequential_time = time.time() - start

        print(f"Sequential time: {sequential_time:.2f} seconds")
        
        if results == sequential_values:
            print("Results are equal")


        return results
