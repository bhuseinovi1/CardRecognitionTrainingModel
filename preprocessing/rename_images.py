import os

# Path to the root directory containing folders "1" to "79"
root_dir = "F:\\DIRECTORY"

def rename_images():
    # Loop through folder numbers from 1 to 79
    for folder_num in range(1, 80):
        folder_name = str(folder_num)
        folder_path = os.path.join(root_dir, folder_name)
        
        # Check if the folder exists
        if not os.path.exists(folder_path):
            print(f"Folder {folder_name} does not exist. Skipping...")
            continue
        
        # Get all files in the folder
        files = sorted(os.listdir(folder_path))
        
        # Rename each image in the folder
        for index, file_name in enumerate(files, start=1):
            # Ensure we're working with a file
            file_path = os.path.join(folder_path, file_name)
            if not os.path.isfile(file_path):
                print(f"Skipping non-file: {file_name}")
                continue
            
            # Create the new name
            new_name = f"card_{folder_num:02d}_{index:02d}"
            file_extension = os.path.splitext(file_name)[1]  # Preserve original extension
            new_file_name = new_name + file_extension
            
            # Rename the file
            new_file_path = os.path.join(folder_path, new_file_name)
            os.rename(file_path, new_file_path)
            print(f"Renamed: {file_name} -> {new_file_name}")

if __name__ == "__main__":
    rename_images()