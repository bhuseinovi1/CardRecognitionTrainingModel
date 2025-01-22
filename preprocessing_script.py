import os
from preprocessing import resizing_images, renaming_images, separating_datasets

def create_datasets_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def preprocess_images(input_dir, datasets_dir, target_size, datasets_range):
    resizing_images.resize_images(input_dir, datasets_dir, target_size, datasets_range)
    renaming_images.rename_images(datasets_dir, datasets_range)
    separating_datasets.separate_datasets(datasets_dir, datasets_range)

def main():
    input_directory = 'D:\\TESTING'
    current_directory = os.path.dirname(os.path.abspath(__file__))
    datasets_directory = os.path.join(current_directory, 'datasets')
    datasets_range = range(1, 80)
    target_size = (224, 224)

    create_datasets_directory(datasets_directory)
    preprocess_images(input_directory, datasets_directory, target_size, datasets_range)

if __name__ == "__main__":
    main()