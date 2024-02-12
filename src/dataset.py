# ==============================================================================
# Main file to manipulate the dataset 
# 
#
# Author: Guilherme Santos
# Last edited: 2023-01-23
# ==============================================================================

import arff
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

        self.dataset_dict = arff.load(open(file_path, 'r')) # a dictionary with the dataset information

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
  
# ==============================================================================
# # This class is used to manipulate the dataset
# ==============================================================================

class DatasetManipulator: 

    # ==============================================================================
    # Constructor, all the variables and the algorithm are initialized here
    # ==============================================================================

    def __init__(self) -> None:
        self.utils = Utils()

    # ==============================================================================
    #  Functions to manipulate the datas
    # ==============================================================================

    def discretize_data(self, dataset_path: str, output_path: str) -> None:
        dataset = Dataset(dataset_path) # Create dataset object

        attributes = dataset.dataset_attributes # Get dataset attributes
        data = dataset.dataset_objects
        
        float_data = []
        classes_data = []

        for i in range(len(data)):
            try:
                float_data.append([float(x) for x in data[i][:-1]]) # strings -> floats
                classes_data.append(data[i][-1]) # Add classes to lists
            except:
                print(f"Error in line {i} of the dataset, removing it.")
                exit()


        # Discretize data using KBinsDiscretizer
        est = KBinsDiscretizer(n_bins=20, encode='ordinal', strategy='uniform', subsample=200)
        est.fit(float_data)
        discretized_data = est.transform(float_data)
        variance_per_feature = list([int(value) for value in np.unique(discretized_data)])
        variance_per_feature = list([str(value) for value in variance_per_feature])

        data = discretized_data.tolist()


        for i in range(len(discretized_data)):
            data[i] = [int(x) for x in data[i]] # floats -> strings
            data[i].append(classes_data[i]) # Add classes to discretized data

        for j in range(len(attributes)):
            if attributes[j][0].upper() == 'CLASS':
                break
            
            attributes[j] = (attributes[j][0], variance_per_feature)
            
        dataset.dataset_dict['attributes'] = attributes # Update dataset attributes
        dataset.dataset_dict['data'] = data # Update dataset data

        dataset.save_dataset(output_path) # Save the dataset in a new file

    

    def minimum_classes(self, dataset_path: str, output_path: str, minimum = 10) -> None:
        
        """ Remove classes with less than 10 instances or classes with only 'R' (root)
        
        if a class is removed, the function will be called again, until all classes have more than 10 instances.
        
        """
        dataset = Dataset(dataset_path) # Create dataset object

        attributes_class = dataset.dataset_attributes[-1]
        attributes = dataset.dataset_attributes[:-1]
        objects = dataset.dataset_objects

        filtered_attributes = []
        filtered_objects = []

        count = 0
        recursion_check = False

        for attribute in attributes_class[1]:
            if attribute != 'R' and attribute != None:
                filtered_attributes.append(attribute)
        for object in objects:
            if object[-1] != 'R':
                filtered_objects.append(object)


        for i in range(len(filtered_attributes[1])):
            for j in range(len(filtered_objects)):
                if filtered_attributes[i] == filtered_objects[j][-1]:
                    count += 1

            if count < minimum: 
                new_attributes = filtered_attributes[i].split('.')
                new_attributes.pop()
                new_attributes = '.'.join(new_attributes)

                self.utils.debug(f"Changing class {filtered_attributes[i]} with {count} instances from {new_attributes}")
                recursion_check = True

                if new_attributes == 'R':
                    self.utils.debug("The class is root, removing it.", "info")

                for k in range(len(filtered_objects)):
                    if filtered_attributes[i] == filtered_objects[k][-1]:
                        filtered_objects[k][-1] = new_attributes
                
                filtered_attributes[i] = new_attributes

        dataset.dataset_dict['attributes'][-1] = ('class', filtered_attributes)
        dataset.dataset_dict['data'] = filtered_objects
        dataset.save_dataset(output_path)

        if recursion_check:
            self.minimum_classes(output_path, output_path)