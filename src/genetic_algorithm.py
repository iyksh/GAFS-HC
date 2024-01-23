# ==============================================================================
# Main file to manipulate the dataset and the genetic algorithm, and to find the
# best attributes to be selected.
# 
#
# Author: Guilherme Santos
# Last edited: 2023-01-23
# ==============================================================================

from population_manipulator import ClassPopulation, Population
from genetic_operators import *
from dataset import *


class GeneticAlgorithm:
    """
    
    This class is responsible for the genetic algorithm.

    `Constructor:`
    - training_filename: The path of the training file.
    - test_filename: The path of the test file.
    - population_size: The size of the population. `Default: 10`
    - num_generations: The number of generations. `Default: 20`
    - cross_validation: If True, the fitness function will be the cross-validation. `Default: True`

    `Enconding:`
        - binary lists, 0 means that the attribute will not be selected and 1 means that the attribute will be selected.
        - The list will be converted to a .arff file, to be used in the fitness function.

    `Selection:`
        - Tournament Selection, with 2 individuals.

    `Fitness:`
        - GMNB cross-validation (5 folds), if cross_validation=True
        - GMNB only, if cross_validation=False

    `Crossover:`
        - Partially Mapped Crossover (PMX)

    `Mutation`
        - Swap Mutation

    """

    # ==============================================================================
    # Constructor, all the variables and the algorithm are initialized here
    # ==============================================================================

    def __init__(self, test_filepath:str, train_filepath:str, population_size = 10, num_generations = 20, cross_validation = False) -> None:
        
        # Creating the objects
        population = ClassPopulation(test_filepath) # Object that manipulates the population and fitness function 
        operators = genetic_operators() # Object that manipulates the genetic operators
        utils = Utils() # Object that manipulates the utils functions

        utils.clear_screen()                # Clear the terminal screen before the starts
        utils.debug(f"Test file: {population.filepath}") # check if the file is correct
        utils.debug(f"Train file: {train_filepath}") # check if the file is correct

        # Initializing the variables
        self.best_chromosome = (None, 0)    #(chromosome [binary], fitness)
        self.fitness_history = []           #list of the average fitness of each generation, will be used to plot the graph
        self.best_fitness_history = []      #list of the best fitness of each generation, will be used to plot the graph

        

    # ==============================================================================
    # Main loop of the genetic algorithm
    # ==============================================================================        

        population_list = population.create_population(population_size) # Creating the initial population 

        for generation in range(num_generations): # Main loop of the genetic algorithm
            
            population_fitness = population.evaluate_fitness(population_list, train_filepath, cross_validation_check = cross_validation) # Evaluating the fitness of each chromosome
            self.get_history(population_fitness, population_list) # Getting the history of the fitness

            population_list = operators.tournament_selection(population_list, population_fitness) # Selecting the chromosomes to the crossover
            population_list = operators.pmx_crossover(population_list) # Applying the crossover
            population_list = operators.swap_mutation(population_list) # Applying the mutation

            utils.print_population_fitness(population_fitness, generation) # Printing the population fitness

    # ==============================================================================
    # End of the genetic algorithm, some functions are called to plot the graphs
    # ==============================================================================       


        utils.debug(f"Best Chromosome found and saved at ./best_chromossome.arff", type="success")
        population.convert_chromossome_to_file(self.best_chromosome[0], path='./best_chromossome.arff', 
        description = f"Binary Enconding: {self.best_chromosome[0]} \nFitness: {self.best_chromosome[1]}")
        
        operators.check_chromossome(train_filepath, test_filepath) # Checking if the best chromosome is correct
        utils.plot_fitness_history(self.fitness_history) # Plotting the average fitness history
        utils.plot_fitness_history(self.best_fitness_history, title = 'Best-Fitness History') # Plotting the best fitness history


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
        



    