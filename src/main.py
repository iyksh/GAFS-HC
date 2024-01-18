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
test_path = "/home/yksh/Desktop/CellCycle_single.arff"
train_path = "/home/yksh/Desktop/CellCycle_train.arff"

# Preprocessing the dataset variables
discretize = True
set_minimum_classes = True # Set the minimum number of 10 classes to be selected
output_path_test = "/home/yksh/Desktop/CellCycle_single_Discretized.arff"
output_path_train = "/home/yksh/Desktop/CellCycle_train_Discretized.arff"
preprocessing = DatasetManipulator()

if discretize:
    preprocessing.discretize_data(test_path, output_path_test)
    preprocessing.discretize_data(train_path, output_path_train)


if set_minimum_classes:
    preprocessing.minimum_classes(output_path_test, output_path_test, minimum= 10)
    preprocessing.minimum_classes(output_path_train, output_path_train, minimum= 10)


# Genetic Algorithm variables
population_size = 50
num_generations = 20
cross_validation = False
GeneticAlgorithm(population_size, num_generations, output_path_train, output_path_test, cross_validation) # Genetic Algorithm object


