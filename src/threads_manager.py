from src.population_manager import Population
from src.utils import Utils
import multiprocessing
import os

class ThreadsManager:
    def __init__(self) -> None:
        self.created_folders = False
        self.utils = Utils()

    def first_run(self, population_list: list[list[int]]):        
        self.utils.debug("Max cores available: " + str(multiprocessing.cpu_count()))
        self.utils.debug("First time running the threads, creating the folders", "info")

        for i in range(len(population_list)):
            folder = f"thread_{i}"
            self.create_folder(folder)

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
        list_of_lists = [] # List of lists of chromosomes, each list is a fold
        list_of_lists.append(population_list)
        return pop_class.cross_validation(list_of_lists)

    def process_population(self, population_class, population, result_queue):
        result_queue.put(self.get_fitness(population_class, population))

    def cross_validation_threading(self, population_list: list[list[int]], train_filepaths: str, test_filepaths: str) -> list[list[float]]:
        if not self.created_folders:
             self.first_run(population_list)

        population_classes = []    
        for i in range(len(population_list)):
            folder = f"thread_{i}"
            population_classes.append(Population(train_filepaths, test_filepaths, folder))

        # Use multiprocessing Process
        result_queue = multiprocessing.Queue()
        processes = []

        for pop_class, population in zip(population_classes, population_list):
            process = multiprocessing.Process(target=self.process_population, args=(pop_class, population, result_queue))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

        results = []
        while not result_queue.empty():
            results.extend(result_queue.get())

        return results
