# ==============================================================================
# Main file to run the genetic algorithm
# 
#
# ==============================================================================
                                                                                
from src.GMNBwGA import GeneticAlgorithm
from src.NNwGA import NNwGeneticAlgorithm
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
    population_size = config["GMNBwGA"]["population_size"]
    num_generations = config["GMNBwGA"]["num_generations"]
    crossover_rate = config["GMNBwGA"]["crossover_rate"]
    mutation_rate = config["GMNBwGA"]["mutation_rate"]
    tournament_winner_rate = config["GMNBwGA"]["tournament_winner_rate"]
    # ==============================================================================
    
    # ==============================================================================
    # Neural Network with Genetic Algorithm variables
    population_size_NN = config["NNwGA"]["population_size"]
    num_generations_NN = config["NNwGA"]["num_generations"]
    crossover_rate_NN = config["NNwGA"]["crossover_rate"]
    mutation_rate_NN = config["NNwGA"]["mutation_rate"]
    tournament_winner_rate_NN = config["NNwGA"]["tournament_winner_rate"]
    GMNB_generations = config["NNwGA"]["GMNB_generations"]
    train_epochs = config["NNwGA"]["train_epochs"]
    save_model = config["NNwGA"]["save_model"]
    save_path = config["NNwGA"]["save_path"]
    load_model = config["NNwGA"]["load_model"]
    load_path = config["NNwGA"]["load_path"]
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
    
    if config["GMNBwGA"]["activate"]:
        Algorithm = GeneticAlgorithm(output_path, population_size, num_generations, crossover_rate, 
                                           mutation_rate, tournament_winner_rate)
        Algorithm.run()
        
    elif config["NNwGA"]["activate"]:
        Algorithm = NNwGeneticAlgorithm(output_path, population_size_NN, num_generations_NN, crossover_rate_NN, 
                                           mutation_rate_NN, tournament_winner_rate_NN, save_model, 
                                           save_path, load_model, load_path, GMNB_generations, train_epochs)
        Algorithm.run()
                                
