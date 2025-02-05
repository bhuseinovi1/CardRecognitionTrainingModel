from pathlib import Path
from preprocessing import image_augmentation, datasets_separation

def main():
    input_directory = ''
    backgrounds_dir = ''
    project_root = Path(__file__).resolve().parent.parent
    datasets_directory = project_root / 'datasets'
    datasets_range = range(1, 80)

    # Create datasets directory if it does not exist and augment images
    if not datasets_directory.exists():
        datasets_directory.mkdir(parents=True, exist_ok=True)
        image_augmentation.augment_images(
            input_dir = input_directory,
            backgrounds_dir = backgrounds_dir,
            datasets_dir = datasets_directory,
            datasets_range = datasets_range,
            augmented_per_image = 20)
        datasets_separation.separate_datasets(
            datasets_dir = datasets_directory,
            datasets_range = datasets_range)
    else:
        print("Datasets directory already exists. Skipping image augmentation and datasets separation.")

if __name__ == "__main__":
    main()