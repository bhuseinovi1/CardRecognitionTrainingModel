import tensorflow as tf
from keras.api.models import load_model

MODEL_PATH = "./models/card_recognition_model.keras"
TFLITE_PATH = "./models/card_recognition_model.tflite"

def export_to_tflite():
    """
    Converts a trained Keras model to TensorFlow Lite format.
    """
    # model = tf.keras.models.load_model(MODEL_PATH)
    model = load_model(MODEL_PATH)
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    
    with open(TFLITE_PATH, "wb") as f:
        f.write(tflite_model)
    
    print(f"Model exported to TensorFlow Lite: {TFLITE_PATH}")

if __name__ == "__main__":
    export_to_tflite()
