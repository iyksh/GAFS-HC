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

from src.utils import Utils
from src.cpp_converter import call_nbayes
from src.dataset import Dataset

class CrossValidation:

    def __init__(self, filepath) -> None:
        
        # Creating the objects.
        self.filepath = filepath
        self.utils = Utils()
        self.num_folds = 5
        
        self.chromossome_train_path = (f"./generated-files/chromossome_train.arff")
        self.chromossome_test_path = (f"./generated-files/chromossome_test.arff")
        

    def convert_chromossome_to_file(self, chromosome: list, filepath:str, type:str, num_folds = 5, cross_validation_folds = None) -> None:
        """
        - Convert a chromosome list with binary encoding (e.g., [0, 1, 0, 1]) to a .arff file.
        - Attributes will be get from the first fold, and the objects will be get from the all folds.
    
        Parameters:
            - chromosome (list): Binary-encoded chromosome representing attribute selection.
            - filepath (str): The path of the dataset file.
            - type (str): The type of the dataset file. It can be 'test' or 'train'.
            - num_folds (int): The number of folds of the dataset file.
            - cross_validation_folds (list): The list of folds to be used in the cross-validation. If None, all folds will be used.

        Note:
            The resulting .arff file is saved as `chromossome.arff`, by the default self.chromossome_path.
        """

        folds = []

        if cross_validation_folds != None and type == 'test':       
            filepath_fold = filepath.split(".")[0] + "_test_fold_" + str(cross_validation_folds) + ".arff"
            temporary = Dataset(filepath_fold)
            folds.append(temporary)

        elif cross_validation_folds != None and type == 'train':
            for i in range(num_folds): # Read all folds
                if i in cross_validation_folds:
                    filepath_fold = filepath.split(".")[0] + "_train_fold_" + str(i) + ".arff"
                    temporary = Dataset(filepath_fold)
                    folds.append(temporary)

        # ==============================================================================
        # Getting the attributes of the folds and the attribute class
        # ==============================================================================
            
        attributes = []
        temporary_chromossome = folds[0] 
        attributes_class = temporary_chromossome.dataset_attributes[-1] 

        # all the folds have the same attributes_class and the same number of attributes
        # The chromosome size is equal to the number of attributes
        for i in range(len(temporary_chromossome.dataset_dict['attributes'][:-1])): 
            if chromosome[i] == 1:
                attributes.append(temporary_chromossome.dataset_dict['attributes'][i])
        attributes.append(attributes_class) #incluing @ATTRIBUTE class

        # ==============================================================================
        # Getting the objects of the folds
        # ==============================================================================

        objects = [] # set of objects of the folds
        descriptions = []

        # for each fold
        for i in range(len(folds)): 
            descriptions.append(folds[i].dataset_dict['description'])
            # for each line of the objects
            for j in range(len(folds[i].dataset_objects)): 
                line = [] # subset of objects of the folds

                # for each number in the line
                for k in range(len(folds[i].dataset_objects[j]) - 1): 
                    if chromosome[k] == 1:
                        line.append(folds[i].dataset_objects[j][k])
                line.append(folds[i].dataset_objects[j][-1]) # add the class


                # add the line in the subset of objects of the folds
                objects.append(line) 

        # ==============================================================================
        # Saving the dataset in a new file
        # ==============================================================================

        new_dataset = Dataset(filepath)
        new_dataset.dataset_dict['attributes'] = attributes
        new_dataset.dataset_dict['data'] = objects
        description = str(descriptions.copy())


        if type == 'test':
            save_path = self.chromossome_test_path

        elif type == 'train':
            save_path = self.chromossome_train_path
            
        elif type == "best_chromossome_test":
            description = "Best Chromossome of the test dataset"
            save_path = "./generated-files/best_chromossome_test.arff"

        elif type == "best_chromossome_train":
            description = "Best Chromossome of the train dataset"
            save_path = "./generated-files/best_chromossome_train.arff"

        new_dataset.dataset_dict['description'] = description
        new_dataset.save_dataset(save_path)

    # a ser alterado, deixar os mesmos parâmetros.
    def cross_validation(self, population: list[list[int]]) -> list[float]:
        chromossomes_fitness = []
        
        for chromosome in population:
            cross_validation_values = []
            
            for test_index in range(self.num_folds):
                train_index = [i for i in range(self.num_folds) if i != test_index]
                
                self.convert_chromossome_to_file(chromosome, self.filepath, 'test', cross_validation_folds=test_index)
                self.convert_chromossome_to_file(chromosome, self.filepath, 'train', cross_validation_folds=train_index)
                
                cross_validation_values.append(call_nbayes(self.chromossome_train_path, self.chromossome_test_path))
            
            chromossomes_fitness.append(sum(cross_validation_values) / self.num_folds)
        
        return chromossomes_fitness
