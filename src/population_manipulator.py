# ======================================================================================================
# Main file to manipulate the population and the fitness function
# 
#
# Author: Guilherme Santos
# Last edited: 2023-01-25
#
# [1]. The class Population is used to manipulate attributes
#      - Not working with mandatory leaf prediction.
#      - The train and test dataset needs to have the same number of attributes
#
# [2]. The class ClassPopulation is used to manipulate classes
#      - Not implemented, maybe can be used in the future with mandatory leaf prediction.
# 
# ======================================================================================================

import random
import time

from dataset import Dataset
from cross_validation import *
from utils import Utils

class Population:

    def __init__(self, test_dataset_path, train_dataset_path) -> None:
        
        # Creating the objects.
        self.utils = Utils()
        self.train_data = Dataset(train_dataset_path) 
        self.test_data = Dataset(test_dataset_path)
        
        # Saving the paths.
        self.train_filepath = train_dataset_path
        self.test_filepath = test_dataset_path

        # The train and test dataset.
        self.chromossome_train_path = (f"./chromossome_train.arff")
        self.chromossome_test_path = (f"./chromossome_test.arff")
        


    def create_population(self, population_size: int) -> list[list[int]]:
        """
        Create the initial population with random genes (0 or 1).
        
        - 0 means that the attribute will not be selected, and 1 means that the attribute will be selected.

        """

        len_attributes = len(self.train_data.dataset_attributes[:-1]) # Exclude the #ATTRIBUTE class
        population = []

        for _ in range(population_size):
            chromosome = [random.randint(0, 1) for _ in range(len_attributes)]

            # Ensure at least one attributes is selected
            if chromosome.count(1) == 0:
                chromosome[random.randint(0, len_attributes - 1)] = 1

            population.append(chromosome)

        return population

        
    def convert_chromossome_to_file(self, chromosome: list, filepath, type) -> None:
        """
        Convert a chromosome list with binary encoding (e.g., [0, 1, 0, 1]) to a .arff file.

        Attributes with a binary value of 0 will be excluded from the resulting dataset.

        Parameters:
            chromosome (list): Binary-encoded chromosome representing attribute selection.

        Note:
            The resulting .arff file is saved as `chromossome.arff`, by the default self.chromossome_path.
        """

        temporary_chromossome = Dataset(filepath)

        attributes = []
        attributes_class = temporary_chromossome.dataset_attributes[-1]
              
        for i in range(len(temporary_chromossome.dataset_dict['attributes'][:-1])): # The chromosome size is equal to the number of attributes
            if chromosome[i] == 1:
                attributes.append(temporary_chromossome.dataset_dict['attributes'][i])
        

        for i in range(len(temporary_chromossome.dataset_objects)):
            for j in range(len(temporary_chromossome.dataset_objects[i]) - 1):
                if chromosome[j] == 0:
                    temporary_chromossome.dataset_objects[i][j] = ''
            

        for i in range(len(temporary_chromossome.dataset_objects)): # Remove empty attributes
            temporary_chromossome.dataset_objects[i] = [attribute for attribute in temporary_chromossome.dataset_objects[i] if attribute != '']


    
        attributes.append(attributes_class) #incluing @ATTRIBUTE class
        temporary_chromossome.dataset_dict['data'] = temporary_chromossome.dataset_objects
        temporary_chromossome.dataset_dict['attributes'] = attributes

        if type == 'test':
            temporary_chromossome.dataset_dict['description'] = "Test Chromossome"
            temporary_chromossome.save_dataset(self.chromossome_test_path)
        elif type == 'train':
            temporary_chromossome.dataset_dict['description'] = "Train Chromossome"
            temporary_chromossome.save_dataset(self.chromossome_train_path)
        elif type == "best_chromossome":
            temporary_chromossome.dataset_dict['description'] = "Best Chromossome"
            temporary_chromossome.save_dataset('./best_chromossome.arff')
        
        else:
            self.utils.debug("Invalid type", "error")

    def evaluate_fitness(self, population, cross_validation_check) -> list:
        chromossomes_fitness = []

        for chromosome in population:
            self.convert_chromossome_to_file(chromosome, self.test_filepath, 'test')
            self.convert_chromossome_to_file(chromosome, self.train_filepath, 'train')

            if cross_validation_check:
                self.utils.debug("Crossvalidation Not implemented yet", "error")
                pass

            else:
                value = call_nbayes(self.chromossome_train_path, self.chromossome_test_path)

            chromossomes_fitness.append(value)
        return chromossomes_fitness



# ==============================================================================
# Class to manipulate classes (outdated)
# ==============================================================================

class ClassPopulation:

    def __init__(self, test_dataset_path) -> None:
        self.data = Dataset(test_dataset_path)
        self.filepath = test_dataset_path
        self.chromossome_path = "./chromossome.arff"
        self.utils = Utils()
        self.cross_validation_warning = False


    def create_population(self, population_size: int) -> list:
        """
        Create the initial population with random genes (0 or 1).
        
        - 0 means that the attribute will not be selected, and 1 means that the gene of the attribute_class will be selected.

        """


        len_attributes = len(self.data.dataset_attributes[-1][1])
        population = []

        for _ in range(population_size):
            chromosome = [random.randint(0, 1) for _ in range(len_attributes)]

            # Ensure at least one attributes is selected
            if chromosome.count(1) == 0:
                chromosome[random.randint(0, len_attributes - 1)] = 1

            population.append(chromosome)

        return population

        
    def convert_chromossome_to_file(self, chromosome: list, path = None, description = None) -> None:
        """
        Convert a chromosome list with binary encoding (e.g., [0, 1, 0, 1]) to a .arff file.

        Attributes with a binary value of 0 will be excluded from the resulting dataset.

        Parameters:
            chromosome (list): Binary-encoded chromosome representing attribute selection.

        Note:
            The resulting .arff file is saved as `chromossome.arff`, by the default self.chromossome_path, if the path is not specified.
        """

        if path == None:
            path = self.chromossome_path

        temporary_chromossome = Dataset(self.filepath)
        attributes_class = self.data.dataset_attributes[-1][1]

        attributes = []
        objects = []

        for i in range(len(attributes_class)): # The chromosome size is equal to the number of attributes
            if chromosome[i] == 1:
                attributes.append(attributes_class[i])
        

        for i in range(len(self.data.dataset_objects)):
            if self.data.dataset_objects[i][-1] in attributes:
                objects.append(self.data.dataset_objects[i])
            
        if description != None:
            temporary_chromossome.dataset_dict['description'] = description
    
        
        temporary_chromossome.dataset_dict['data'] = objects
        temporary_chromossome.dataset_dict['attributes'][-1] = ('class', attributes)
        temporary_chromossome.save_dataset(path)

    def evaluate_fitness(self, population, training_path, cross_validation_check = False) -> list:
        chromossomes_fitness = []
        start_time = time.time()
        for chromosome in population:
            self.convert_chromossome_to_file(chromosome)
            
            if cross_validation_check:
                if not self.cross_validation_warning:
                    self.utils.debug("Cross Validation is activated", "warning")
                    self.cross_validation_warning = True
                value = cross_validation(self.chromossome_path, training_path)

            else:
                value = call_nbayes(training_path, self.chromossome_path)

            chromossomes_fitness.append(value)

        self.utils.debug(f"Time to evaluate fitness: {(time.time() - start_time):.3f} seconds", "info")


        return chromossomes_fitness
    


