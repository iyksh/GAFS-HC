# ==============================================================================
# Main file to run the genetic algorithm
# 
#
# Author: Guilherme Santos
# Last edited: 2023-01-23
# ==============================================================================

from genetic_algorithm import GeneticAlgorithm
from dataset import DatasetManipulator

# ==============================================================================
# Paths and variables
# ==============================================================================                                                        

test_path = "/home/yksh/Desktop/bases_particionadas/CellCycle/10-folds/fold5/CellCycle_test.arff"
train_path = "/home/yksh/Desktop/bases_particionadas/CellCycle/10-folds/fold5/CellCycle_train.arff"
output_path_test = test_path.split(".")[0] + "_output.arff"
output_path_train = train_path.split(".")[0] + "_output.arff"

# Preprocessing the dataset variables
discretize = True # Set the discretize variable to True if you want to discretize the dataset
set_minimum_classes = True # Set the set_minimum_classes variable to True if you want to set the minimum number of classes to 10

# Genetic Algorithm variables
population_size = 10 
num_generations = 20
cross_validation = True # Recommended to be always True

# Report variables
i = 1 # Number of the report

# ==============================================================================
# Preprocessing the dataset
# ==============================================================================

preprocessing = DatasetManipulator()

if discretize:    
    preprocessing.discretize_data(test_path, output_path_test)
    preprocessing.discretize_data(train_path, output_path_train)
    if set_minimum_classes:
        preprocessing.minimum_classes(output_path_test, output_path_test, minimum= 10)
        preprocessing.minimum_classes(output_path_train, output_path_train, minimum= 10)

else:
    output_path_test = test_path
    output_path_train = train_path

# ==============================================================================
# Algorithm and report
# ==============================================================================

Algorithm = GeneticAlgorithm(output_path_test, output_path_train, cross_validation= cross_validation) # Genetic Algorithm object

# Report
with open("src/report.txt", "a") as file:
    file.write(f"-------------------------------------------------\n")
    file.write(f"Report {i}\n")
    file.write(f"Test file: {output_path_test}\n")
    file.write(f"Train file: {output_path_train}\n")
    file.write(f"Population size: {population_size}\n")
    file.write(f"Number of generations: {num_generations}\n")
    file.write(f"Cross validation: {cross_validation}\n")
    file.write(f"Best chromossome: {Algorithm.best_chromosome[0]}\n")
    file.write(f"Best fitness: {Algorithm.best_chromosome[1]}\n")
    file.write(f"Avarage fitness history: {Algorithm.fitness_history}\n")
    file.write(f"Best fitness history: {Algorithm.best_fitness_history}\n")
    file.write(f"-------------------------------------------------\n")
file.write(f"\n")
file.close()


