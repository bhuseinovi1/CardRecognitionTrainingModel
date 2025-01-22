import os
import random
import shutil

def separate_datasets(datasets_directory, datasets_range, train_ratio=0.70, validation_ratio=0.15, testing_ratio=0.15):
    """
    Separate files into training, validation, and testing datasets.

    Parameters:
        datasets_directory (str): Root directory containing subfolders of datasets.
        datasets_range (range): Range of folder numbers to process (e.g., range(1, 80)).
        train_ratio (float): Proportion of files to allocate to the training set.
        validation_ratio (float): Proportion of files to allocate to the validation set.
        testing_ratio (float): Proportion of files to allocate to the testing set.
    """
    # Validate that the ratios add up to 1.0
    if not (0 <= train_ratio <= 1 and 0 <= validation_ratio <= 1 and 0 <= testing_ratio <= 1):
        raise ValueError("Ratios must be between 0 and 1.")
    if abs(train_ratio + validation_ratio + testing_ratio - 1.0) > 1e-6:
        raise ValueError("Ratios must add up to 1.0.")
    
    categories = ['training', 'validation', 'testing']

    # Create subdirectories for the datasets
    for category in categories:
        category_folder_path = os.path.join(datasets_directory, category)
        os.makedirs(category_folder_path, exist_ok=True)
        print(f"Created folder: {category_folder_path}")

    for folder_num in datasets_range:
        folder_name = str(folder_num)
        folder_path = os.path.join(datasets_directory, folder_name)

        # Check if the folder exists
        if not os.path.exists(folder_path):
            print(f"Folder {folder_name} does not exist. Skipping...")
            continue

        # Get all files in the folder and shuffle them for random distribution
        all_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not all_files:
            print(f"No files found in folder {folder_name}. Skipping...")
            continue
        random.shuffle(all_files)

        # Calculate the number of files for each dataset
        total_files = len(all_files)
        train_count = int(total_files * train_ratio)
        validation_count = int(total_files * validation_ratio)
        testing_count = total_files - train_count - validation_count

        # Split files into datasets
        train_files = all_files[:train_count]
        validation_files = all_files[train_count:train_count + validation_count]
        testing_files = all_files[train_count + validation_count:]

        # Helper function to move files
        def move_files(file_list, destination_category):
            for file_name in file_list:
                source_path = os.path.join(folder_path, file_name)
                destination_path = os.path.join(datasets_directory, destination_category, folder_name)
                os.makedirs(destination_path, exist_ok=True)
                destination_path = os.path.join(destination_path, file_name)
                try:
                    shutil.move(source_path, destination_path)
                    print(f"Moved: {file_name} -> {destination_category}")
                except Exception as e:
                    print(f"Error moving {file_name}: {e}")

        # Move files to their respective directories
        move_files(train_files, 'training')
        move_files(validation_files, 'validation')
        move_files(testing_files, 'testing')
        try: 
            os.rmdir(folder_path)
            print(f"Deleted folder: {folder_path}")
        except Exception as e:
            print(f"Error deleting folder {folder_path}: {e}")

    print("Dataset separation completed successfully!")
