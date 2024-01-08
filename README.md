# A Genetic Algorithm for Feature Selection in Hierarchical Classification

## Introduction

Feature selection is a widely adopted preprocessing step in the field of data mining. One of its objectives is to reduce the number of original attributes in a database to enhance the performance of a predictive model. 

However, despite the benefits of feature selection for classification tasks, as far as we know, few studies in the literature address attribute selection for the context of hierarchical classification. 

This project proposes the use of genetic algorithms in a hybrid supervised feature selection approach, combining filter-type metrics adapted for hierarchical classification with the use of genetic algorithms to explore the subset space of attributes.


## Table of Contents
- [Objectives](#Objectives)
- [How to use](#How-to-use)
- [Contact Information](#Contact)
- [Requirements and libraries descriptions](#Requirements)

## Objectives

The main goalis to propose the development of a hybrid feature selection method that takes into account the hierarchy of classes, combining correlation-based filter techniques to assess the quality of attribute subsets and genetic algorithm-based techniques to search for attribute subsets. This aims to construct solutions capable of improving the predictive performance of global hierarchical classifiers. In this regard, the specific objectives of this work are:

1. **Development of a hybrid feature selection method**: This method needs to be:
   - Fast;
   - Scalable;
   - Capable of reducing the number of attributes in databases without compromising the classification model's performance.

2. **Experiments**: Conducting computational experiments using hierarchical databases related to protein function prediction and image problems.

3. **Analyzing the state of the art**: Comparing the proposed approach with other feature selection methods available in the literature and with the use of global classifiers without attribute selection.

## How-to-use

To get started, you'll need a .arff file for both the training and testing datasets. Ensure that these datasets are discretized following this format:

``` .arff 

@relation ExampleDataset

@ATTRIBUTE attribute1 {value1, value2, value3}
@ATTRIBUTE attribute2 {value4, value5, value6}
@ATTRIBUTE attribute3 {value7, value8, value9}
@ATTRIBUTE class {x1, x2, x3}

@data
value1, value4, value7, x1
value2, value5, value8, x2
value3, value6, value9, x3

```


For discretization, you can employ the KBinsDiscretizer from sklearn.preprocessing, which is already integrated into the project and can be found in `./src/dataset.py`.

Once your datasets are prepared, update the file paths in `./src/main.py` to point to your respective training and testing files. This ensures that the main script operates on the correct data. Following these steps, you'll be ready to use the project effectively.

## Contact

For any inquiries or suggestions, please don't hesitate to contact me. You can reach me at my [e-mail](mailto:gssantoz2012@gmail.com) for more information.

Thank you for your interest!

## Requirements
Ensure the following dependencies are installed before running the project:

- **LIAC-ARFF Library**: You can obtain the LIAC-ARFF library from: https://github.com/renatopp/liac-arff. 
This library is essential for reading and writing ARFF files, providing a seamless interaction with ARFF-formatted datasets.

- **scikit-learn**: The project relies on scikit-learn, a widely-used machine learning library in Python. 

- **Pandas**: It provides data structures like DataFrame for efficient handling of structured data. 

- **NumPy**: It provides support for large, multi-dimensional arrays and matrices, along with mathematical functions to operate on these elements.

- **MatplotLib**: It is employed in this project for data visualization, enabling the generation of informative plots and charts.