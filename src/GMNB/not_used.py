################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
########################## NOT USED #############################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################

from src.dataset import Dataset
from src.utils import Utils 
import random

# ==============================================================================
# Class to manipulate classes (outdated)
# ==============================================================================

class ClassPopulation:

    def __init__(self, test_dataset_path) -> None:
        self.data = Dataset(test_dataset_path)
        self.filepath = test_dataset_path
        self.chromossome_path = "./chromossome.arff"
        self.utils = Utils()
        self.cross_validation_warning = False


    def create_population(self, population_size: int) -> list:
        """
        Create the initial population with random genes (0 or 1).
        
        - 0 means that the attribute will not be selected, and 1 means that the gene of the attribute_class will be selected.

        """


        len_attributes = len(self.data.dataset_attributes[-1][1])
        population = []

        for _ in range(population_size):
            chromosome = [random.randint(0, 1) for _ in range(len_attributes)]

            # Ensure at least one attributes is selected
            if chromosome.count(1) == 0:
                chromosome[random.randint(0, len_attributes - 1)] = 1

            population.append(chromosome)

        return population

        
    def convert_chromossome_to_file(self, chromosome: list, path = None, description = None) -> None:
        """
        Convert a chromosome list with binary encoding (e.g., [0, 1, 0, 1]) to a .arff file.

        Attributes with a binary value of 0 will be excluded from the resulting dataset.

        Parameters:
            chromosome (list): Binary-encoded chromosome representing attribute selection.

        Note:
            The resulting .arff file is saved as `chromossome.arff`, by the default self.chromossome_path, if the path is not specified.
        """

        if path == None:
            path = self.chromossome_path

        temporary_chromossome = Dataset(self.filepath)
        attributes_class = self.data.dataset_attributes[-1][1]

        attributes = []
        objects = []

        for i in range(len(attributes_class)): # The chromosome size is equal to the number of attributes
            if chromosome[i] == 1:
                attributes.append(attributes_class[i])
        

        for i in range(len(self.data.dataset_objects)):
            if self.data.dataset_objects[i][-1] in attributes:
                objects.append(self.data.dataset_objects[i])
            
        if description != None:
            temporary_chromossome.dataset_dict['description'] = description
    
        
        temporary_chromossome.dataset_dict['data'] = objects
        temporary_chromossome.dataset_dict['attributes'][-1] = ('class', attributes)
        temporary_chromossome.save_dataset(path)




