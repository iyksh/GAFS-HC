# ==============================================================================
# Main file to manipulate the dataset 
# 
#
# Author: Guilherme Santos
# Last edited: 2023-01-23
# ==============================================================================

import arff
import random

import numpy as np

from sklearn.preprocessing import KBinsDiscretizer
from src.utils import Utils

# ==============================================================================
# # This class is used just to extract the dataset information
# ==============================================================================

class Dataset: 
    """
    
    This class is used to extract the dataset information, such as the dataset name, 
    the dataset attributes and the dataset data itself.

    Imported arff library of Connectionist Artificial Intelligence Laboratory (LIAC)    
    `Args:`
        - filename (str): the path of the dataset.
        - binary (bool): if the dataset is binary or not. default: False.

    """

    # ==============================================================================
    # Constructor, all the variables and the algorithm are initialized here
    # ==============================================================================
    
    def __init__(self, file_path) -> None:

        self.utils = Utils() # Debugging object
        
        try:
            self.dataset_dict = arff.load(open(file_path, 'r')) # a dictionary with the dataset information

        except Exception as e:
            self.utils.debug("Error reading the dataset.", type="error")
            self.utils.debug(f"File path: {file_path}", type="error")
            print(e)
            exit()

        self.dataset_description = self.dataset_dict['description'] # a inlined string

        self.dataset_name = self.dataset_dict['relation'] # a inlined string

        self.dataset_attributes = self.dataset_dict['attributes'] #list of tuples [('attribute_name', 'value), ('', '')] both strings

        self.dataset_objects = self.dataset_dict['data'] #list of lists [[value, value, value], [value, value, value]] all strings

        

    # ==============================================================================
    # Functions to manipulate the datas
    # ==============================================================================

    def save_dataset(self, path):
        """
        Save the dataset in a new file.

        `Args:`
            - path (str): the path of the new file.
        """
        
        try:
            arff.dump(self.dataset_dict, open(path, 'w+'))
        except Exception as e:
            self.utils.debug("Error saving the dataset.", type="error")
            print(e)

    def get_dataset_info(self):
        return self.dataset_name, self.dataset_attributes, self.dataset_objects

    def get_numeric_categorical_info(self):
        numeric_indices = []
        categorical_indices = []
        for i, (attr_name, attr_type) in enumerate(self.dataset_attributes):
            if 'numeric' in attr_type.lower():
                numeric_indices.append(i)
            else:
                categorical_indices.append(i)
        return numeric_indices, categorical_indices
    
    def read_dataset(self):
        data = []
        a_class = []
        dist_class = []
        header_attr = []
        f_type = []

        for line in self.dataset_objects:
            v_value = []
            for i, value in enumerate(line[:-1]):
                v_value.append(float(value))
                if len(f_type) <= i:
                    f_type.append(1 if isinstance(value, (int, float)) else 2)
            classe = line[-1]
            if classe not in dist_class:
                dist_class.append(classe)
            a_class.append(classe)
            data.append(v_value)

        return data, a_class, dist_class, header_attr, f_type
  
