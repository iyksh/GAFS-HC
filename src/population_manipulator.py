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
import warnings
import pandas as pd


from dataset import Dataset
from utils import Utils
from call_nbayes import call_nbayes
from sklearn.model_selection import StratifiedKFold


class Population:

    def __init__(self, test_dataset_path:str, train_dataset_path:str) -> None:
        
        # Creating the objects.
        self.utils = Utils()
        self.train_data = Dataset(train_dataset_path) 
        self.test_data = Dataset(test_dataset_path)
        
        # Saving the paths.
        self.train_filepath = train_dataset_path
        self.test_filepath = test_dataset_path

        # The train and test dataset.
        self.chromossome_train_path = (f"./generated-files/chromossome_train.arff") # Problem if use threads    
        self.chromossome_test_path = (f"./generated-files/chromossome_test.arff") # Problem if use threads

    def five_folds(self, path_dataset: str) -> None:
        """Divide the dataset into 5 parts, and each part is saved in a .arff file.
        
        The dataset is divided using StratifiedKFold,
        to maintain class proportions during cross-validation.
        
        """
        # Load datasets
        dataset = Dataset(path_dataset)
        data_list_test = dataset.dataset_objects
        df_test = pd.DataFrame(data_list_test)
        X_test = df_test.iloc[:, :-1]   # Separating the attributes and 
        y_test = df_test.iloc[:, -1]    # the classes for test dataset

        if len(dataset.dataset_objects) < 20:
            raise ValueError("The dataset is too small to be divided into 5 folds. Minimum of 20 objects.")

        # Using StratifiedKFold to maintain class proportions during cross-validation for test dataset
        skf_test = StratifiedKFold(n_splits=5, random_state=42, shuffle=True)
        warnings.filterwarnings("ignore", category=UserWarning)
        for i, (train_index_test, test_index_test) in enumerate(skf_test.split(X_test, y_test)):

            X_train_test, X_test_test = X_test.iloc[train_index_test], X_test.iloc[test_index_test]
            y_train_test, y_test_test = y_test.iloc[train_index_test], y_test.iloc[test_index_test]

            test_data_test = pd.concat([X_test_test, y_test_test], axis=1).astype(str).values.tolist()
            test_df_test = pd.DataFrame(test_data_test, columns=df_test.columns)
            
            # Saving the DataFrames to .arff files
            path = path_dataset.split(".")[0] + "_fold(" + str(i + 0) + ").arff"
            test_df_test.to_csv(path, index=False, header=False)

            fold_data = []
            with open(path, 'r') as file:
                for line in file:
                    fold_data.append(line.strip().split(','))

            description = dataset.dataset_dict['description']
            dataset.dataset_dict['description'] = f'{description}_fold({i + 0})'
            dataset.dataset_dict['data'] = fold_data
            dataset.save_dataset(path)
            dataset.dataset_dict['description'] = description
        warnings.catch_warnings()
        


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

        
    def convert_chromossome_to_file(self, chromosome: list, filepath:str, type:str, num_folds = 5) -> None:
        """
        - Convert a chromosome list with binary encoding (e.g., [0, 1, 0, 1]) to a .arff file.
        - Attributes will be get from the first fold, and the objects will be get from the all folds.
    
        Parameters:
            chromosome (list): Binary-encoded chromosome representing attribute selection.

        Note:
            The resulting .arff file is saved as `chromossome.arff`, by the default self.chromossome_path.
        """

        folds = []

        for i in range(num_folds): # Read all folds
            filepath_fold = filepath.split(".")[0] + "_fold(" + str(i) + ").arff"
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
        
        # for each fold
        for i in range(len(folds)): 
            
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

        if type == 'test':
            description = "Test Chromossome - 5 folds"
            save_path = self.chromossome_test_path

        elif type == 'train':
            description = "Train Chromossome - 5 folds"
            save_path = self.chromossome_train_path
            
        elif type == "best_chromossome_test":
            description = "Best Chromossome of the test dataset"
            save_path = "./generated-files/best_chromossome_test.arff"

        elif type == "best_chromossome_train":
            description = "Best Chromossome of the train dataset"
            save_path = "./generated-files/best_chromossome_train.arff"

        new_dataset.dataset_dict['description'] = description
        new_dataset.save_dataset(save_path)


    def cross_validation(self, population:list[int]) -> list[float]:
        chromossomes_fitness = []

        for chromosome in population:
            self.convert_chromossome_to_file(chromosome, self.test_filepath, 'test')
            self.convert_chromossome_to_file(chromosome, self.train_filepath, 'train')

            value = call_nbayes(self.chromossome_train_path, self.chromossome_test_path)

            chromossomes_fitness.append(value)
        return chromossomes_fitness

