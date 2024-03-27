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

from src.utils import Utils
from src.cpp_converter import call_nbayes
from src.dataset import Dataset

import arff
import os
import multiprocessing

class CrossValidation:

    def __init__(self, filepath) -> None:
        
        # Creating the objects.
        self.filepath = filepath
        self.utils = Utils()
        self.num_folds = 5
        
        self.chromossome_train_path = (f"./generated-files/chromossome_train.arff")
        self.chromossome_test_path = (f"./generated-files/chromossome_test.arff")

    def convert_chromossome_to_file(self, chromosome: list, type_chromossome:str, 
                                    cross_validation_folds = None, thread_index = 0) -> None:
        """
        - Convert a chromosome list with binary encoding (e.g., [0, 1, 0, 1]) to a .arff file.
        - Attributes will be get from the first fold, and the objects will be get from the all folds.
        """

        folds = []
        file_paths = []
        

        if type_chromossome == 'test':       
            file_paths.append(self.filepath.split(".")[0] + "_test_fold_" + str(cross_validation_folds) + ".arff")
            
        elif type_chromossome == 'train':
            for i in cross_validation_folds:
                    file_paths.append(self.filepath.split(".")[0] + "_train_fold_" + str(i) + ".arff")
                    
        for file_path in file_paths:
            folds.append(Dataset(file_path))
            
        # ==============================================================================
        # Getting the attributes of the folds and the attribute class
        # ==============================================================================
            
        attributes = folds[0].dataset_dict['attributes'] # attributes of the first fold with the class
        selected_attributes = []
        
        for index, attribute in enumerate(attributes): 
            if attributes[index] == attributes[-1]: # Stop when the class is reached
                selected_attributes.append(attribute)
                break
            
            elif chromosome[index] == 1:
                selected_attributes.append(attribute)
        
        attributes = selected_attributes            

        # ==============================================================================
        # Getting the objects of the folds
        # ==============================================================================

        objects = [] # set of objects of the folds
        selected_objects = [] # set of objects selected by the chromosome
        descriptions = []
    
        
        for i in range(len(folds)):  # for each fold
            objects += folds[i].dataset_dict['data']
            descriptions.append(f"Fold {cross_validation_folds} of the dataset")
        
        
        for line in range(len(objects)):
            selected_objects_line = []
            for column in range(len(objects[line])):
                if objects[line][column] == objects[line][-1]: # Stop when the class is reached
                    selected_objects_line.append(objects[line][column])
                    break
                
                if chromosome[column] == 1:
                    selected_objects_line.append(objects[line][column])
            
            selected_objects.append(selected_objects_line)
        objects = selected_objects
        
        #print(f"Attributes per line: {len(selected_objects[0])}")
        #print(f"Attributes selected by this algorithm: {len(attributes)}")   
        #print(f"Chromossome selected attributes number: {chromosome.count(1)}")
        #print("-" * 50)
        
                
        # ==============================================================================
        # Saving the dataset in a new file
        # ==============================================================================

        new_dataset = {}
        new_dataset['attributes'] = attributes
        new_dataset['data'] = objects
        new_dataset['description'] = str(descriptions.copy())
        new_dataset['relation'] = folds[0].dataset_dict['relation']
        
        if type_chromossome == 'test':
            save_path = (f"./generated-files/{thread_index}/chromossome_test.arff")

        elif type_chromossome == 'train':
            save_path = (f"./generated-files/{thread_index}/chromossome_train.arff")
            
        elif type_chromossome == "best_chromossome_test":
            save_path = (f"./generated-files/{thread_index}/best_chromossome_test.arff")

        elif type_chromossome == "best_chromossome_train":
            save_path = (f"./generated-files/{thread_index}/best_chromossome_train.arff")

        arff.dump(new_dataset, open(save_path, 'w+'))
        
        return save_path

    def cross_validation(self, population: list[list[int]]) -> list[float]:
        # Define a function to handle fitness calculation for each chromosome
        def calculate_fitness(chromosome, thread_index, thread_results):
            cross_validation_values = []
            for test_index in range(self.num_folds):
                train_index = [i for i in range(self.num_folds) if i != test_index]

                test_path =  self.convert_chromossome_to_file(chromosome, 'test', cross_validation_folds=test_index, thread_index=thread_index)
                train_path = self.convert_chromossome_to_file(chromosome, 'train', cross_validation_folds=train_index, thread_index=thread_index)

                cross_validation_values.append(call_nbayes(train_path, test_path))

            # Append the average of cross_validation_values to thread_results
            thread_results.append(sum(cross_validation_values) / len(cross_validation_values))

        with multiprocessing.Manager() as manager:
            thread_results = manager.list()  # Shared list

            processes = []
            for chromossome in population:
                thread_index = population.index(chromossome)
                os.makedirs(f"./generated-files/{thread_index}", exist_ok=True)
                
                p = multiprocessing.Process(target=calculate_fitness, args=(chromossome, thread_index, thread_results))
                processes.append(p)
                p.start()

            for process in processes:
                process.join()

            # Convert the shared list to a regular list
            chromossomes_fitness = list(thread_results)
            
            return chromossomes_fitness