# from keras._tf_keras.keras.applications.mobilenet_v3 import MobileNetV3
from keras._tf_keras.keras.applications.mobilenet_v2 import MobileNetV2
from keras import layers, models

def create_model(num_classes):
    # Load MobileNetV3Small model
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    base_model.trainable = False # Freeze the base model

    # Custom classification head
    model = models.Sequential([
        base_model,
        # layers.Conv2D(32, (3,3), activation='relu'),
        # layers.MaxPooling2D((2,2)),
        # layers.BatchNormalization(),
        layers.GlobalAveragePooling2D(),
        layers.Flatten(),
        layers.Dense(4096, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model