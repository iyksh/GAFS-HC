from src.population_manager import Population
from src.utils import Utils
import multiprocessing
import os

class ThreadsManager:

    def __init__(self, num_threads) -> None:
        self.created_folders = False
        self.num_threads_warning = False
        self.utils = Utils()
        self.num_threads = num_threads

    def first_run(self, population_list: list[list[int]]):
        self.utils.debug(f"Using {self.num_threads} threads", "info")
        self.utils.debug(f"ThreadsManager object created with {self.num_threads} threads")
        self.utils.debug("Max cores available: " + str(multiprocessing.cpu_count()))
        self.utils.debug("First time running the threads, creating the folders", "info")

        for i in range(len(population_list)):
                folder = f"thread_{i}"
                self.create_folder(folder)
        
        self.num_threads_warning = True
        self.created_folders = True



    def create_folder(self, folder_name:str):
        try:
            folder_path = "./generated-files/" + folder_name

            os.mkdir(folder_path)
            self.utils.debug(f"Folder '{folder_path}' created successfully.", "success")

        except FileExistsError:
            return

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



    def cross_validation_threading(self, population_list: list[list[int]], train_filepaths: str, test_filepaths: str) -> list[list[float]]:

        if not self.num_threads_warning:
             self.first_run(population_list)

        population_classes = []    
        for i in range(len(population_list)):
            folder = f"thread_{i}"
            population_classes.append(Population(train_filepaths, test_filepaths, folder))


        # Start the threads

        with multiprocessing.Pool(processes = self.num_threads) as pool:
                results = pool.starmap(self.get_fitness, zip(population_classes, population_list))
        
        results = [item for sublist in results for item in sublist]
        return results



            
