import numpy as np

def sum_vc(a):
    return sum(a)

def mean(b):
    return sum_vc(b) / len(b)

def sqsum(a):
    s = 0
    for i in range(len(a)):
        s += a[i]**2
    return s

def stdev(a):
    return sqsum(a)**0.5

def operator_subtract(a, b):
    retvect = a.copy()
    for i in range(len(a)):
        retvect[i] = a[i] - b
    return retvect

def operator_multiply(a, b):
    retvect = a.copy()
    for i in range(len(a)):
        retvect[i] = a[i] * b[i]
    return retvect

def pearsoncoeff(a, b):
    dif_a, dif_b, mul = a.copy(), a.copy(), a.copy()

    mean_a = mean(a)
    mean_b = mean(b)
    dif_a = operator_subtract(a, mean_a)
    dif_b = operator_subtract(b, mean_b)
    mul = operator_multiply(dif_a, dif_b)

    try:
        pearson = abs((sum_vc(mul))/(stdev(dif_a)*stdev(dif_b)))
    except ZeroDivisionError:
        pearson = 0.00000001
    return pearson

def binary_vec(k, a):
    tam = len(a)
    b = [0]*tam
    for i in range(len(a)):
        if a[i] == k:
            b[i] = 1
    return b

def pearsoncoeff_cat_num(a, b):
    binary = []
    pearson = 0
    sum = 0
    tam = len(a)
    dist = list(set(a))
    freq = [a.count(i) for i in dist]
    for k in range(len(dist)):
        binary = binary_vec(dist[k], a)
        pearson = pearsoncoeff(binary, b)
        sum += ((freq[k]/tam)*abs(pearson))
    return sum

def prob_a_and_b(a, b):
    tam = len(a)
    sum = 0
    for k in range(tam):
        if a[k] == 1 and b[k] == 1:
            sum += 1
    return (sum/tam)

def pearsoncoeff_cat_cat(a, b):
    binary_a = []
    binary_b = []
    prop = 0
    pearson = 0
    sum = 0
    dist_a = list(set(a))
    dist_b = list(set(b))

    for k in range(len(dist_a)):
        binary_a = binary_vec(dist_a[k], a)
        for i in range(len(dist_b)):
            binary_b = binary_vec(dist_b[i], b)
            prop = prob_a_and_b(binary_a, binary_b)
            pearson = pearsoncoeff(binary_a, binary_b)
            sum += (prop*abs(pearson))
    return sum