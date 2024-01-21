import os
import matplotlib.pyplot as plt

class Utils:

    def delete_chromossomes(self):
        current_directory = "./"
        files = os.listdir(current_directory)
        for file in files:
            if file.endswith('.arff') and (file.startswith('chromossome')):
                file_path = os.path.join(current_directory, file)
                os.remove(file_path)
                
                
    def pause(self):
        input("Press the <ENTER> key to continue...")


    def print_population_fitness(self, population_fitness, generation):
        best_fitness = f"{max(population_fitness):.3f}"
        average_fitness = f"{sum(population_fitness) / len(population_fitness):.3f}"
        worst_fitness = f"{min(population_fitness):.3f}"

        self.debug(f"Generation {generation}: ")
        self.debug(f"Best fitness: {best_fitness}")
        self.debug(f"Average fitness: {average_fitness}")
        self.debug(f"Worst fitness: {worst_fitness}")

    def clear_screen(self):
        print("\033[H\033[J")


    def plot_fitness_history(self, fitness_history, title = 'Avarage-Fitness History'):
        """
        Plot the fitness history.

        Parameters:
        - fitness_history (list): List containing fitness scores for each generation.
        """
        # Plotting the fitness history
        plt.plot(range(1, len(fitness_history) + 1), fitness_history, marker='o', linestyle='-')
        plt.title(title)
        plt.xlabel('Generation')
        plt.ylabel('Fitness Score')
        plt.grid(True)
        plt.show()
    

    def debug(self, text, type = "debug"):

        if type == "error":
            print("\033[1;31m" + "[Error]: " + "\033[0m" + text)
                
        elif type == "warning":
            print("\033[1;33m" + "[Warning]: " + "\033[0m" + text)
        
        elif type == "info":
            print("\033[1;34m" + "[Info]: " + "\033[0m" + text)
            
        elif type == "success":
            print("\033[1;32m" + "[Success]: " + "\033[0m" + text)
                
        else:
            print("\033[1;35m" + "[Debug]: " + "\033[0m" + text)
        

