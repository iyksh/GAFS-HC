import random

from src.utils import *
from src.cpp_converter import call_nbayes
from src.dataset import Dataset

class genetic_operators:

    def __init__(self) -> None:
        self.utils = Utils()
        pass
    
    def create_population(self, population_size: int, len_attributes:int) -> list[list[int]]:
        """
        Create the initial population with random genes (0 or 1).
        
        - 0 means that the attribute will not be selected, and 1 means that the attribute will be selected.

        """

        population = []

        for _ in range(population_size):
            chromosome = [random.randint(0, 1) for _ in range(len_attributes)]

            # Ensure at least one attributes is selected
            if chromosome.count(1) == 0:
                chromosome[random.randint(0, len_attributes - 1)] = 1

            population.append(chromosome)

        return population

    def roulette_selection(self, population, fitness_scores):
        total_fitness = sum(fitness_scores)
        normalized_fitness = [score / total_fitness for score in fitness_scores]

        # Criar uma roleta ponderada
        cumulative_probabilities = [sum(normalized_fitness[:i+1]) for i in range(len(normalized_fitness))]

        # Selecionar indivíduos
        selected_population = []
        for _ in range(len(population)):
            rand_num = random.random()
            selected_index = next(i for i, cum_prob in enumerate(cumulative_probabilities) if rand_num <= cum_prob)
            selected_population.append(population[selected_index])

        return selected_population


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

    def pmx_crossover(self, population:list, crossover_rate) -> list:
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
    

    def swap_mutation(self, population:list, mutation_rate) -> list:
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
    







