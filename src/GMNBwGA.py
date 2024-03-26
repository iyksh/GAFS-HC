# ==============================================================================
# Main file to manipulate the dataset and the genetic algorithm, and to find the
# best attributes to be selected.
# 
#
# Author: Guilherme Santos
# Last edited: 2023-02-18
# ==============================================================================

import time
import multiprocessing

from src.cross_validation import CrossValidation
from src.genetic_operators import *
from src.dataset import *

class GeneticAlgorithm:
    """
    This class is responsible for the genetic algorithm.
    """

    # ==============================================================================
    # Constructor, all the variables and the algorithm are initialized here
    # ==============================================================================

    def __init__(self, dataset_path: str, population_size:int, num_generations:int, 
                 crossover_rate:float, mutation_rate:float, tournament_winner_rate:float) -> None:
        
        # Creating the objects
        self.operators = genetic_operators() # Object that manipulates the genetic operators
        self.utils = Utils() # Object that manipulates the utils functions
        self.dataset = Dataset(dataset_path) # Object that manipulates the dataset
        
        self.cv = CrossValidation(dataset_path) # Object that manipulates the population
        self.num_attributes = len(self.dataset.dataset_attributes) - 1 # Number of attributes - attribute class
  

        # Initializing the variables
        self.best_chromosome = (None, 0)    #(chromosome [binary], fitness)
        self.fitness_history = []           #list of the average fitness of each generation, will be used to plot the graph
        self.best_fitness_history = []      #list of the best fitness of each generation, will be used to plot the graph
        self.num_objects = len(self.dataset.dataset_objects) # Number of objects in the dataset
        
        # Saving the parameters
        self.dataset_path = dataset_path         #path of the dataset
        self.num_generations = num_generations   #number of generations
        self.population_size = population_size   #size of the population
        self.crossover_rate = crossover_rate     #rate of the crossover
        self.mutation_rate = mutation_rate       #rate of the mutation
        self.tournament_winner_rate = tournament_winner_rate #rate of the tournament winner

        # Debugging the variables before the algorithm starts
        self.utils.clear_screen()                # Clear the terminal screen before the starts
        self.utils.debug(f"N. of attributes: {self.num_attributes} | N. of objects: {self.num_objects}", "info") # check the number of attributes

    # ==============================================================================
    # Genetic Algorithm Global Model Naive Bayes with Parallelism
    #
    # This algorithm uses the GMNB cross-validation to evaluate the fitness of the
    # chromosomes, with CPU Parallelism.
    # ============================================================================== 

    def run(self):
        """Genetic Algorithm with the GMNB with CPU Parallelism cross-validation"""
        
        self.utils.debug(f"Starting the Global Model Naive Bayes with Genetic Algorithm", type="info")
        dataset_fitness = self.cv.cross_validation([[1] * self.num_attributes])
        population_list = self.operators.create_population(self.population_size, self.num_attributes) # Creating the initial population
        self.utils.debug(f"Dataset hF: {dataset_fitness[0]:.5f} \n", type="info")
        
        
        self.start_time = time.time() # Start the timer to check the time of the algorithm
        for generation in range(self.num_generations): # Main loop of the genetic algorithm
            
            try:
                generation_start_time = time.time()

                population_fitness = self.cv.cross_validation(population_list) # Evaluating the fitness of each chromosome
                self.get_history(population_fitness, population_list) # Getting the history of the fitness

                population_list = self.operators.tournament_selection(population_list, population_fitness, k = self.tournament_winner_rate) # Selection
                population_list = self.operators.pmx_crossover(population_list, self.crossover_rate) # Applying the crossover
                population_list = self.operators.swap_mutation(population_list, self.mutation_rate) # Applying the mutation

                
                # Information to show the progress of the algorithm
                generation_end_time = time.time()
                time_estimated = (generation_end_time - generation_start_time) * (self.num_generations - generation)
                progress = f"\033[1;35m" + "[Debug]: " + "\033[0m" + f"Progress {generation + 1}/{self.num_generations} | Time estimated: {(time_estimated):.2f} seconds" + "\033[0m"
                print(f"\33[2K\r{progress}", end= "\r")
                
            except KeyboardInterrupt:
                self.utils.debug(f"\nStopped at generation {generation}", type="info")
                processes = multiprocessing.active_children()  # Corrected here
                for process in processes:
                    process.terminate()

                break   

        self.end_time = time.time() # End the timer to check the time of the algorithm
        self.show_results("GMNBwPC", dataset_fitness, self.best_chromosome)
               

    # ==============================================================================
    # Uselful functions
    #
    # This functions are used to show the results of the algorithm
    # Or to get the history of the best fitness and the average fitness
    # ============================================================================== 
     
    def show_results(self, type_of_algorithm:str, dataset_fitness:tuple, best_chromosome:tuple) -> None:
    
        porcentage_better = ((dataset_fitness[0] - best_chromosome[1]) / dataset_fitness[0] * 100) * - 1
        self.utils.debug(f"The algorithm found a solution {porcentage_better:.2f}% better than the dataset fitness, using {type_of_algorithm}", type="success")

        self.utils.plot_fitness_history(self.fitness_history, title = f'Fitness History {type_of_algorithm}')
        self.utils.plot_fitness_history(self.best_fitness_history, title = f'{type_of_algorithm} Best-Fitness History') # Plotting the best fitness history


    def get_history(self, population_fitness, population_list): # Function to get the history of the best fitness and the average fitness   
        
        if max(population_fitness) > self.best_chromosome[1]:
            index = population_fitness.index(max(population_fitness))
            self.best_chromosome = (population_list[index], population_fitness[index])      
            self.best_fitness_history.append(population_fitness[index])
        else:
            self.best_fitness_history.append(self.best_chromosome[1])     

        self.fitness_history.append(sum(population_fitness) / len(population_fitness))



        







    