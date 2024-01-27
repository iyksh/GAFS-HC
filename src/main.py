# ==============================================================================
# Main file to run the genetic algorithm
# 
#
# Author: Guilherme Santos
# Last edited: 2023-01-23 
# ==============================================================================
                                                                                
import json

from genetic_algorithm import GeneticAlgorithm
from dataset import DatasetManipulator

# ==============================================================================
# Paths and variables, read the config.json file and change the variables there
# ==============================================================================

with open("./src/config.json", "r") as FILE:
    config = json.load(FILE)                                                      

#Paths variables
test_path = config["test_path"]
train_path = config["train_path"]
output_path_test = test_path.split(".")[0] + "_preprocessed.arff"
output_path_train = train_path.split(".")[0] + "_preprocessed.arff"


# Genetic Algorithm variables
population_size = config["population_size"]
num_generations = config["num_generations"]
crossover_rate = config["crossover_rate"]
mutation_rate = config["mutation_rate"]
tournament_winner_rate = config["tournament_winner_rate"]
timer = config["timer_stop_algorithm"]

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

# Genetic Algorithm object
Algorithm = GeneticAlgorithm(output_path_test, output_path_train, population_size, num_generations, 
                             crossover_rate, mutation_rate, tournament_winner_rate, timer) 

                             
