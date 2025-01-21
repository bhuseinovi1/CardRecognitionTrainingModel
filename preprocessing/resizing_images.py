from PIL import Image
import os

def resize_image(input_path, target_size):
    image = Image.open(input_path)
    image.thumbnail(target_size, Image.LANCZOS)  # Maintain aspect ratio
    new_image = Image.new("RGB", target_size)  # Create a new image with the target size
    new_image.paste(image, ((target_size[0] - image.width) // 2, (target_size[1] - image.height) // 2))  # Center the resized image
    new_image.save(input_path)

input_directory = 'DIRECTORY'
output_directory = 'DIRECTORY'
target_size = (224, 224)  # Adjust as needed



for filename in os.listdir(input_directory):
    if filename.endswith('.jpg') or filename.endswith('.png'):  # Add other extensions if needed
        input_path = os.path.join(input_directory, filename)
        resize_image(input_path, target_size)

print("Images resized and saved successfully!")
