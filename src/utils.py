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


    def plot_fitness_history_file(self, report_num, pop_size, best_fitness, avg_fitness_history, best_fitness_history):
        plt.plot(avg_fitness_history, label=f'Report {report_num} - Average Fitness')
        plt.plot(best_fitness_history, label=f'Report {report_num} - Best Fitness')

        plt.ylabel(f'{report_num} - Best Fitness: {best_fitness}')



    def parse_report_line(self, line):
        return line.split()[2:]

    def parse_float_list(self, line):
        items = line.split()[3:][:-1]
        cleaned_items = [item.replace(",", "").strip("[]") for item in items]
        cleaned_items = [item.replace("]", "") for item in cleaned_items]
        return [f"{float(item):.3f}" for item in cleaned_items]


    def plot_report(self):
        with open("src/report.txt", "r") as file:
            lines = file.readlines()

            report_num, population_size, num_generations, cross_validation = 0, 0, 0, False
            best_fitness, avg_fitness_history, best_fitness_history = 0.0, [], []

            for line in lines:
                if line.startswith("Report"):
                    report_num = str(line).strip()
                elif line.startswith("Population"):
                    population_size = int(line.split(" ")[2])
                elif line.startswith("Best chromossome"):
                    best_chromossome = line.split(" ")[2:-1]
                elif line.startswith("Best fitness") and not line.startswith("Best fitness history"):
                    best_fitness = float(line.split(" ")[2])
                elif line.startswith("Avarage"):
                    avg_fitness_history = self.parse_report_line(line)
                elif line.startswith("Best fitness history"):
                    best_fitness_history = self.parse_float_list(line)
                    self.plot_fitness_history(report_num, population_size, best_fitness, avg_fitness_history, best_fitness_history)

        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.legend()
        plt.show()
        

if __name__ == "__main__":
    utils = Utils()
    utils.plot_report()
