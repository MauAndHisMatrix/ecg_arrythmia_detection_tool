import numpy as np
import os

def name_changer(root_dir):
    n = 0
    for root, _, files in os.walk("test_records"):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    if filename.endswith('.hea'):
                        new_name = os.path.join(root, f"patient_{n:05d}.hea")
                        os.rename(file_path, new_name)
                    elif filename.endswith('.mat'):
                        new_name = os.path.join(root, f"patient_{n:05d}.mat")
                        os.rename(file_path, new_name)
                        n+=1