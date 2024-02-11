# ==============================================================================
# Main file init to run the genetic algorithm
# 
#
# Author: Guilherme Santos
# Last edited: 2024-02-11 
# ==============================================================================

import os
from src.__main__ import __init__

dirs = os.listdir()

if "src" not in dirs:
    Exception("The src folder is not in the current directory")

else:
    __init__()