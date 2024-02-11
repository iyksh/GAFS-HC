# ==============================================================================
# Main file to manipulate the dataset and the genetic algorithm, and to find the
# best attributes to be selected.
# 
#
# Author: Guilherme Santos
# Last edited: 2023-01-23
# ==============================================================================

import threading
import time

from src.population_manager import Population
from src.threads_manager import ThreadsManager
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
    - timer: The time to check if the user wants to stop the algorithm
    - num_threads: The number of threads to be used
    - enable_threading: If the threading will be used or not
    

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
                 crossover_rate:float, mutation_rate:float, tournament_winner_rate:float, timer:int = 5, num_threads:int = 1,
                 enable_threading:bool = True) -> None:
        
        # Creating the objects
        population = Population(test_filepath, train_filepath) # Object that manipulates the population and fitness function 
        operators = genetic_operators() # Object that manipulates the genetic operators
        self.utils = Utils() # Object that manipulates the utils functions
        self.threads = ThreadsManager() # Object that manipulates the threads

        # Initializing the variables
        self.best_chromosome = (None, 0)    #(chromosome [binary], fitness)
        self.fitness_history = []           #list of the average fitness of each generation, will be used to plot the graph
        self.best_fitness_history = []      #list of the best fitness of each generation, will be used to plot the graph
        self.timer = timer                  #timer to check if stops the algorithm
        self.stop_input = None              #input to check if stops the algorithm
        self.num_generations = num_generations #number of generations

        # Debugging the variables before the algorithm starts
        self.utils.clear_screen()                # Clear the terminal screen before the starts
        self.utils.clear_log()
        self.utils.debug(f"Test file: {population.train_filepath}", "info") # check if the file is correct on the object
        self.utils.debug(f"Train file: {population.test_filepath}", "info") # check if the file is correct on the object
        self.utils.debug(f"N. of attributes: {len(population.test_data.dataset_attributes)}", "info") # check the number of attributes
        self.start_time = time.time() # Start the timer to check the time of the algorithm

    # ==============================================================================
    # Main loop of the genetic algorithm
    # ==============================================================================
        population.five_folds(train_filepath) # Creating the 5 folds of the train file        
        population.five_folds(test_filepath) # Creating the 5 folds of the test file
        

        population_list = population.create_population(population_size) # Creating the initial population 

        for generation in range(num_generations): # Main loop of the genetic algorithm
            start = time.time()

            if enable_threading:
                population_fitness = self.threads.cross_validation_threading(population_list, train_filepath, test_filepath, num_threads) # Evaluating the fitness of each chromosome            
            else:
                population_fitness = population.cross_validation(population_list)
            
            
            self.get_history(population_fitness, population_list) # Getting the history of the fitness

            population_list = operators.tournament_selection(population_list, population_fitness, k= tournament_winner_rate) # Selection
            population_list = operators.pmx_crossover(population_list, crossover_rate) # Applying the crossover
            population_list = operators.swap_mutation(population_list, mutation_rate) # Applying the mutation

            self.utils.print_population_fitness(population_fitness, generation) # Printing the population fitness
            
            end = time.time()

            if self.stop_check(generation, start, end): #checking if the user wants to stop the algorithm
                break


    # ==============================================================================
    # End of the genetic algorithm, some functions are called to plot the graphs
    # ==============================================================================       

        self.end_time = time.time() # End the timer to check the time of the algorithm
        self.utils.debug(f"The algorithm took {(self.end_time - self.start_time):.2f} seconds to run", type="info")
        self.utils.debug(f"Best Chromosome found and saved at ./best_chromossome.arff", type="success")

        population.convert_chromossome_to_file(self.best_chromosome[0], population.test_filepath, type="best_chromossome_test") # Saving the best chromosome in a file
        population.convert_chromossome_to_file(self.best_chromosome[0], population.train_filepath, type="best_chromossome_train") # Saving the best chromosome in a file

        operators.check_chromossome(train_filepath, test_filepath) # Checking if the best chromosome is correct
        self.utils.plot_fitness_history(self.fitness_history) # Plotting the average fitness history
        self.utils.plot_fitness_history(self.best_fitness_history, title = 'Best-Fitness History') # Plotting the best fitness history

        self.utils.debug(f"Number of attributes selected: {sum(self.best_chromosome[0])}", type="info")
        


    # ==============================================================================
    # Functions 
    # ============================================================================== 
        
    def get_history(self, population_fitness, population_list): # Function to get the history of the best fitness and the average fitness
        if max(population_fitness) > self.best_chromosome[1]:
            index = population_fitness.index(max(population_fitness))
            self.best_chromosome = (population_list[index], population_fitness[index])      
            self.best_fitness_history.append(population_fitness[index])
        else:
            self.best_fitness_history.append(self.best_chromosome[1])     


        self.fitness_history.append(sum(population_fitness) / len(population_fitness))

    def get_user_input(self):
        self.stop_input = str(input())
        
    def stop_check(self, generation, start, end) -> bool:
        self.utils.debug(f"Generation {generation} took {(end - start):.2f} seconds")
        hours_finish = (end - start) * (self.num_generations - generation) / 3600
        minutes_finish = (hours_finish - int(hours_finish)) * 60

        self.utils.debug(f"Approximate time to finish: {hours_finish:.2f} hours and {minutes_finish:.2f} minutes")

        if self.timer == 0:
            return False

        #check if the user wants to stop
        self.utils.debug(f"Stop at generation {generation}? (y/n)")
        thread = threading.Thread(target=self.get_user_input)
        thread.start()

        # Wait for the thread to finish or the specified time to elapse
        thread.join(self.timer)

        # Check the user input
        if self.stop_input == 'y':
            self.utils.debug(f"Stopped at generation {generation}", type="info")
            return True
            
        return False




    