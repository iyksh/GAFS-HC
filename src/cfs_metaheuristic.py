import time

from queue import PriorityQueue
from dataset import Dataset
from metaheuristic_utils.utils_cfs import *
from metaheuristic_utils.pearson_coeff import *

def correlation_fl_hierarchical(class_vec, data, f_type, class_level, w_0, classes_per_level):
    correlation = []
    sum_weight = 0
    tam_class_vec = len(class_vec[0])
    tam_features = len(data[0])
    
    # calculate the total weights multiplied by the total classes per level of the hierarchy (denominator of the rFL calculation)
    for k in range(len(classes_per_level)):
        sum_weight += (pow(w_0, k+1)*classes_per_level[k])
    
    for k in range(tam_features):
        feature = get_column(data, k)
        sum_correlation = 0
        # if f_type is 1, att is numeric, if it is 2, it is categorical
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

def correlation_f_to_f_vec(data, f_type):
    correlation_matrix = []
    tam_features = len(data[0])

    for k in range(tam_features - 1):
        correlation = []
        for j in range(k + 1, tam_features):
            f1 = get_column(data, k)
            f2 = get_column(data, j)

            if f_type[k] == 1 and f_type[j] == 1:  # numeric and numeric
                pearson = pearsoncoeff(f1, f2)
            elif f_type[k] == 1 and f_type[j] == 2:  # numeric and categorical
                pearson = pearsoncoeff_cat_num(f2, f1)
            elif f_type[k] == 2 and f_type[j] == 1:  # categorical and numeric
                pearson = pearsoncoeff_cat_num(f1, f2)
            else:  # categorical and categorical
                pearson = pearsoncoeff_cat_cat(f1, f2)

            correlation.append(pearson)

        correlation_matrix.append(correlation)

    return correlation_matrix


def get_dataset_correlations(path):

    file = Dataset(path)
    header_attr = file.dataset_attributes[:-1]
    f_type = [1 if "numeric" in attr[1] else 2 for attr in header_attr]
    dataset_objects = file.dataset_objects
    dist_class = []
    a_class = []
    data = []

    for i in range(len(dataset_objects)):
        v_value = []
        line = dataset_objects[i]
        for j in range(len(line) - 1):
            v_value.append(float(line[j]))
        
        classe = line[len(line) - 1]
        if classe not in dist_class:
            dist_class.append(classe)
        a_class.append(classe)
        data.append(v_value)
    

    possible_classes = possible_class_hierarchy(a_class, dist_class)
    a_class_vec = a_class_to_vec(a_class, possible_classes)

    classes_level = class_level(possible_classes)
    max_level = getMaxLevel(dist_class)
    number_classes_per_level = classes_per_level(max_level, classes_level)

    fl_time = time.time()

    correlation_fl_hierar = correlation_fl_hierarchical(a_class_vec, data, f_type, classes_level, 0.75, number_classes_per_level)
    fl_time = time.time() - fl_time
    ff_time = time.time()
    ccorrelation_f_to_f = correlation_f_to_f_vec(data, f_type)
    ff_time = time.time() - ff_time

    print(f"Feature-Feature Correlation Time: {ff_time}")
    print(f"Feature-Class Correlation Time: {fl_time}")

    return correlation_fl_hierar, ccorrelation_f_to_f


def merit_cfs(s, correlation_ff_mat, correlation_fl_vec):
    merit = []
    att_vec = sorted(s)
    tam_features = len(att_vec)
    sum_correlation_ff = 0
    sum_correlation_fl = 0

    for k in range(tam_features - 1):
        for j in range(k + 1, tam_features):
            sum_correlation_ff += correlation_ff_mat[att_vec[k]][att_vec[j] - att_vec[k] - 1]

    for k in range(tam_features):
        sum_correlation_fl += correlation_fl_vec[att_vec[k]]

    merit_denominator = np.sqrt(tam_features + (tam_features * (tam_features - 1) * sum_correlation_ff))
    if np.isnan(merit_denominator):
        merit_denominator = 0.00000001

    merit_value = (tam_features * sum_correlation_fl) / (merit_denominator)
    merit.append(merit_value)

    return merit

"""
def evaluate(open, open_queue, fitness, population, correlation_ff_mat, correlation_fl_vec):
    att_analises = []
    att_vec_avg = []
    best_att = 0
    worse_att = 100
    best_merit = 0
    worse_merit = 100
    for i in range(len(population)):
        aux = set(population[i])
        size_set = len(aux)
        merit_open = in_list_candidate(size_set, aux, open)
        if merit_open == -1:
            new_set = Candidate()
            new_set.att = aux
            set_vec = list(aux)
            if len(set_vec) < 1:
                fitness[i] = 0.0
            elif len(set_vec) == 1:
                fitness[i] = correlation_fl_vec[set_vec[0]]
            else:
                fo_cfs_hierarq = merit_cfs(set_vec, correlation_ff_mat, correlation_fl_vec)
                new_set.merit = fo_cfs_hierarq[0]
                new_set.size_set = size_set
                open.append(new_set)
                new_set_queue = CandidateQueue()
                new_set_queue.merit = new_set.merit
                new_set_queue.position = len(open) - 1
                open_queue.put(new_set_queue)
                fitness[i] = new_set.merit
        else:
            fitness[i] = merit_open
        if fitness[i] > best_merit:
            best_merit = fitness[i]
            best_att = size_set
        elif fitness[i] < worse_merit:
            worse_merit = fitness[i]
            worse_att = size_set
        att_vec_avg.append(float(size_set))
    avg_att = mean(att_vec_avg)
    att_analises.append(best_att)
    att_analises.append(worse_att)
    att_analises.append(avg_att)
    return att_analises
"""


########################################################################

if __name__ == "__main__":
    dataset_path = "/home/yksh/Desktop/temp/CellCycle_test.arff"
    
    
    fl, ff = get_dataset_correlations(dataset_path)


    s = [1, 0]
    merit = merit_cfs(s, ff, fl)  # receives the att vector of the solution and calculates multilabel merit
    
    print(f"Merit: {merit}")


