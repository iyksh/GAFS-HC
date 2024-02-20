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

from src.population_manager import Population
from src.threads_manager import ThreadsManager
from src.cfs_hierarchical import CorrelationFeatureSelection
from src.genetic_operators import *
from src.dataset import *

class GeneticAlgorithm:
    """
    
    This class is responsible for the genetic algorithm.

    `Constructor:`
    - test_filepath: The path of the test file
    - train_filepath: The path of the train file
    - population_size: The size of the population
    - num_generations: The number of generations
    - crossover_rate: The rate of the crossover
    - mutation_rate: The rate of the mutation
    - tournament_winner_rate: The rate of the tournament winner
    - timer: The time to check if the user wants to stop the algorithm (Not used anymore, you can stop with ctrl+c)
    - enable_threading: If the threading will be used or not
    - max_parallelism_subprocess: The number of threads to be used
    - HCFS: If the hierarchical CFS will be used or not
    

    `Enconding:`
        - binary lists, 0 means that the attribute will not be selected and 1 means that the attribute will be selected.
        - The list will be converted to a .arff file, to be used in the fitness function.

    `Selection:`
        - Tournament Selection, with 2 individuals.

    `Fitness:`
        - GMNB cross-validation (5 folds)

    `Crossover:`
        - Partially Mapped Crossover (PMX)

    `Mutation`
        - Swap Mutation

    """

    # ==============================================================================
    # Constructor, all the variables and the algorithm are initialized here
    # ==============================================================================

    def __init__(self, test_filepath:str, train_filepath:str, population_size:int, num_generations:int, 
                 crossover_rate:float, mutation_rate:float, tournament_winner_rate:float,
                 enable_threading:bool = True, max_parallelism_subprocess:int = 10, HCFS = True) -> None:
        
        # Creating the objects
        self.population = Population(test_filepath, train_filepath) # Object that manipulates the population and fitness function 
        self.operators = genetic_operators() # Object that manipulates the genetic operators
        self.utils = Utils() # Object that manipulates the utils functions
        self.threads = ThreadsManager() # Object that manipulates the threads
        self.cfs = CorrelationFeatureSelection(train_filepath) # Object that manipulates the hierarchical CFS
        self.num_generations_GMNB = 10

        # Initializing the variables
        self.best_chromosome = (None, 0)    #(chromosome [binary], fitness)
        self.fitness_history = []           #list of the average fitness of each generation, will be used to plot the graph
        self.best_fitness_history = []      #list of the best fitness of each generation, will be used to plot the graph
        self.stop_input = None              #input to check if stops the algorithm
        
        # Saving the parameters
        self.num_generations = num_generations   #number of generations
        self.best_chromosome_GMNB = (None, 0)    #(chromosome [binary], fitness)
        self.test_filepath = test_filepath       #path of the test file
        self.train_filepath = train_filepath     #path of the train file
        self.population_size = population_size   #size of the population
        self.crossover_rate = crossover_rate     #rate of the crossover
        self.mutation_rate = mutation_rate       #rate of the mutation
        self.tournament_winner_rate = tournament_winner_rate #rate of the tournament winner
        self.enable_threading = enable_threading #if the threading will be used or not
        self.max_parallelism_subprocess = max_parallelism_subprocess #number of threads to be used
        self.HCFS = HCFS                        #if the hierarchical CFS will be used or not

        # Debugging the variables before the algorithm starts
        self.utils.clear_screen()                # Clear the terminal screen before the starts
        self.utils.clear_log()                   # Clear the log file before the starts
        self.utils.debug(f"Test file: {self.population.train_filepath}", "info") # check if the file is correct on the object
        self.utils.debug(f"Train file: {self.population.test_filepath}", "info") # check if the file is correct on the object
        self.utils.debug(f"N. of attributes: {len(self.population.test_data.dataset_attributes)}", "info") # check the number of attributes
        self.utils.debug(f"N. of objects: {len(self.population.test_data.dataset_objects)}", "info") # check the number of objects
        self.population.five_folds(train_filepath) # Creating the 5 folds of the train file        
        self.population.five_folds(test_filepath) # Creating the 5 folds of the test file

    # ==============================================================================
    # Genetic Algorithm Global Model Naive Bayes
    #
    # This algorithm uses the GMNB cross-validation to evaluate the fitness of the
    # chromosomes. 
    # ============================================================================== 

    def GMNBwC(self):
        """Genetic Algorithm with the GMNB with cross-validation"""
        self.utils.debug(f"Starting the Genetic Algorithm with GMNB cross-validation", type="info")
        dataset_fitness = self.population.cross_validation(self.population.create_population(1, default_dataset = True), sequential_run = True) # Check if the cross-validation is working
        population_list = self.population.create_population(self.population_size) # Creating the initial population 

        self.start_time = time.time() # Start the timer to check the time of the algorithm
        for generation in range(self.num_generations): # Main loop of the genetic algorithm
            
            try:
                generation_start_time = time.time()

                population_fitness = self.population.cross_validation(population_list) # Evaluating the fitness of each chromosome
                self.get_history(population_fitness, population_list) # Getting the history of the fitness

                population_list = self.operators.tournament_selection(population_list, population_fitness, k = self.tournament_winner_rate) # Selection
                population_list = self.operators.pmx_crossover(population_list, self.crossover_rate) # Applying the crossover
                population_list = self.operators.swap_mutation(population_list, self.mutation_rate) # Applying the mutation
                generation_end_time = time.time()

                self.utils.print_population_fitness(population_fitness, generation, self.num_generations, generation_start_time, generation_end_time) # Printing the population fitness
                
                

            except KeyboardInterrupt:
                self.utils.debug(f"Stopped at generation {generation}", type="info")
                processes = multiprocessing.active_children()  # Corrected here
                for process in processes:
                    process.terminate()

                break   

        self.end_time = time.time() # End the timer to check the time of the algorithm
        self.show_results("GMNBwC", dataset_fitness, self.best_chromosome, self.end_time, self.start_time, population_fitness, 
                          self.best_fitness_history, self.fitness_history)
        


    # ==============================================================================
    # Genetic Algorithm Global Model Naive Bayes with Parallelism
    #
    # This algorithm uses the GMNB cross-validation to evaluate the fitness of the
    # chromosomes, with CPU Parallelism.
    # ============================================================================== 

    def GMNBwPC(self):
        """Genetic Algorithm with the GMNB with CPU Parallelism cross-validation"""
        self.utils.debug(f"Starting the Genetic Algorithm with GMNB with Parallel cross-validation", type="info")
        dataset_fitness = self.population.cross_validation(self.population.create_population(1, default_dataset = True), sequential_run = True) # Check if the cross-validation is working
        population_list = self.population.create_population(self.population_size) # Creating the initial population 

        self.start_time = time.time() # Start the timer to check the time of the algorithm
        for generation in range(self.num_generations): # Main loop of the genetic algorithm
            
            try:
                generation_start_time = time.time()

                population_fitness = self.threads.cross_validation_multiprocessing(population_list, self.train_filepath, self.test_filepath, self.max_parallelism_subprocess) # Evaluating the fitness of each chromosome            
                self.get_history(population_fitness, population_list) # Getting the history of the fitness

                population_list = self.operators.tournament_selection(population_list, population_fitness, k = self.tournament_winner_rate) # Selection
                population_list = self.operators.pmx_crossover(population_list, self.crossover_rate) # Applying the crossover
                population_list = self.operators.swap_mutation(population_list, self.mutation_rate) # Applying the mutation
                generation_end_time = time.time()

                self.utils.print_population_fitness(population_fitness, generation, self.num_generations, generation_start_time, generation_end_time) # Printing the population fitness
                
            except KeyboardInterrupt:
                self.utils.debug(f"Stopped at generation {generation}", type="info")
                processes = multiprocessing.active_children()  # Corrected here
                for process in processes:
                    process.terminate()

                break   

        self.end_time = time.time() # End the timer to check the time of the algorithm
        self.show_results("GMNBwPC", dataset_fitness, self.best_chromosome, self.end_time, self.start_time, population_fitness, 
                          self.best_fitness_history, self.fitness_history)
        
    # ==============================================================================
    # Genetic Algorithm Global Model Naive Bayes with Parallelism
    #
    # This algorithm uses the GMNB cross-validation to evaluate the fitness of the
    # chromosomes, with CPU Parallelism.
    # ============================================================================== 

    def HCFSwGMNBwPC(self, GMNB_generations = 10):
        """Hierarchical CFS with GMNB with Parallel cross-validation
        - Function set to 10 generations using GMNB and the rest using HCFS"""

        self.utils.debug(f"Starting the Genetic Algorithm with Hierarchical CFS and GMNB with Parallel cross-validation", type="info")
        dataset_fitness = self.population.cross_validation(self.population.create_population(1, default_dataset = True), sequential_run = True) # Check if the cross-validation is working
        population_list = self.population.create_population(self.population_size) # Creating the initial population 

        self.start_time = time.time() # Start the timer to check the time of the algorithm
        
        for generation in range(self.num_generations): # Main loop of the genetic algorithm
            
            try:
                generation_start_time = time.time()

                if generation < GMNB_generations: # Using GMNB for the first x generations
                    population_fitness = self.threads.cross_validation_multiprocessing(population_list, self.train_filepath, self.test_filepath, self.max_parallelism_subprocess) # Evaluating the fitness of each chromosome            
                
                else: # Using HCFS for the rest of the generations

                    pass
                
                self.get_history(population_fitness, population_list) # Getting the history of the fitness
                population_list = self.operators.tournament_selection(population_list, population_fitness, k = self.tournament_winner_rate) # Selection
                population_list = self.operators.pmx_crossover(population_list, self.crossover_rate) # Applying the crossover
                population_list = self.operators.swap_mutation(population_list, self.mutation_rate) # Applying the mutation
                generation_end_time = time.time()

                self.utils.print_population_fitness(population_fitness, generation, self.num_generations, generation_start_time, generation_end_time) # Printing the population fitness
                
            except KeyboardInterrupt:
                self.utils.debug(f"Stopped at generation {generation}", type="info")
                processes = multiprocessing.active_children()  # Corrected here
                for process in processes:
                    process.terminate()

                break   

        self.end_time = time.time() # End the timer to check the time of the algorithm
        self.show_results("HCFSwGMNBwPC", dataset_fitness, self.best_chromosome, self.end_time, self.start_time, population_fitness, 
                          self.best_fitness_history, self.fitness_history)

    # ==============================================================================
    # Uselful functions
    #
    # This functions are used to show the results of the algorithm
    # Or to get the history of the best fitness and the average fitness
    # ============================================================================== 
    
    def show_results(self, type_of_algorithm:str, dataset_fitness:tuple, best_chromosome:tuple, end_time:float, start_time:float, population_fitness:list, best_fitness_history:list, fitness_history:list) -> None:
        
        self.population.convert_chromossome_to_file(best_chromosome[0], self.population.test_filepath, type="best_chromossome_test") # Saving the best chromosome in a file
        self.population.convert_chromossome_to_file(best_chromosome[0], self.population.train_filepath, type="best_chromossome_train") # Saving the best chromosome in a file
        porcentage_better = ((dataset_fitness[0] - best_chromosome[1]) / dataset_fitness[0] * 100) * - 1
        
        self.utils.debug(f"The algorithm took {(end_time - start_time):.2f} seconds to run", type="success")
        self.utils.debug(f"Best Chromosome saved at ./best_chromossome.arff", type="success")
        self.utils.debug(f"Default Dataset fitness: {dataset_fitness[0]}", "info") # check if the cross-validation is working
        self.utils.debug(f"{type_of_algorithm} Best Chromosome Fitness: {best_chromosome[1]}", type="success")
        self.utils.debug(f"Number of at tributes selected with {type_of_algorithm}: {sum(best_chromosome[0])}", type="success")
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

    
        







    