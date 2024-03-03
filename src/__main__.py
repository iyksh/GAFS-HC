# ==============================================================================
# Main file to run the genetic algorithm
# 
#
# Author: Guilherme Santos
# Last edited: 2024-02-11 
# ==============================================================================
                                                                                
from src.genetic_algorithm import GeneticAlgorithm
from src.dataset import DatasetManipulator, Dataset

# ==============================================================================
# Paths and variables, read the config.json file and change the variables there
# ==============================================================================

def __main__(config: dict) -> None:
    """ - Warning: This function will discretize the dataset and delete the attributes with less than 10 classes."""
                                                  
    #Paths variables
    dataset_path = config["dataset_path"]
    
    # Create the test and train files
    test_path = dataset_path.split("_")[0] + "_test.arff"
    train_path = dataset_path.split("_")[0] + "_train.arff"

    # Genetic Algorithm variables
    population_size = config["GeneticAlgorithm"]["population_size"]
    num_generations = config["GeneticAlgorithm"]["num_generations"]
    crossover_rate = config["GeneticAlgorithm"]["crossover_rate"]
    mutation_rate = config["GeneticAlgorithm"]["mutation_rate"]
    tournament_winner_rate = config["GeneticAlgorithm"]["tournament_winner_rate"]
    enable_parallelism = config["GeneticAlgorithm"]["enable_parallelism"]
    max_parallelism_subprocess = config["GeneticAlgorithm"]["max_parallelism_subprocess"]
    
    HCFS = config["HCFS"]["activate"]
    GMNB_generations = config["HCFS"]["GMNB_generations"] if HCFS else 0
    
    NeuralNetwork = config["NeuralNetwork"]["activate"]
    train_epochs = config["NeuralNetwork"]["train_epochs"]
    save_model = config["NeuralNetwork"]["save_model"]
    save_path = config["NeuralNetwork"]["save_path"]
    load_model = config["NeuralNetwork"]["load_model"]
    load_path = config["NeuralNetwork"]["load_path"]
    GMNB_generations = config["NeuralNetwork"]["GMNB_generations"] if NeuralNetwork else GMNB_generations
    

    # ==============================================================================
    # Preprocessing the dataset
    # ==============================================================================
    
    preprocessing = DatasetManipulator()

    preprocessing.split_dataset(dataset_path, test_path, train_path) # Split the dataset into test and train datasets

    preprocessing.discretize_data(test_path, test_path) # Discretize the dataset 
    preprocessing.discretize_data(train_path, train_path) # Discretize the dataset

    preprocessing.minimum_classes(test_path, test_path) # Delete the attributes with less than 10 classes
    preprocessing.minimum_classes(train_path, train_path) # Delete the attributes with less than 10 classes

    # ==============================================================================
    # Algorithm and report
    # ==============================================================================

    Algorithm = GeneticAlgorithm(test_path, train_path, population_size, num_generations, 
                                crossover_rate, mutation_rate, tournament_winner_rate,
                                enable_parallelism, max_parallelism_subprocess, HCFS,
                                NeuralNetwork, train_epochs, save_model, save_path, load_model, load_path,
                                GMNB_generations)
                                
                                
                                

    
    Algorithm.NNwGMNBwPC() # Run the genetic algorithm