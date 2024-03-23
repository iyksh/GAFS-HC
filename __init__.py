# ================================================================================================================================================
# Main file init to run the genetic algorithm, read the config.json file and change the variables there to run the algorithm
#
# Author: Guilherme Santos
# Last edited: 2024-02-11 
# ========================================================================================================================================================

import os
import yaml
import shutil

from src.__main__ import __main__

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
    
    for files in os.listdir(folders_path):
        if files.endswith(".arff"):
            try:
                os.remove(os.path.join(folders_path, files))
                
            except OSError as e:
                print(f"[+] Error removing file: {e}")


if __name__ == "__main__":

    remove_thread_folders()

    with open("./config.yaml", "r") as FILE:
        config = yaml.safe_load(FILE)
        
        __main__(config)
