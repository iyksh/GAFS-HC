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
    test_path = config["test_path"]
    train_path = config["train_path"]
    if test_path == None:
        test_path = train_path.split(".")[0] + "_test.arff"
        temp_dataset = Dataset(train_path)
        temp_dataset.save_dataset(test_path)       
        print(f"[+] Test path not found, using the train path to create the test file: {test_path}")

    output_path_test = test_path.split(".")[0] + "_preprocessed.arff"
    output_path_train = train_path.split(".")[0] + "_preprocessed.arff"

    # Genetic Algorithm variables
    population_size = config["population_size"]
    num_generations = config["num_generations"]
    crossover_rate = config["crossover_rate"]
    mutation_rate = config["mutation_rate"]
    tournament_winner_rate = config["tournament_winner_rate"]
    timer = config["timer_stop_algorithm"]
    enable_parallelism = config["enable_parallelism"]
    max_parallelism_subprocess = config["max_parallelism_subprocess"]

    # ==============================================================================
    # Preprocessing the dataset
    # ==============================================================================

    preprocessing = DatasetManipulator()

    preprocessing.discretize_data(test_path, output_path_test) # Discretize the dataset 
    preprocessing.discretize_data(train_path, output_path_train) # Discretize the dataset

    preprocessing.minimum_classes(output_path_test, output_path_test) # Delete the attributes with less than 10 classes
    preprocessing.minimum_classes(output_path_train, output_path_train) # Delete the attributes with less than 10 classes

    # ==============================================================================
    # Algorithm and report
    # ==============================================================================

    Algorithm = GeneticAlgorithm(output_path_test, output_path_train, population_size, num_generations, 
                                crossover_rate, mutation_rate, tournament_winner_rate, timer,
                                enable_parallelism, max_parallelism_subprocess) 

                                