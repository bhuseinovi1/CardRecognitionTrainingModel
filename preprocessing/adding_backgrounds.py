from PIL import Image, ImageEnhance, ImageFilter
import os
import random

# Define paths
base_dir = 'F:\\MARVEL_REMIX_CROPPED_2'
backgrounds_dir = 'F:\\Card Recognition Training Model\\backgrounds\\Background 3\\data'
output_base_dir = 'F:\\MARVEL_REMIX_CROPPED_2\\backgrounds'

# Create the output base directory if it doesn't exist
os.makedirs(output_base_dir, exist_ok=True)

# Get a list of all image files in the backgrounds directory
all_background_images = [os.path.join(backgrounds_dir, f) for f in os.listdir(backgrounds_dir) if f.endswith(('jpg', 'png', 'PNG', 'JPG'))]

# Transformation functions
def random_rotation(image):
    return image.rotate(random.uniform(0, 360), expand=True)

def random_brightness(image):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(random.uniform(0.5, 1.5))

def random_contrast(image):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(random.uniform(0.5, 1.5))

def random_saturation(image):
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(random.uniform(0.5, 1.5))

def random_blur(image):
    return image.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.0, 2.0)))

def random_resize(image):
    width, height = image.size
    new_width = random.randint(int(width * 0.8), int(width * 1.2))
    new_height = random.randint(int(height * 0.8), int(height * 1.2))
    return image.resize((new_width, new_height), Image.LANCZOS)

def resize_background_to_fit(card_image, background_image):
    card_width, card_height = card_image.size
    background_image = background_image.resize((card_width, card_height), Image.LANCZOS)
    return background_image

def resize_to_target(image, target_size):
    return image.resize(target_size, Image.LANCZOS)

def add_to_background(card_image, background_image):
    card_width, card_height = card_image.size
    
    # Ensure background image has an alpha channel
    if background_image.mode != 'RGBA':
        background_image = background_image.convert('RGBA')
    
    # Resize the background to the size of the card image
    background_image = resize_background_to_fit(card_image, background_image)

    # Create a combined image
    combined_image = Image.alpha_composite(background_image, card_image)
    return combined_image

# Generate new images
target_size = (224, 224)
for folder_num in range(1, 31):  # Iterate through folders named 1 to 30
    
    # Load the selected images
    selected_background_images = random.sample(all_background_images, 3000)
    background_images = [Image.open(img_path) for img_path in selected_background_images]   
    
    card_folder_path = os.path.join(base_dir, str(folder_num))
    output_folder_path = os.path.join(output_base_dir, str(folder_num))
    os.makedirs(output_folder_path, exist_ok=True)
    
    counter = 1
    for card_filename in os.listdir(card_folder_path):
        if card_filename.endswith(('jpg', 'png', 'PNG', 'JPG')):
            card_image_path = os.path.join(card_folder_path, card_filename)
            card_image = Image.open(card_image_path).convert('RGBA')
            
            for i in range(20):  # Generate 10 new images per card
                background_image = random.choice(background_images).copy()

                # Apply transformations
                card_image_transformed = random_rotation(card_image)
                card_image_transformed = random_brightness(card_image_transformed)
                card_image_transformed = random_contrast(card_image_transformed)
                card_image_transformed = random_saturation(card_image_transformed)
                card_image_transformed = random_blur(card_image_transformed)
                card_image_transformed = random_resize(card_image_transformed)
                
                # Ensure card image has an alpha channel for transparency
                if card_image_transformed.mode != 'RGBA':
                    card_image_transformed = card_image_transformed.convert('RGBA')
                
                # Add card to background
                new_image = add_to_background(card_image_transformed, background_image)

                # Resize final image to 224x224
                new_image_resized = resize_to_target(new_image, target_size)

                # Save new image
                new_image_resized.save(os.path.join(output_folder_path, f'card_{counter}.png'))
                counter += 1

print("New images created and saved successfully!")