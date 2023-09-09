import os

def process_file(filepath, filename):
    base_filename = os.path.splitext(filename)[0]  # Get the filename without extension

    with open(filepath, 'r') as file:
        lines = file.readlines()

    # Modify the first 13 lines
    for i in range(min(13, len(lines))):
        lines[i] = base_filename + lines[i][7:]

    with open(filepath, 'w') as file:
        file.writelines(lines)


for root, _, files in os.walk("WFDBRecords"):
            for filename in files:
                file_path = os.path.join(root, filename)
                if filename.endswith('.hea'):
                     print(filename)
                     process_file(file_path, filename)
                     
                     