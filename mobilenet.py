# from keras._tf_keras.keras.applications.mobilenet_v3 import MobileNetV3Small
from keras._tf_keras.keras.applications.mobilenet_v2 import MobileNetV2
from keras import layers, models

def create_model(num_classes):
    # Load MobileNetV3Small model
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    base_model.trainable = False # Freeze the base model

    # Custom classification head
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.1),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model