from src.dataset import Dataset
from src.metaheuristic_utils.utils_cfs import *
from src.metaheuristic_utils.pearson_coeff import *
from src.population_manager import Population

import multiprocessing
import random
import numpy as np

class CorrelationFeatureSelection:
    """ Correlation Feature Selection (CFS) with hierarchical labels
    
    `Constructor:`
        - dataset_path (str): the path of the dataset.
    
    `Warning:`
        - The datastpath need to be divided by five folds.
    
    """

    def __init__(self, dataset_path:str) -> None:
        self.dataset_path = dataset_path

        pass

    def correlation_fl_hierarchical(self, class_vec, data, f_type, class_level, w_0, classes_per_level):
        correlation = []
        sum_weight = 0
        tam_class_vec = len(class_vec[0])
        tam_features = len(data[0])
        
        for k in range(len(classes_per_level)):
            sum_weight += (pow(w_0, k+1)*classes_per_level[k])
        
        for k in range(tam_features):
            print(f"Calculating correlation between feature {k} of {tam_features - 1} and labels")
            feature = get_column(data, k)
            sum_correlation = 0

            if f_type[k] == 1:
                for i in range(tam_class_vec):
                    label = get_column(class_vec, i)
                    pearson = pearsoncoeff(feature, label)
                    sum_correlation += abs(pearson) * (pow(w_0, class_level[i]))
            else:
                for i in range(tam_class_vec):
                    label = get_column(class_vec, i)
                    pearson = pearsoncoeff_cat_num(feature, label)
                    sum_correlation += abs(pearson) * (pow(w_0, class_level[i]))

            pearson_normal = sum_correlation / sum_weight
            correlation.append(pearson_normal)

        return correlation

    def correlation_ff_hierarchical(self, data, f_type):
        correlation_matrix = []
        tam_features = len(data[0])
        data = np.array(data)

        for k in range(tam_features - 1):
            print(f"Calculating correlation between features {k} of {tam_features - 1}")
            correlation = []
            f1 = data[:, k]
            
            for j in range(k + 1, tam_features):
                f2 = data[:, j]
                
                if f_type[k] == 1 and f_type[j] == 1:  
                    pearson = np.corrcoef(f1, f2)[0, 1]  # numeric and numeric
                elif f_type[k] == 1 and f_type[j] == 2:  
                    pearson = pearsoncoeff_cat_num(f2, f1)  # numeric and categorical
                elif f_type[k] == 2 and f_type[j] == 1:  
                    pearson = pearsoncoeff_cat_num(f1, f2)  # categorical and numeric
                else:  
                    pearson = pearsoncoeff_cat_cat(f1, f2)  # categorical and categorical

                correlation.append(pearson)

            correlation_matrix.append(correlation)

        return correlation_matrix

    def get_dataset_correlations(self) -> tuple[list[float], list[float]]:
        """ - Returns the correlation between features and labels and the correlation between features and features"""

        print(f"Reading dataset: {self.dataset_path}")
        dataset_obj = Dataset(self.dataset_path)
        data, a_class, dist_class, header_attr, f_type = dataset_obj.read_dataset()

        print(f"Calculating correlations")
        possible_classes = possible_class_hierarchy(a_class, dist_class)
        a_class_vec = a_class_to_vec(a_class, possible_classes)
        classes_level = class_level(possible_classes)
        max_level = getMaxLevel(dist_class)
        number_classes_per_level = classes_per_level(max_level, classes_level)


        with multiprocessing.Pool(processes=2) as pool:
            # Run the functions in parallel
            fl = pool.apply_async(self.correlation_fl_hierarchical, (a_class_vec, data, f_type, classes_level, 0.75, number_classes_per_level))
            ff = pool.apply_async(self.correlation_ff_hierarchical, (data, f_type))

            # Get the results
            correlation_fl_hierar = fl.get()
            correlation_f_to_f = ff.get()

        return correlation_fl_hierar, correlation_f_to_f



    def merit(self, s:list, correlation_ff:list, correlation_fl:list) -> float:
        """ - Returns the merit value of a feature subset
        
       `Args:`
            - s: list[int] - feature subset
            - correlation_ff: list[float] - correlation between features and features
            - correlation_fl: list[float] - correlation between features and labels
        """

        att_vec = sorted(s)
        tam_features = len(att_vec)
        sum_correlation_ff = 0
        sum_correlation_fl = 0

        for k in range(tam_features - 1):
            for j in range(k + 1, tam_features):
                sum_correlation_ff += correlation_ff[att_vec[k]][att_vec[j] - att_vec[k] - 1]

        for k in range(tam_features):
            sum_correlation_fl += correlation_fl[att_vec[k]]

        merit_denominator = pow(tam_features + (tam_features * (tam_features - 1) * sum_correlation_ff), 0.5)
        if np.isnan(merit_denominator):
            merit_denominator = 0.00000001


        return (tam_features * sum_correlation_fl)/merit_denominator # merit value
    
    def evaluate_population(self, population:list[list[int]], 
                 correlation_f_to_f:list[float], correlation_fl_hierar:list[float]) -> tuple[list[float]]:

        fitness = [0 for i in range(len(population))]

        for i, individual in enumerate(population):
            
            set_vec = []
            for j in range(len(individual)):
                if individual[j] == 1:
                    set_vec.append(j)

            if len(set_vec) == 0:
                fitness[i] = 0.0
            elif len(set_vec) == 1:
                fitness[i] = correlation_fl_hierar[set_vec[0]]
            
            else:
                fitness[i] = self.merit(set_vec, correlation_f_to_f, correlation_fl_hierar)
        
        return fitness, "Not making analyses, to improve the performance of the algorithm"
    
    def hierarchicalCFS(self, population, fl, ff) -> tuple[list[float], list[float]]:
        """ - Run the hierarchical CFS algorithm
        
        `Args:`
            - population: list[list[int]] - the population to be evaluated
        
        `Returns:`
            - tuple[list[float], list[float]] - the fitness of the population and the analyses of the features
            
        """
        fitness, analyses = self.evaluate_population(population, ff, fl)

        return fitness, analyses
    
        
        


# ==============================================================================
# Example of use
# ==============================================================================

def create_population(population_size: int, default_dataset = False, chromossome_len = 0) -> list[list[int]]:

        len_attributes = chromossome_len
        population = []

        if default_dataset:
            return [[1 for _ in range(len_attributes)] for _ in range(population_size)]

        for _ in range(population_size):
            chromosome = [random.randint(0, 1) for _ in range(len_attributes)]

            # Ensure at least one attributes is selected
            if chromosome.count(1) == 0:
                chromosome[random.randint(0, len_attributes - 1)] = 1

            population.append(chromosome)

        return population

def cfs_example_usage() -> None:

    dataset_path = "/home/yksh/Desktop/temp/SPO_test.arff"
    cfs = CorrelationFeatureSelection(dataset_path)


    dataset = Dataset(dataset_path)
    population = create_population(10, False, len(dataset.dataset_attributes) - 1)
    fl, ff = cfs.get_dataset_correlations()  

    fitness, analyses = cfs.hierarchicalCFS(population, fl , ff)
    
    
    print(f"Fitness: {fitness}")
    print(f"Analyses: {analyses}")




