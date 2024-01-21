#                                                                   #
#                                                                   #
#                                                                   #
#                   In this code has 2 types of classes             #
#               To manipulate .arff files to chromossomes           #
#   One is the @ATTRIBUTE class chromossomes, another one is        #
#   just the @ATTRIBUTE chromossomes. both are in binary enconding  #
#  with same functions names to use it on the genetic_algorithm.py  #
#                                                                   #
#                                                                   #

import random
import time

from dataset import Dataset
from cross_validation import *
from utils import Utils

class ClassPopulation:

    def __init__(self, test_dataset_path) -> None:
        self.data = Dataset(test_dataset_path)
        self.filepath = test_dataset_path
        self.chromossome_path = "./chromossome.arff"
        self.utils = Utils()


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
                self.utils.debug("Cross Validation is activated", "warning")
                value = cross_validation(self.chromossome_path, training_path)

            else:
                value = call_nbayes(training_path, self.chromossome_path)

            chromossomes_fitness.append(value)

        self.utils.debug(f"Time to evaluate fitness: {(time.time() - start_time):.3f} seconds", "info")


        return chromossomes_fitness
    

#                                                                   #
#                                                                   #
#   AttributesPopulation doesnt seems to get different values in    #
#   the chromossomes fitness evaluation                             #
#                                                                   #
#                                                                   #

class Population:

    def __init__(self, test_dataset_path) -> None:
        self.data = Dataset(test_dataset_path)
        self.filepath = test_dataset_path
        self.chromossome_path = (f"./chromossome.arff")
        


    def create_population(self, population_size: int) -> list:
        """
        Create the initial population with random genes (0 or 1).
        
        - 0 means that the attribute will not be selected, and 1 means that the attribute will be selected.

        """

        len_attributes = len(self.data.dataset_attributes[:-1])
        population = []

        for _ in range(population_size):
            chromosome = [random.randint(0, 1) for _ in range(len_attributes)]

            # Ensure at least one attributes is selected
            if chromosome.count(1) == 0:
                chromosome[random.randint(0, len_attributes - 1)] = 1


            population.append(chromosome)

        return population

        
    def convert_chromossome_to_file(self, chromosome: list) -> None:
        """
        Convert a chromosome list with binary encoding (e.g., [0, 1, 0, 1]) to a .arff file.

        Attributes with a binary value of 0 will be excluded from the resulting dataset.

        Parameters:
            chromosome (list): Binary-encoded chromosome representing attribute selection.

        Note:
            The resulting .arff file is saved as `chromossome.arff`, by the default self.chromossome_path.
        """

        attributes = []
        temporary_chromossome = Dataset(self.filepath)
              
        for i in range(len(temporary_chromossome.dataset_dict['attributes'][:-1])): # The chromosome size is equal to the number of attributes
            if chromosome[i] == 1:
                attributes.append(temporary_chromossome.dataset_dict['attributes'][i])
        

        for i in range(len(temporary_chromossome.dataset_objects)):
            for j in range(len(temporary_chromossome.dataset_objects[i]) - 1):
                if chromosome[j] == 0:
                    temporary_chromossome.dataset_objects[i][j] = ''
            

        for i in range(len(temporary_chromossome.dataset_objects)): # Remove empty attributes
            temporary_chromossome.dataset_objects[i] = [attribute for attribute in temporary_chromossome.dataset_objects[i] if attribute != '']


    
        attributes.append(self.data.dataset_attributes[-1]) #incluing @ATTRIBUTE class
        temporary_chromossome.dataset_dict['data'] = temporary_chromossome.dataset_objects
        temporary_chromossome.dataset_dict['attributes'] = attributes
        temporary_chromossome.save_dataset(self.chromossome_path)
        
    def evaluate_fitness(self, population, training_path, cross_validation_check = True) -> list:
        chromossomes_fitness = []

        for chromosome in population:
            self.convert_chromossome_to_file(chromosome)

            if cross_validation_check:
                value = cross_validation(self.chromossome_path, training_path)

            else:
                value = call_nbayes(training_path, self.chromossome_path)

            chromossomes_fitness.append(value)
        return chromossomes_fitness

