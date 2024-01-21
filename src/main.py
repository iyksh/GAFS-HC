from genetic_algorithm import GeneticAlgorithm
from dataset import DatasetManipulator

#                                                                   
#                                                                   
#                                                                   
#                                                                   
#                  Main file to manipulate                 
#   The dataset and the genetic algorithm, and to find the best                                                                    
#                  attributes to be selected.                                                                     
#                                                                   
#                                                                   
#                                                                   

#You can change the paths here
test_path = "/home/yksh/Desktop/CellCycle_train.arff"
train_path = "/home/yksh/Desktop/CellCycle_test.arff"

# Preprocessing the dataset variables
discretize = False
set_minimum_classes = False # Set the minimum number of 10 classes to be selected
preprocessing = DatasetManipulator()

output_path_test = test_path.split(".")[0] + "_discretized.arff"
output_path_train = train_path.split(".")[0] + "_discretized.arff"

if discretize:
    output_path_test = test_path.split(".")[0] + "_discretized.arff"
    output_path_train = train_path.split(".")[0] + "_discretized.arff"
    
    preprocessing.discretize_data(test_path, output_path_test)
    preprocessing.discretize_data(train_path, output_path_train)


if set_minimum_classes:
    output_path_test = test_path.split(".")[0] + "_discretized.arff"
    output_path_train = train_path.split(".")[0] + "_discretized.arff"

    preprocessing.minimum_classes(output_path_test, output_path_test, minimum= 10)
    preprocessing.minimum_classes(output_path_train, output_path_train, minimum= 10)


# Genetic Algorithm variables
population_size = 10
num_generations = 3
cross_validation = False
GeneticAlgorithm(population_size, num_generations, output_path_train, output_path_test) # Genetic Algorithm object


