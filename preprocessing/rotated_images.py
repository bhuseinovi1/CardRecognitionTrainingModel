import os
from PIL import Image

# Path to the root directory containing folders "1" to "79"
root_dir = "F:\\DIRECTORY"

def check_image_orientation():
    for folder_num in range(1, 80):
        folder_name = str(folder_num)
        folder_path = os.path.join(root_dir, folder_name)
        
        # Check if the folder exists
        if not os.path.exists(folder_path):
            print(f"Folder {folder_name} does not exist. Skipping...")
            continue
        
        # Get all files in the folder
        files = sorted(os.listdir(folder_path))
        
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            
            # Ensure it's a valid file
            if not os.path.isfile(file_path):
                continue
            
            # Open the image and check its dimensions
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    if width > height:
                        print(f"Wide image found: {file_path} (Width: {width}, Height: {height})")
            except Exception as e:
                print(f"Could not process file {file_path}. Error: {e}")

if __name__ == "__main__":
    check_image_orientation()