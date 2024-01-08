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
test_path = "exemples-datasets/test_test.arff"
train_path = "exemples-datasets/test_train.arff"

# Preprocessing the dataset variables
discretize = False
set_minimum_classes = False
output_path_test = ""
output_path_train = ""
preprocessing = DatasetManipulator()

if discretize:
    preprocessing.discretize_data(test_path, output_path_test)
    preprocessing.discretize_data(train_path, output_path_train)


if set_minimum_classes:
    preprocessing.minimum_classes(output_path_test, output_path_test, minimum= 10)
    preprocessing.minimum_classes(output_path_train, output_path_train, minimum= 10)


# Genetic Algorithm variables
population_size = 40
num_generations = 100
cross_validation = True
GeneticAlgorithm(population_size, num_generations, train_path, test_path, cross_validation) # Genetic Algorithm object


