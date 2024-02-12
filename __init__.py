# ==============================================================================
# Main file init to run the genetic algorithm
# 
#
# Author: Guilherme Santos
# Last edited: 2024-02-11 
# ==============================================================================

import os
import json

from src.__main__ import __main__

dirs = os.listdir()

if "src" not in dirs:
    Exception("The src folder is not in the current directory")

else:
    with open("./.json", "r") as FILE:
        config = json.load(FILE)    

    __main__(config)