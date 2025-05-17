# Card Recognition Model

## Overview

The **Card Recognition Model** is a TensorFlow-based machine learning model aimed at recognizing cards in an Android application. The model is trained on a dataset of 79 cards, each labeled with a unique class identifier ("1", "2", ..., "79"). The final model is exported as a TensorFlow Lite file, optimized for use on Android devices.

The project is built in Python, using TensorFlow for model training, and the final model is exported in TensorFlow Lite format to be used in an Android app.

## Table of Contents

- [Requirements](#requirements)
- [Installation & Setup](#installation--setup)
- [Running the Project](#running-the-project)

## Requirements

The following dependencies are required to run the project:

- **Python 3.11**
- **TensorFlow**
- **PIL (Python Imaging Library)**
- **NumPy**
- **Matplotlib**

You can install these dependencies using the `requirements.txt` file included in the repository.

## Installation & Setup

1. **Clone the Repository**

   Clone this repository to your local machine:

   ```bash
   git clone https://github.com/bhuseinovi1/CardRecognitionTrainingModel.git
   cd CardRecognitionTrainingModel
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   It is recommended to create a virtual environment to avoid conflicts with other Python projects:

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Mac/Linux
   venv\Scripts\activate     # For Windows
   ```

3. **Install Dependencies**

   Install the required dependencies listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

Once the dependencies are installed, you can run the following scripts to process the images, train the model, and export it:

### 1. **Preprocessing**

The `preprocess.py` script loads images, applies data augmentation, and splits the dataset into training, validation and test sets. Run the script first:

    python preprocess.py

### 2. **Training the Model**

Once the preprocessing is complete, use the `train.py` script to train the model. This script will:

- Use the MobileNetV2 architecture as the base model.
- Fine-tune the model on the card dataset.
- Plot training metrics (such as accuracy and loss).
- Save the trained model.

Run the following command to start training:

    python train.py

### 3. **Exporting the model**

After training, you can export the model to TensorFlow Lite format using the `export.py` script. This step will convert the trained model to a `.tflite` file, which is optimized for mobile devices like Android.

Run the following command to export the model:

    python export.py <keras_model_filename>

This Python script excepts one argument representing Keras model name. Name should be provided since many models can exist in a project at the same time (every time train.py script is started, a new model is created). You can find all created models in `models` folder inside the project. The exported `.tflite` model can then be integrated into Android application.

### 4. **Testing the model**

If you want to test how model works, you can do it with your own card photos! All you need to do is place the photo inside the `samples` folder and run the following command:

    python predict.py <tflite_model_filename>

This Python script excepts one argument representing TFLite model name. After the script is run, you will be able to see predictions for all the cards you added.

> ⚠️ **Important:** For optimal model accuracy, it is essential that all card images are taken under normal and consistent lighting conditions. Please avoid harsh shadows, glare, overly dark environments, or colored lighting. Cards should be clearly visible, not blurry, and fully within the frame.
> Inconsistent lighting or poor image quality can significantly affect the model's ability to correctly recognize cards, leading to inaccurate predictions. We strongly recommend testing in typical indoor lighting to ensure the best results..
