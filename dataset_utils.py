"""
"""

# Standard Library
import os


def process_header_file(filepath, filename):
    base_filename = os.path.splitext(filename)[0]  # Get the filename without extension

    with open(filepath, 'r') as file:
        lines = file.readlines()

    # Modify the first 13 lines
    for i in range(min(13, len(lines))):
        lines[i] = base_filename + lines[i][7:]

    with open(filepath, 'w') as file:
        file.writelines(lines)


def rename_files(root_dir):
    n=0
    for root, _, files in os.walk(root_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            if filename.endswith('.hea'):
                if n in [999, 22674]:
                    os.remove(file_path)
                    continue
                new_header = f"patient_{n:05d}.hea"
                new_header_path = os.path.join(root, new_header)
                os.rename(file_path, new_header_path)

                process_header_file(new_header_path, new_header)

            elif filename.endswith('.mat'):
                if n in [999, 22674]:
                    os.remove(file_path)
                    n += 1
                    continue
                new_mat_path = os.path.join(root, f"patient_{n:05d}.mat")
                os.rename(file_path, new_mat_path)
                n+=1
