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
from src.neural_network import NeuralNetwork

class NNwGeneticAlgorithm:
    """
    This class is responsible for algorithm.

    """

    # ==============================================================================
    # Constructor, all the variables and the algorithm are initialized here
    # ==============================================================================

    def __init__(self, dataset_path: str, population_size:int, num_generations:int, 
                 crossover_rate:float, mutation_rate:float, tournament_winner_rate:float,
                 save_model = False, save_path = "", load_model = False,
                 load_path = "", GMNB_generations = 10, train_epochs = 10000) -> None:
        
        # Creating the objects
        self.operators = genetic_operators() # Object that manipulates the genetic operators
        self.utils = Utils() # Object that manipulates the utils functions
        self.dataset = Dataset(dataset_path) # Object that manipulates the dataset
        
        self.cv = CrossValidation(dataset_path) # Object that manipulates the cross-validation
        self.num_attributes = len(self.dataset.dataset_attributes) - 1 # Number of attributes - attribute class
        self.NN = NeuralNetwork(self.num_attributes)# Object that manipulates the Neural Network     
        
        # Initializing the variables
        self.num_generations_GMNB = GMNB_generations # Number of generations to use GMNB
        self.best_chromosome = (None, 0)    #(chromosome [binary], fitness)
        self.fitness_history = []           #list of the average fitness of each generation, will be used to plot the graph
        self.best_fitness_history = []      #list of the best fitness of each generation, will be used to plot the graph
        self.neuralNetwork_data = "generated-files/train_data.txt" #path of the file to save the train data
        self.num_objects = len(self.dataset.dataset_objects) # Number of objects in the dataset
        
        # Saving the parameters
        self.dataset_path = dataset_path         #path of the dataset
        self.num_generations = num_generations   #number of generations
        self.best_chromosome_GMNB = (None, 0)    #(chromosome [binary], fitness)
        self.population_size = population_size   #size of the population
        self.crossover_rate = crossover_rate     #rate of the crossover
        self.mutation_rate = mutation_rate       #rate of the mutation
        self.tournament_winner_rate = tournament_winner_rate #rate of the tournament winner
        self.save_model = save_model             #if the model will be saved or not
        self.save_model_path = save_path               #path to save the model
        self.load_model = load_model             #if the model will be loaded or not
        self.load_path = load_path               #path to load the model
        self.GMNB_generations = GMNB_generations #number of generations to use GMNB
        self.train_epochs = train_epochs         #number of epochs to train the Neural Network
        

        # Debugging the variables before the algorithm starts
        self.utils.debug(f"N. of attributes: {self.num_attributes} | N. of objects: {self.num_objects}", "info") # check the number of attributes
        self.utils.debug(f"Will be generated {self.GMNB_generations * self.population_size} models using GMNB to train data", "info") # check the number of models to be generated
          
    # ==============================================================================
    # Genetic Algorithm Global Model Naive Bayes with Parallelism and Neural Networks
    #
    # This algorithm uses the GMNB cross-validation to evaluate the fitness of the
    # chromosomes, with CPU Parallelism, after thatt, will use Neural Networks to
    # evaluate the fitness of the best chromosomes.
    # ============================================================================== 

    def run(self):
        
        """Neural Networks with GMNB with Parallel cross-validation"""
        self.start_time = time.time() # Start the timer to check the time of the algorithm
        
        #dataset_fitness = self.cv.cross_validation([[1] * self.num_attributes])
        save_train_data, model_trained = True, False
        
        dataset_fitness = (0,0) # if you want to skip the GMNB
        self.utils.debug(f"Train Save model: {self.save_model} | Load model: {self.load_model} | Dataset hF: {dataset_fitness[0]:.5f} \n", type="info")
        population_list = self.operators.create_population(self.population_size, self.num_attributes) # Creating the initial population
        
        
        for generation in range(self.num_generations): # Main loop of the genetic algorithm
            
            try:
                generation_start_time = time.time()

                if generation < self.GMNB_generations: # Using GMNB for the first x generations, run at least one time
                
                        try:
                            population_list = self.operators.create_population(self.population_size, self.num_attributes)  
                            population_fitness = self.cv.cross_validation(population_list) # Evaluating the fitness of each chromosome 
                            
                            progress = "\033[1;34m[Database Creation Progress]: " + "\033[0m" + "{:.2f}%".format((generation+1)/self.GMNB_generations * 100)
                            time_estimated = "\033[0m" + "| Estimated time: {:.2f} seconds".format((time.time() - generation_start_time) * (self.GMNB_generations - generation))
                            
                            self.get_history(population_fitness, population_list, save_train_data, progress, time_estimated)
                        
                        except KeyboardInterrupt:
                            self.utils.debug(f"\033[1;34m\nStopped the Database Creation at generation {generation}\n", type="info")
                            processes = multiprocessing.active_children()
                            for process in processes:
                                process.terminate()
                                
                            self.GMNB_generations = 0
                    
                else: # Using NN for the rest of the generations
                    if not model_trained and self.load_model:
                        self.NN.load_nn(self.load_path)
                        model_trained = True
                        save_train_data = False # Saving the train data only with the correct model (GMNB)
                    
                    if not model_trained and not self.load_model:
                        self.NN.train_nn(self.neuralNetwork_data, self.train_epochs) # Training the Neural Network
                        if self.save_model:
                            self.NN.save_nn(self.save_model_path) # Saving the Neural Network
                            
                            
                        model_trained = True
                        save_train_data = False # Saving the train data only with the correct model (GMNB)
                    
                    population_fitness = self.NN.evaluate_population(population_list) # Evaluating the fitness of each chromosome          
                    population_list = self.operators.tournament_selection(population_list, population_fitness, k = self.tournament_winner_rate) # Selection
                    population_list = self.operators.pmx_crossover(population_list, self.crossover_rate) # Applying the crossover
                    population_list = self.operators.swap_mutation(population_list, self.mutation_rate) # Applying the mutation
                    
                    progress = "\033[1;34m"+"[Genetic Algorithm Progress]: " + "\033[0m" + "{:.2f}%".format((generation+1)/self.num_generations * 100)
                    time_estimated = "\033[0m" + "| Estimated time: {:.2f} seconds".format((time.time() - generation_start_time) * (self.num_generations - generation))

                    self.get_history(population_fitness, population_list, save_train_data, progress, time_estimated)
                
            except KeyboardInterrupt:
                self.utils.debug(f"Stopped at generation {generation}", type="info")
                processes = multiprocessing.active_children()  # Corrected here
                for process in processes:
                    process.terminate()

                break   

        self.end_time = time.time() # End the timer to check the time of the algorithm
        self.show_results("NNwGMNBwPC", dataset_fitness, self.best_chromosome, self.end_time, self.start_time, population_fitness, 
                          self.best_fitness_history, self.fitness_history)

    # ==============================================================================
    # Uselful functions
    #
    # This functions are used to show the results of the algorithm
    # Or to get the history of the best fitness and the average fitness
    # ============================================================================== 
    
    def show_results(self, type_of_algorithm:str, dataset_fitness:tuple, best_chromosome:tuple, end_time:float, start_time:float, population_fitness:list, best_fitness_history:list, fitness_history:list) -> None:
        
        if type_of_algorithm == "NNwGMNBwPC":
    
                fitness = self.cv.cross_validation([best_chromosome[0]])
                best_chromosome = (best_chromosome[0], fitness[0])
                
                self.utils.debug(f"Chromossome hF found by the Neural Network: {best_chromosome[1]:.5f} | with {sum(best_chromosome[0])} Attributes", type="info")
                self.utils.debug(f"Dataset hF: {dataset_fitness[0]:.5f} | with {self.num_attributes} Attributes", type="info")
 

        
        porcentage_better = ((dataset_fitness[0] - best_chromosome[1]) / dataset_fitness[0] * 100) * - 1
        self.utils.debug(f"The algorithm found a solution {porcentage_better:.2f}% better than the dataset fitness, using {type_of_algorithm}", type="success")

        self.utils.plot_fitness_history(self.fitness_history, title = f'Fitness History {type_of_algorithm}')
        self.utils.plot_fitness_history(self.best_fitness_history, title = f'{type_of_algorithm} Best-Fitness History') # Plotting the best fitness history


    def get_history(self, population_fitness, population_list, save_train_data = False, progress = 0, time_estimated = 0): # Function to get the history of the best fitness and the average fitness
        if save_train_data:
            with open(self.neuralNetwork_data, "a+") as file:
                for i in range(len(population_list)):
                    file.write((str(population_list[i]) + "," + str(population_fitness[i])) + "\n")
            
            print("\33[2K\r " + progress + " " + time_estimated, end = "\r")
        
        if max(population_fitness) > self.best_chromosome[1]:
            index = population_fitness.index(max(population_fitness))
            self.best_chromosome = (population_list[index], population_fitness[index])      
            self.best_fitness_history.append(population_fitness[index])
        else:
            self.best_fitness_history.append(self.best_chromosome[1])     

        self.fitness_history.append(sum(population_fitness) / len(population_fitness))
        
        if not save_train_data and progress != 0 and time_estimated != 0:
            print("\33[2K\r " + progress + " " + time_estimated, end = "\r")


        







    