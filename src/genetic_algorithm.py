from population_manipulator import Attributes_ClassPopulation, AttributesPopulation
from genetic_operators import *
from dataset import *


class GeneticAlgorithm:
    """
    
    This class is responsible for the genetic algorithm.

    `Constructor:`
    - population_size: The size of the population.
    - num_attributes: The number of attributes that will be selected in each chromosome.
    - training_filename: The path of the training file.
    - test_filename: The path of the test file.

    `Enconding:`
        - binary lists, 0 means that the attribute will not be selected, and 1 means that 

            the gene of the attribute_class will be selected. E.g., [0, 1, 0, 1]

        - The list will be converted to a .arff file, to be used in the fitness function.

    `Selection:`
        - Tournament Selection

    `Fitness:`
        - GMNB cross-validation (5 folds), if cross_validation=True
        - GMNB only, if cross_validation=False

    `Crossover:`
        - Partially Mapped Crossover (PMX)

    `Mutation`
        - Swap Mutation

    """

    def __init__(self, population_size, num_generations, training_filepath, test_filepath, cross_validation = False) -> None:
        
        # Creating the objects
        population = Attributes_ClassPopulation(test_filepath) # Object that manipulates the population and fitness function 
        operators = genetic_operators() # Object that manipulates the genetic operators
        utils = Utils() # Object that manipulates the utils functions

        # Initializing the variables
        self.best_chromosome = (None, 0)    #(chromosome [binary], fitness)
        self.fitness_history = []           #list of the average fitness of each generation, will be used to plot the graph
        self.best_fitness_history = []      #list of the best fitness of each generation, will be used to plot the graph

    #                                                                   #
    #                                                                   #
    #                                                                   #
    #                                                                   #
    #                           MAIN-LOOP                               #
    #                                                                   #
    #                                                                   #
    #                                                                   #
    #                                                                   #
    #                                                                   #

        utils.clear_screen()
        population_list = population.create_population(population_size)

        for generation in range(num_generations):
            
            population_fitness = population.evaluate_fitness(population_list, training_filepath, cross_validation_check = cross_validation)
            if max(population_fitness) > self.best_chromosome[1]:
                index = population_fitness.index(max(population_fitness))
                self.best_chromosome = (population_list[index], population_fitness[index])      
                self.best_fitness_history.append(population_fitness[index])
            else:
                self.best_fitness_history.append(self.best_chromosome[1])     


            self.fitness_history.append(sum(population_fitness) / len(population_fitness))
            #population_list = operators.elitism(population_list, population_fitness, num_elites= 1)
            population_list = operators.tournament_selection(population_list, population_fitness)
            population_list = operators.pmx_crossover(population_list)
            population_list = operators.swap_mutation(population_list)

            utils.print_population_fitness(population_fitness, generation)

        print(f"\n\nBest Chromosome: {self.best_chromosome[0]}")
        population.convert_chromossome_to_file(self.best_chromosome[0], path='./best_chromossome.arff')
        
        utils.check_chromossome(training_filepath)
        utils.plot_fitness_history(self.fitness_history)
        utils.plot_fitness_history(self.best_fitness_history, title = 'Best-Fitness History')




    