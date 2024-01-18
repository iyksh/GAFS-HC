import random
import os

from utils import *
from dataset import Dataset
from cross_validation import *

class genetic_operators:

    def __init__(self) -> None:
        pass


    def tournament_selection(self, population:list, fitness_scores:list, tournament_size = 2, k = 0.75) -> list:
        selected_parents = []
        for _ in range(len(population)):
            tournament_indices = random.sample(range(len(population)), tournament_size)
            tournament_candidates = [population[i] for i in tournament_indices]
            tournament_fitness = [fitness_scores[i] for i in tournament_indices]

            if random.random() < k:
                selected_parent = tournament_candidates[tournament_fitness.index(max(tournament_fitness))]
            else:
                selected_parent = tournament_candidates[tournament_fitness.index(min(tournament_fitness))]

            selected_parents.append(selected_parent)
        return selected_parents

    def pmx_crossover_chromossomes(self, parent1, parent2):
        crossover_point1 = random.randint(0, len(parent1) - 1)
        crossover_point2 = random.randint(crossover_point1 + 1, len(parent1))

        child = [-1] * len(parent1)
        elements_in_child = set(parent1[crossover_point1:crossover_point2])

        for i in range(crossover_point1, crossover_point2):
            child[i] = parent1[i]

        for i in range(len(parent2)):
            if parent2[i] not in elements_in_child:
                empty_index = child.index(-1)
                child[empty_index] = parent2[i]
                elements_in_child.add(parent2[i])

        # Ensure the child is a valid binary representation
        for i in range(len(child)):
            if child[i] == -1:
                child[i] = parent2[i]  # Fill remaining positions with values from the second parent

        return child

    def pmx_crossover(self, population:list, crossover_rate=0.8) -> list:
        new_population = []
        for i in range(0, len(population)-1, 2):
            parent1 = population[i]
            parent2 = population[i + 1]


            if random.random() < crossover_rate:
                child1 = self.pmx_crossover_chromossomes(parent1, parent2)
                child2 = self.pmx_crossover_chromossomes(parent2, parent1)
            else:
                child1 = parent1
                child2 = parent2

            new_population.append(child1)
            new_population.append(child2)

        return new_population
    

    def swap_mutation(self, population:list, mutation_rate=0.1) -> list:
        for i in range(len(population)):
            if random.random() < mutation_rate:
                mutation_point1 = random.randint(0, len(population[i]) - 1)
                mutation_point2 = random.randint(0, len(population[i]) - 1)

                population[i][mutation_point1], population[i][mutation_point2] = population[i][mutation_point2], \
                                                                                 population[i][mutation_point1]

        return population
    

    def elitism(self, population:list, fitness_scores:list, num_elites:int) -> list:
        """
        Selects elite individuals based on fitness scores and replaces random individuals in the population with them.
        """
        elites = []
        for _ in range(num_elites):
            max_index, max_fitness = max(enumerate(fitness_scores), key=lambda x: x[1])
            elites.append(population[max_index])
            fitness_scores.pop(max_index)

        for elite_individual in elites:
            random_index = random.randint(0, len(population) - 1)
            population[random_index] = elite_individual

        return population






#                                                                   #
#                                                                   #
#                   Usage examples:                                 #
#                                                                   #
#                                                                   #
#                                                                   #
    
if __name__ == "__main__":

    operators = genetic_operators()
    population = [[1, 1, 0, 0, 1], [0, 1, 0, 0, 0], [1, 1, 0, 1, 1], [0, 1, 0, 0, 0]]  # list of chromosomes 
    fitness_scores = [34.72222137451172, 23.58974266052246, 24.72222137451172, 15.58974266052246]  # Corresponding fitness 

    # Tournament Selection
    selected_parents = operators.tournament_selection(population, fitness_scores)

    print(selected_parents)

    """
    # PMX Crossover
    child = operators.pmx_crossover(selected_parents)
    

    child = operators.swap_mutation(population)
    print(child)

    elits = operators.elitism(population, fitness_scores, 1)
    print(elits)
    """






