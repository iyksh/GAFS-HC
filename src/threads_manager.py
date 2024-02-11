from src.population_manager import Population
from src.utils import Utils
import multiprocessing
import os

class ThreadsManager:

    def __init__(self) -> None:
        self.created_folders = False
        self.num_threads_warning = False
        self.utils = Utils()

    def create_folder(self, folder_name:str):
        try:
            folder_path = "./generated-files/" + folder_name

            os.mkdir(folder_path)
            self.utils.debug(f"Folder '{folder_path}' created successfully.", "success")

        except FileExistsError:
            self.utils.debug(f"Folder '{folder_path}' already exists, ignoring...", "warning")

        except Exception as e:
                self.utils.debug(f"Error creating the folder '{folder_path}': {e}", "error")


    def get_fitness(self, pop_class: Population, population_list) -> list:
        """
        Calculate the fitness of a chromosome using cross-validation.

        Parameters:
            pop_class (Population): An instance of the Population class.

        Returns:
            list: List of fitness values for the chromosome.
        """
        list_of_lists = [] # List of lists of chromosomes, each list is a fold
        list_of_lists.append(population_list)

        return pop_class.cross_validation(list_of_lists)



    def cross_validation_threading(self, population_list: list[list[int]], train_filepaths: str, test_filepaths: str, num_threads: int = 1) -> list[list[float]]:
        population_classes = []
        num_threads = min(num_threads, len(population_list))

        if not self.num_threads_warning:
            self.utils.debug(f"Using {num_threads} threads", "info")
            self.num_threads_warning = True

        if not self.created_folders:
            self.utils.debug("First time running the threads, creating the folders", "info")
            for i in range(len(population_list)):
                folder = f"thread_{i}"
                self.create_folder(folder)
                population_classes.append(Population(train_filepaths, test_filepaths, folder))
            self.created_folders = True

        else:
            for i in range(len(population_list)):
                folder = f"thread_{i}"
                population_classes.append(Population(train_filepaths, test_filepaths, folder))


        # Start the threads

        while True:

            #start = time.time()

            with multiprocessing.Pool(processes=num_threads) as pool:
                results = pool.starmap(self.get_fitness, zip(population_classes, population_list))
            results = [item for sublist in results for item in sublist]

            #thread_time = time.time() - start


            #start = time.time() 

            #sequential = Population(train_filepaths, test_filepaths)
            #sequential_values = sequential.cross_validation(population_list)

            #sequential_time = time.time() - start
            
            #if results == sequential_values:
                #self.utils.debug("Results are equal", "success")
                #self.utils.debug(f"Threads is {((sequential_time-thread_time)/sequential_time * 100):.2f}% faster than sequential", "success")


            return results
