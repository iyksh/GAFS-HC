from dataset import Dataset
from metaheuristic_utils.utils_cfs import *
from metaheuristic_utils.pearson_coeff import *


class CorrelationFeatureSelection:
    """ Correlation Feature Selection (CFS) with hierarchical labels
    
    `Constructor:`
        - dataset_path (str): the path of the dataset.
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

        for k in range(tam_features - 1):
            correlation = []
            for j in range(k + 1, tam_features):
                f1 = get_column(data, k)
                f2 = get_column(data, j)

                if f_type[k] == 1 and f_type[j] == 1:  
                    pearson = pearsoncoeff(f1, f2) # numeric and numeric
                elif f_type[k] == 1 and f_type[j] == 2:  
                    pearson = pearsoncoeff_cat_num(f2, f1) # numeric and categorical
                elif f_type[k] == 2 and f_type[j] == 1:  
                    pearson = pearsoncoeff_cat_num(f1, f2) # categorical and numeric
                else:  
                    pearson = pearsoncoeff_cat_cat(f1, f2) # categorical and categorical

                correlation.append(pearson)

            correlation_matrix.append(correlation)

        return correlation_matrix

    def get_dataset_correlations(self) -> tuple[list[float], list[float]]:
        """ - Returns the correlation between features and labels and the correlation between features and features"""

        dataset_obj = Dataset(self.dataset_path)
        data, a_class, dist_class, header_attr, f_type = dataset_obj.read_dataset()

        possible_classes = possible_class_hierarchy(a_class, dist_class)
        a_class_vec = a_class_to_vec(a_class, possible_classes)
        classes_level = class_level(possible_classes)
        max_level = getMaxLevel(dist_class)
        number_classes_per_level = classes_per_level(max_level, classes_level)

        correlation_fl_hierar = self.correlation_fl_hierarchical(a_class_vec, data, f_type, classes_level, 0.75, number_classes_per_level)
        ccorrelation_f_to_f = self.correlation_ff_hierarchical(data, f_type)


        return (correlation_fl_hierar, ccorrelation_f_to_f)


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

        merit_denominator = np.sqrt(tam_features + (tam_features * (tam_features - 1) * sum_correlation_ff))
        if np.isnan(merit_denominator):
            merit_denominator = 0.00000001


        return (tam_features * sum_correlation_fl)/merit_denominator # merit value
    
    def evaluate(self, fitness:list[float], population:list[list[int]], 
                 correlation_f_to_f:list[float], correlation_fl_hierar:list[float]) -> tuple[list[float]]:
        """
        Evaluate the fitness of the individuals in the population

        `Args:`
            - fitness: list[float] - list of fitness values
            - population: list[list[int]] - list of lists of binary festures
            - correlation_f_to_f: list[float] - correlation between features and features
            - correlation_fl_hierar: list[float] - correlation between features and labels
        

        """
        # Not working yet 
        # maybe chromossome -> file, evaluate -> merit of the file 

        dataset = Dataset(self.dataset_path)
        """             
        att_analyses = []
        att_vec_avg = []
        best_att = worse_att = avg_att = 0
        best_merit = 0
        worse_merit = 100
        for i, individual in enumerate(population):
            att = dataset.save_dataset(individual)
            size_set = len(att)
            merit_open = in_list_candidate(size_set, att, open_candidates)
            if merit_open == -1:
                new_set = Candidate()
                new_set.att = att
                set_vec = list(att)
                if len(set_vec) < 1:
                    fitness[i] = 0.0
                elif len(set_vec) == 1:
                    fitness[i] = correlation_fl_vec[set_vec[0]]
                else:
                    fo_cfs_hierarq = merit_cfs(set_vec, correlation_ff_mat, correlation_fl_vec)
                    new_set.merit = fo_cfs_hierarq[0]
                    new_set.size_set = size_set
                    open_candidates.append(new_set)
                    new_set_queue = CandidateQueue(new_set.merit, len(open_candidates) - 1)
                    heappush(open_queue, new_set_queue)
                    fitness[i] = new_set.merit
            else:
                fitness[i] = merit_open

            if fitness[i] > best_merit:
                best_merit = fitness[i]
                best_att = size_set
            elif fitness[i] < worse_merit:
                worse_merit = fitness[i]
                worse_att = size_set

            att_vec_avg.append(size_set)

        avg_att = mean(att_vec_avg)
        att_analyses.extend([best_att, worse_att, avg_att])
        
        return att_analyses
        """


# ==============================================================================
# Example of use
# ==============================================================================


if __name__ == "__main__":
    dataset_path = "/home/yksh/Desktop/temp/SPO_test.arff"
    
    cfs = CorrelationFeatureSelection(dataset_path)

    fl, ff = cfs.get_dataset_correlations()
    fitness = [0 for i in range(2)]
    s = [1, 0]
    merit = cfs.merit(s, ff, fl)  # receives the att vector of the solution and calculates multilabel merit
    fitness = cfs.evaluate(fitness, s, ff, fl)

    print(f"Merit: {merit}")


