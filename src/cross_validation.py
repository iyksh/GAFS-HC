import pandas as pd
import os

from dataset import Dataset    
from sklearn.model_selection import StratifiedKFold
from call_nbayes import call_nbayes
import warnings

def five_folds(path_dataset: str, type = "train") -> None:
    """Divide the dataset into 5 parts, and each part is saved in a .arff file.
    
    The dataset is divided using StratifiedKFold,
    to maintain class proportions during cross-validation.
    
    `Args:`
        - path_dataset (str): the path of the dataset to be discretized
        - type (str): if the dataset is the train dataset or the test dataset, this is used to name the files.
        
    `Returns:`
        - A new dataset with the discretized data.
        
    
    """
    dataset = Dataset(path_dataset)

    # Load datasets

    data_list_test = dataset.dataset_objects
    df_test = pd.DataFrame(data_list_test)
    
    
    X_test = df_test.iloc[:, :-1]   # Separating the attributes and 
    y_test = df_test.iloc[:, -1]    # the classes for test dataset

    # Using StratifiedKFold to maintain class proportions during cross-validation for test dataset
    skf_test = StratifiedKFold(n_splits=5, random_state=42, shuffle=True)
    
    warnings.filterwarnings("ignore", category=UserWarning)
    for i, (train_index_test, test_index_test) in enumerate(skf_test.split(X_test, y_test)):


        X_train_test, X_test_test = X_test.iloc[train_index_test], X_test.iloc[test_index_test]
        y_train_test, y_test_test = y_test.iloc[train_index_test], y_test.iloc[test_index_test]

        test_data_test = pd.concat([X_test_test, y_test_test], axis=1).astype(str).values.tolist()
        test_df_test = pd.DataFrame(test_data_test, columns=df_test.columns)
        
        # Saving the DataFrames to .arff files
        path = f'{type}_{i + 0}.arff'
        test_df_test.to_csv(path, index=False, header=False)

        fold_data = []
        with open(path, 'r') as file:
            for line in file:
                fold_data.append(line.strip().split(','))

        description = dataset.dataset_dict['description']
        dataset.dataset_dict['description'] = f'{description}_fold({i + 1})'
        dataset.dataset_dict['data'] = fold_data
        dataset.save_dataset(path)
        dataset.dataset_dict['description'] = description

    warnings.catch_warnings()
 

def cross_validation(dataset_test_path: str, dataset_train_path: str, num_folds = 5) -> float:
    """Make cross validation using the 5 parts of the dataset, with nbayes global model algorithm.
    
    `Args:`
        - dataset_test_path (str): the path of the test dataset (chromosome)
        - dataset_train_path (str): the path of the train dataset 
        
    `Returns:`
        - None    
    """

    five_folds(dataset_test_path, type= "test")
    five_folds(dataset_train_path, type= "train")

    sum_nbayes = 0 
    sum_iteration = 0
    
    for i in range(num_folds):
        for j in range(num_folds):
            if i != j:
                #print(f"Cross-validation: test_{i} -> train_{j}")
                sum_iteration += call_nbayes(f'train_{j}.arff', f'test_{i}.arff')


        sum_iteration /= num_folds
        sum_nbayes += sum_iteration

    sum_nbayes /= num_folds

    
    
    current_directory = os.getcwd()
    for filename in os.listdir(current_directory): # Delete the files created by five_folds function
        if filename.startswith("train") or filename.startswith("test") or filename.startswith("result"):
            file_path = os.path.join(current_directory, filename)
            os.remove(file_path)

    #print(f"GMNbayes cross-validation: {sum_nbayes}")

    return sum_nbayes

#
#
#   Example of use  
#
#


if __name__ == "__main__": #
    
    os.system('cls' if os.name == 'nt' else 'clear') 
    dataset_test_output_path = 'datasets/cellcyle/CellCycle_test_discretized.arff'
    dataset_train_output_path = 'datasets/cellcyle/CellCycle_train_discretized.arff'
    
    cross_validation(dataset_test_output_path, dataset_train_output_path)