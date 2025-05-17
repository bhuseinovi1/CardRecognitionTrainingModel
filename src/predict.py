
import sys
from models.preparing_data_generators import prepare_data_generators
import numpy as np
from keras._tf_keras.keras.preprocessing import image
from tensorflow.lite.python.interpreter import Interpreter
import os
import re
from pathlib import Path

def load_labels(class_indices):
    return {v: k for k, v in class_indices.items()}

def predict_tflite(model_path, image_path, class_labels, image_size=(224, 224)):
    img = image.load_img(image_path, target_size=image_size)
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0).astype(np.float32)

    interpreter = Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], img_array)

    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])

    for i, score in enumerate(output_data[0]):
        percentage = float(score) * 100
        if percentage > 0.01:
            print(f"Class {class_labels[i]}: {percentage:.2f}")

    predicted_index = np.argmax(output_data)
    confidence = float(np.max(output_data))
    predicated_label = class_labels[predicted_index]

    return predicated_label, confidence


def main(model_filename):
    model_path = Path("models") / model_filename
    if not model_path.exists():
        print(f"Model file not found: {model_path}")
        return
    
    train_generator, _, _ = prepare_data_generators()
    #folder_path = "./models/samples"
    folder_path = Path("models/samples")
    folder_path.mkdir(exist_ok=True)
    class_indices = train_generator.class_indices
    labels = load_labels(class_indices)
    print(labels)
    print(model_path)
    print(folder_path)
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            label, confidence = predict_tflite(
                #model_path = "./models/model.tflite",
                model_path = str(model_path),
                image_path = image_path,
                class_labels = labels
            )
            match = re.search(r'karta(\d+)\.jpg', filename)
            if match:
                n = int(match.group(1))
                result = "✔" if n == int(label) else "✘"
                print(f"{filename} → {label} ({confidence * 100:.2f}%) {result}\n")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python export.py <tflite_model_filename>")
        sys.exit(1)

    filename = sys.argv[1]
    main(filename)