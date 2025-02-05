from PIL import Image, ImageEnhance, ImageFilter
import os
import random

def augment_images(input_dir, backgrounds_dir, datasets_dir, datasets_range, augmented_per_image, target_size=(224, 224)): 
    """
    Augments images by applying transformations and blending them with backgrounds.

    Parameters:
        input_dir (str): Directory containing input card images.
        backgrounds_dir (str): Directory containing background images.
        datasets_dir (str): Directory to store augmented datasets.
        datasets_range (range): Range of dataset folders to process.
        augmented_per_image (int): Number of augmented images to generate per input image.
        target_size (tuple): Final size of the augmented images.
    """

    # Ensure the output dataset directory exists
    os.makedirs(datasets_dir, exist_ok=True)

    # Load all background images
    background_images = [
        os.path.join(backgrounds_dir, f) 
        for f in os.listdir(backgrounds_dir) 
        if f.lower().endswith(('jpg', 'png'))
    ]

    if not background_images:
        print("No background images found. Exiting.")
        return
    
    print(f"Loaded {len(background_images)} background images.")

    # Define transformation functions
    def random_rotation(image):
        return image.rotate(random.uniform(0, 360), expand=True)

    def random_brightness(image):
        return ImageEnhance.Brightness(image).enhance(random.uniform(0.5, 1.5))

    def random_contrast(image):
        return ImageEnhance.Contrast(image).enhance(random.uniform(0.5, 1.5))

    def random_saturation(image):
        return ImageEnhance.Color(image).enhance(random.uniform(0.5, 1.5))

    def random_blur(image):
        return image.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.0, 2.0)))

    def random_resize(image):
        width, height = image.size
        new_size = (
            random.randint(int(width * 0.8), int(width * 1.2)), 
            random.randint(int(height * 0.8), int(height * 1.2))
        )
        return image.resize(new_size, Image.LANCZOS)

    def resize_background(background, target_size):
        return background.resize(target_size, Image.LANCZOS)

    def blend_card_with_background(card, background):
        if background.mode != 'RGBA':
            background = background.convert('RGBA')
        background = resize_background(background, card.size)
        return Image.alpha_composite(background, card)

    # Process each dataset folder
    for folder_num in datasets_range:
        folder_path = os.path.join(input_dir, str(folder_num))
        output_folder_path = os.path.join(datasets_dir, str(folder_num))

        if not os.path.exists(folder_path):
            print(f"Skipping {folder_path}, folder does not exist.")
            continue

        os.makedirs(output_folder_path, exist_ok=True)

        card_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('jpg', 'png'))]
        
        if not card_files:
            print(f"No card images found in {folder_path}. Skipping.")
            continue
        
        print(f"Processing folder {folder_num}: {len(card_files)} card images found.")

        augmented_count = 0
        for card_file in card_files:
            card_path = os.path.join(folder_path, card_file)
            card_image = Image.open(card_path).convert('RGBA')

            for _ in range(augmented_per_image):
                background = Image.open(random.choice(background_images)).copy()

                # Apply transformations
                transformed_card = random_rotation(card_image)
                transformed_card = random_resize(transformed_card)
                blended_image = blend_card_with_background(transformed_card, background)

                # Apply post-blend effects
                final_image = random_brightness(blended_image)
                final_image = random_contrast(final_image)
                final_image = random_saturation(final_image)
                final_image = random_blur(final_image)

                # Resize to final target size
                final_image_resized = final_image.resize(target_size, Image.LANCZOS)

                # Save the augmented image
                output_filename = f'card_{folder_num:02d}_{(augmented_count+1):03d}.png'
                final_image_resized.save(os.path.join(output_folder_path, output_filename))
                augmented_count += 1

        print(f"Folder {folder_num}: Generated {augmented_count} augmented images.")

    print("Image augmentation completed successfully!")
