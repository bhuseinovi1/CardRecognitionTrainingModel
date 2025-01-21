import os
import random
import shutil

# Define the input and output directories
input_dir = 'F:\\DIRECTORY'
categories = ['training', 'validation', 'testing']

# Define the split ratios
train_ratio = 0.70
validation_ratio = 0.15
testing_ratio = 0.15

# Iterate over each folder
for folder_name in range(1, 80):  # Assuming folders are named 1, 2, ..., 79
    folder_path = os.path.join(input_dir, str(folder_name))
    all_files = os.listdir(folder_path)
    random.shuffle(all_files)
    
    # Calculate the number of files for each set
    total_files = len(all_files)
    train_count = int(total_files * train_ratio)
    validation_count = int(total_files * validation_ratio)
    testing_count = total_files - train_count - validation_count

    # Creating output directories
    for category in categories:
        category_folder_path = os.path.join(folder_path, category)
        os.makedirs(category_folder_path, exist_ok=True)
        print(f"Folder {category_folder_path} created")

    # Split the files into training, validation, and testing sets
    train_files = all_files[:train_count]
    validation_files = all_files[train_count:train_count + validation_count]
    testing_files = all_files[train_count + validation_count:]

    # Move the files to the corresponding output directories
    for file in train_files:
        file_from_path = os.path.join(folder_path, file)
        file_to_path = os.path.join(folder_path, 'training', file)
        shutil.move(file_from_path, file_to_path)
        print(f"File {file_from_path} deleted")
        print(f"File {file_to_path} created")
    
    for file in validation_files:
        file_from_path = os.path.join(folder_path, file)
        file_to_path = os.path.join(folder_path, 'validation', file)
        shutil.move(file_from_path, file_to_path)
        print(f"File {file_from_path} deleted")
        print(f"File {file_to_path} created")
    
    for file in testing_files:
        file_from_path = os.path.join(folder_path, file)
        file_to_path = os.path.join(folder_path, 'testing', file)
        shutil.move(file_from_path, file_to_path)
        print(f"File {file_from_path} deleted")
        print(f"File {file_to_path} created")

print("Files have been successfully moved!")
