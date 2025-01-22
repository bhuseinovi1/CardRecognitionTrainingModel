from PIL import Image
import os

def resize_image(input_path, datasets_file_path, target_size):
    """
    Resize a single image while maintaining its aspect ratio and center it on a new canvas of the target size.

    Parameters:
        input_path (str): Path to the input image.
        output_path (str): Path to save the resized image.
        target_size (tuple): The target size as (width, height).
    """
    try:
        image = Image.open(input_path)
        image.thumbnail(target_size, Image.LANCZOS)  # Maintain aspect ratio
        new_image = Image.new("RGB", target_size)  # Create a new image with the target size
        new_image.paste(image, ((target_size[0] - image.width) // 2, (target_size[1] - image.height) // 2))  # Center the resized image
        new_image.save(datasets_file_path)
        print(f"Image {input_path} copied to {datasets_file_path}!")
    except Exception as e:
        print(f"Error resizing image {input_path}: {e}")


def resize_images(input_directory, datasets_directory, target_size, datasets_range):
    """
    Resize images in multiple subdirectories and save them in a corresponding output directory.

    Parameters:
        input_directory (str): Root directory containing folders of images to resize.
        datasets_directory (str): Root directory where resized images will be saved.
        target_size (tuple): The target size for the resized images as (width, height).
        folders_range (range): Range object defining folder names to process.
    """
    for folder_name in datasets_range:  # Process each folder in the specified range
        folder_path = os.path.join(input_directory, str(folder_name))
        datasets_folder_path = os.path.join(datasets_directory, str(folder_name))
        os.makedirs(datasets_folder_path, exist_ok=True)

        if not os.path.exists(folder_path):  # Skip if the input folder doesn't exist
            print(f"Folder does not exist: {folder_path}")
            continue

        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Case-insensitive extension check
                input_path = os.path.join(folder_path, filename)
                dataset_file_path = os.path.join(datasets_folder_path, filename)
                resize_image(input_path, dataset_file_path, target_size)

    print("Images resized and saved successfully!")
