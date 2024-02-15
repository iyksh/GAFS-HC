# ================================================================================================================================================
# Main file init to run the genetic algorithm, read the config.json file and change the variables there
# 
# .json file example:
# 
# { 
#     "train_path": "./CellCycle.arff", # The path of the train file (required)
#     "test_path": null,                # The path of the test file (optional), if null, the train file will be used to create the test file
#     "population_size": 16,            # The size of the population, recommended a number that is a multiple of the max_parallelism_subprocess
#     "num_generations": 300,           # The number of generations
#     "crossover_rate": 0.9,            # The rate of the crossover
#     "mutation_rate": 0.1,             # The rate of the mutation
#     "tournament_winner_rate": 0.75,   # The rate of the tournament winner
#     "timer_stop_algorithm": 0,        # The time to check if the user wants to stop the algorithm (Not used anymore, you can stop with ctrl+c)
#     "enable_parallelism": true,       # If the threading will be used or not
#     "max_parallelism_subprocess": 4   # The number of threads to be used
#
# }
#
#
#
#
# Author: Guilherme Santos
# Last edited: 2024-02-11 
# ========================================================================================================================================================

import os
import json
import shutil
from src.__main__ import __main__
from src.cfs_hierarchical import cfs_example_usage  # noqa
from src.call_nbayes import call_nbayes  # 

def remove_thread_folders():
    dirs = os.listdir()

    if "src" not in dirs or "generated-files" not in dirs:
        raise Exception("Some folder is not in the current directory")

    folders_path = "./generated-files"
    folders = [os.path.join(folders_path, folder) for folder in os.listdir(folders_path) if os.path.isdir(os.path.join(folders_path, folder))]
    for folder in folders:
        if folder.startswith("./generated-files/thread_") or folder.startswith("thread_"):
            try:
                shutil.rmtree(folder)
                
            except OSError as e:
                print(f"[+] Error removing folder: {e}")


if __name__ == "__main__":

    remove_thread_folders()

    #cfs_example_usage()  

    with open("./.json", "r") as FILE:
        config = json.load(FILE)    
        
        __main__(config)
