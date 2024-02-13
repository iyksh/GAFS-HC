def get_column(matriz, k):
    vec = []
    tam_lines = len(matriz)
    for j in range(tam_lines):
        vec.append(matriz[j][k])
    return vec

def class_level(possible_class):
    level_vec = []
    for i in range(len(possible_class)):
        aux_str = possible_class[i].split('.')
        level = len(aux_str)
        level_vec.append(level)
    return level_vec

def getMaxLevel(dist_class):
    maxlevel = 0
    for i in range(len(dist_class)):
        aux_str = dist_class[i].split('.')
        level = len(aux_str)
        if level > maxlevel:
            maxlevel = level
    return maxlevel

def classes_per_level(max_level, possible_class_level):
    total_classes_per_level = [0] * max_level
    for i in range(len(possible_class_level)):
        total_classes_per_level[int(possible_class_level[i]) - 1] += 1
    return total_classes_per_level

def a_class_to_vec(a_class, possible_class):
    # create occurrence matrix and initialize with zero
    occurrence = []

    concate = []

    # iterate over the distinct classes and create the possible classes vector
    for i in range(len(a_class)):
        instance_vec = [0] * len(possible_class)
        aux_str = a_class[i].split('.')
        level = len(aux_str)
        # add the superclass of the class to possible_class if it's not already in the vector
        for j in range(level):
            if j == 0:
                concate.append(aux_str[j])
            else:
                concate.append("." + aux_str[j])
            current_c = ''.join(concate)
            position = possible_class.index(current_c) if current_c in possible_class else -1
            if position != -1:
                instance_vec[position] = 1
        concate = []
        occurrence.append(instance_vec)

    return occurrence

def possible_class_hierarchy(a_class, dist_class):
    possible_class = []
    concate = []

    # iterate over the distinct classes and create the possible classes vector
    for i in range(len(dist_class)):
        aux_str = dist_class[i].split('.')
        level = len(aux_str)
        # add the superclass of the class to possible_class if it's not already in the vector
        for j in range(level):
            if j == 0:
                concate.append(aux_str[j])
            else:
                concate.append("." + aux_str[j])
            possible_c = ''.join(concate)
            if possible_c not in possible_class:
                possible_class.append(possible_c)  # if it's a new class, add it to the possible_class vector
        concate = []
    # sort the possible classes vector
    possible_class.sort()
    return possible_class
