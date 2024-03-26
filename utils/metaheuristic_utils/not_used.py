from utils_cfs import *
from pearson_coeff import *

def correlation_fl_multilabel(class_vec, data, f_type):
    """
    Create a vector of correlation between all features of the base and the class attribute,
    considering each class of the hierarchy as a binary class.

    Parameters:
    - class_vec (list): Matrix of occurrence with rows representing instances and columns representing possible classes.
    - data (list): Matrix of features with rows representing instances and columns representing features.
    - f_type (list): Vector indicating the type of each feature (1 for numerical, 2 for categorical).

    Returns:
    - list: Vector of correlation values between each feature and the class attribute.

    Raises:
    - ValueError: If the lengths of 'class_vec' and 'data' are not equal.
    """
    if len(class_vec) != len(data):
        raise ValueError("Lengths of 'class_vec' and 'data' must be equal.")

    correlation = []
    tam_class_vec = len(class_vec[0])
    tam_features = len(data[0])

    for k in range(tam_features):
        feature = [row[k] for row in data]

        sum_correlation = 0

        if f_type[k] == 1:  # Numerical feature
            for i in range(tam_class_vec):
                label = [row[i] for row in class_vec]
                pearson = np.abs(np.corrcoef(feature, label)[0, 1])
                sum_correlation += pearson
        else:  # Categorical feature
            for i in range(tam_class_vec):
                label = [row[i] for row in class_vec]
                pearson = pearsoncoeff_cat_num(feature, label)
                sum_correlation += np.abs(pearson)

        pearson_normal = sum_correlation / tam_class_vec
        correlation.append(pearson_normal)

    return correlation
