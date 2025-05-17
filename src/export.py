import sys
import tensorflow as tf
from keras.api.models import load_model
from pathlib import Path

def export_to_tflite(model_filename):
    model_path = Path("models") / model_filename
    if not model_path.exists():
        print(f"Model file not found: {model_path}")
        return
    
    tflite_path = model_path.with_suffix(".tflite")

    model = load_model(model_path)
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    
    with open(tflite_path, "wb") as f:
        f.write(tflite_model)
    
    print(f"Model exported to TensorFlow Lite: {tflite_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python export.py <keras_model_filename>")
        sys.exit(1)

    filename = sys.argv[1]
    export_to_tflite(filename)
