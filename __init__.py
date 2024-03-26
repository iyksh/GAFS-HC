# ================================================================================================================================================
# Main file init to run the genetic algorithm, read the config.json file and change the variables there to run the algorithm
#
# Author: Guilherme Santos
# Last edited: 2024-02-11 
# ========================================================================================================================================================

import yaml


from src.__main__ import __main__

if __name__ == "__main__":

    with open("./config.yaml", "r") as FILE:
        config = yaml.safe_load(FILE)
        
        __main__(config)
