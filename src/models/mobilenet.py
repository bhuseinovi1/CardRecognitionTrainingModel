from keras import layers, models

def create_model(base_model, num_classes):

    base_model.trainable = False # Freeze the base model

    # Custom classification head
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model