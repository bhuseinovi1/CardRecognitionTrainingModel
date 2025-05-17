from pathlib import Path
from preprocessing import image_augmentation, datasets_separation
import gdown
import zipfile
import json

def download_and_extract_zip(file_id: str, extract_to: Path, marker_filename: str):
    marker_path = extract_to / marker_filename
    if marker_path.exists():
        print(f"{marker_filename} already exists. Skipping download.")
        return

    print(f"Downloading from Google Drive: {file_id}")
    zip_path = extract_to / "temp.zip"
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, str(zip_path), quiet=False)

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    except zipfile.BadZipFile:
        print(f"{zip_path} is not a valid zip.")
        
    zip_path.unlink()

    marker_path.touch()


def find_project_root(marker_files=('pyproject.toml', '.git', 'requirements.txt')):
    current = Path(__file__).resolve()
    for parent in current.parents:
        if any((parent / marker).exists() for marker in marker_files):
            return parent
    raise FileNotFoundError("Project root not found.")


def main():
    project_root = find_project_root()

    input_directory = project_root / 'temp_input'
    backgrounds_dir = project_root / 'temp_backgrounds'
    datasets_directory = project_root / 'datasets'
    config_path = project_root / 'config.json'
    datasets_range = range(1, 80)
    
    # Create necessary directories for card and background photos
    input_directory.mkdir(exist_ok=True)
    backgrounds_dir.mkdir(exist_ok=True)
    
    # Download and load data into dictionaries
    with open(config_path, "r") as f:
        config = json.load(f)

    download_and_extract_zip(config["drive_input_folder_id"], 
                             input_directory, 'cards_ready.marker')
    download_and_extract_zip(config["drive_backgrounds_folder_id"], 
                             backgrounds_dir, 'backgrounds_ready.marker')
    
    # Create datasets directory if it does not exist and augment images
    if not datasets_directory.exists():
        datasets_directory.mkdir(exist_ok=True)

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