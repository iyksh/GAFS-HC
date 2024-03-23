# ==============================================================================
# Main file to run the genetic algorithm
# 
#
# ==============================================================================
                                                                                
from src.genetic_algorithm import GeneticAlgorithm
from src.utils import Utils
from src.preprocessing import Preprocessing
from src.cpp_converter import call_nbayes

# ==============================================================================
# Paths and variables, read the config.json file and change the variables there
# ==============================================================================

def __main__(config: dict) -> None:
    """ - Warning: This function will discretize the dataset and delete the attributes with less than 10 classes."""
                                                  
    dataset_path = config["dataset_path"]
    
    # ==============================================================================
    # Global Model Naive Bayes with Genetic Algorithm variables 
    activate_GMNBwGA = config["GMNBwGA"]["activate"]
    population_size = config["GMNBwGA"]["population_size"]
    num_generations = config["GMNBwGA"]["num_generations"]
    crossover_rate = config["GMNBwGA"]["crossover_rate"]
    mutation_rate = config["GMNBwGA"]["mutation_rate"]
    tournament_winner_rate = config["GMNBwGA"]["tournament_winner_rate"]
    # ==============================================================================


    # ==============================================================================
    # Preprocessing the dataset
    #
    # 1. Delete the attributes with less than 10 classes
    # 2. Discretize the dataset
    # 3. Split the dataset into test and train files with 5 folds each

    preprocessing, utils = Preprocessing(), Utils()
    utils.clear_log() 
    utils.clear_screen() 

    output_path = dataset_path.split("_")[0] + ".arff" 
    train_path = dataset_path.split("_")[0] + "_train"
    test_path = dataset_path.split("_")[0] + "_test"
    
    preprocessing.minimum_classes(dataset_path, output_path) # Delete the attributes with less than 10 classes
    preprocessing.discretize_data(output_path, output_path) # Discretize the dataset 
    preprocessing.split_dataset(output_path, test_path, train_path) # Split into test and train datasets
    
    #
    #
    #
    #
    # ==============================================================================
    
    if activate_GMNBwGA:
        Algorithm = GeneticAlgorithm(output_path, population_size, num_generations, crossover_rate, 
                                           mutation_rate, tournament_winner_rate)
        Algorithm.run()
                                
