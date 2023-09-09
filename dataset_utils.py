import numpy as np
import os


def process_header_file(filepath, filename):
    base_filename = os.path.splitext(filename)[0]  # Get the filename without extension

    with open(filepath, 'rw') as file:
        lines = file.readlines()

        # Modify the first 13 lines
        for i in range(min(13, len(lines))):
            lines[i] = base_filename + lines[i][7:]

        file.writelines(lines)


def rename_files(root_dir):
    n=0
    for root, _, files in os.walk(root_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            if filename.endswith('.hea'):
                new_name = os.path.join(root, f"patient_{n:05d}.hea")
                os.rename(file_path, new_name)

                process_header_file(file_path, filename)

            elif filename.endswith('.mat'):
                new_name = os.path.join(root, f"patient_{n:05d}.mat")
                os.rename(file_path, new_name)
                n+=1

