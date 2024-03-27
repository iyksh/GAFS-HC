# ==============================================================================
# # This class is used to manipulate the dataset
# ==============================================================================

import arff
import numpy as np
import warnings

from sklearn.preprocessing import KBinsDiscretizer
from sklearn.model_selection import StratifiedKFold
from src.utils import Utils
from src.dataset import Dataset


class Preprocessing: 

    def __init__(self) -> None:
        self.utils = Utils()

    def split_dataset(self, original_path: str, test_path: str, train_path: str) -> None:
        # Load the original dataset
        original_dataset = arff.load(open(original_path, 'r'))

        # Get the data and shuffle it
        data = np.array(original_dataset['data'])

        # Get the labels (assuming they are in the last column)
        labels = data[:, -1]

        # Calculate the split points
        test_size = len(data) // 5
        train_size = len(data) - test_size

        # Split the data into test and train datasets
        test_data = np.array_split(data[:test_size], 5)
        train_data = np.array_split(data[test_size:], 5)

        # Create StratifiedKFold object
        skf = StratifiedKFold(n_splits=5)
        # Ignore warnings
   
        # Split the train data into 5 stratified folds
        warnings.filterwarnings("ignore", category=UserWarning)
        for i, data_part in enumerate(train_data):
            
            for train_index, val_index in skf.split(data_part, labels[test_size + i*len(data_part):test_size + (i+1)*len(data_part)]):
                
                # Create the train and validation datasets
                train_fold_data = data_part[train_index]

                # Create the train and validation datasets
                train_fold_dataset = original_dataset.copy()
                train_fold_dataset['data'] = train_fold_data.tolist()
                train_fold_dataset['description'] = f"Train fold {i}"
                
                arff.dump(train_fold_dataset, open(f"{train_path}_fold_{i}.arff", 'w'))

        # Split the test data into 5 stratified folds
        for i, data_part in enumerate(test_data):
            for train_index, val_index in skf.split(data_part, labels[i*len(data_part):(i+1)*len(data_part)]):
                
                # Create the train and validation datasets
                train_fold_data = data_part[train_index]

                # Create the train and validation datasets
                train_fold_dataset = original_dataset.copy()
                train_fold_dataset['data'] = train_fold_data.tolist()
                train_fold_dataset['description'] = f"Test fold {i}"

                arff.dump(train_fold_dataset, open(f"{test_path}_fold_{i}.arff", 'w'))
        
        warnings.catch_warnings()


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
            est = KBinsDiscretizer(n_bins=20, encode='ordinal', strategy='quantile')
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

        
        recursion_check = False

        for attribute in attributes_class[1]:
            if attribute != 'R' and attribute != None:
                filtered_attributes.append(attribute)
        for object in objects:
            if object[-1] != 'R':
                filtered_objects.append(object)


        for i in range(len(filtered_attributes[1])):
            count = 0
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

