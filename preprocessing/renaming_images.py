import os

def rename_images(datasets_directory, datasets_range):
    """
    Rename image files in specified folders within the output directory.

    Parameters:
        datasets_directory (str): Root directory containing subfolders of images.
        datasets_range (range): Range of folder numbers to process (e.g., range(1, 80)).
    """
    for folder_num in datasets_range:
        folder_name = str(folder_num)
        folder_path = os.path.join(datasets_directory, folder_name)
        
        # Check if the folder exists
        if not os.path.exists(folder_path):
            print(f"Folder {folder_name} does not exist. Skipping...")
            continue
        
        # Get all files in the folder and sort them
        files = sorted(os.listdir(folder_path))
        
        for index, file_name in enumerate(files, start=1):
            # Construct full file path
            file_path = os.path.join(folder_path, file_name)
            
            # Skip non-files (e.g., directories)
            if not os.path.isfile(file_path):
                print(f"Skipping non-file: {file_name}")
                continue
            
            # Generate new file name
            new_name = f"card_{folder_num:02d}_{index:02d}"
            file_extension = os.path.splitext(file_name)[1].lower()  # Preserve original extension and normalize case
            new_file_name = new_name + file_extension
            
            # Rename the file
            new_file_path = os.path.join(folder_path, new_file_name)
            try:
                os.rename(file_path, new_file_path)
                print(f"Renamed: {file_name} -> {new_file_name}")
            except Exception as e:
                print(f"Error renaming {file_name}: {e}")

    print("Image renaming completed!")
