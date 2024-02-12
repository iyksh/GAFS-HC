# ==============================================================================
# Main file init to run the genetic algorithm
# 
#
# Author: Guilherme Santos
# Last edited: 2024-02-11 
# ==============================================================================

import os
import json
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


if __name__ == "__main__":

    remove_thread_folders()

    with open("./.json", "r") as FILE:
        config = json.load(FILE)    
        
        __main__(config)