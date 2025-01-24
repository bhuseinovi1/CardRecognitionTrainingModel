from keras._tf_keras.keras.preprocessing.image import ImageDataGenerator

def prepare_data_generators(base_dir='./datasets',
                            image_size=(224, 224),
                            training_batch_size=32, 
                            validation_batch_size=16, 
                            testing_batch_size=16):

    # Define the paths to your dataset folders
    train_dir = f"{base_dir}/training"
    validation_dir = f"{base_dir}/validation"
    test_dir = f"{base_dir}/testing"

    # Create an ImageDataGenerator for training with data augmentation
    train_datagen = ImageDataGenerator(
        rescale=1.0/255,              # Normalize pixel values to [0, 1]
        rotation_range=20,            # Randomly rotate images by 20 degrees
        width_shift_range=0.2,        # Randomly shift images horizontally by 20%
        height_shift_range=0.2,       # Randomly shift images vertically by 20%
        shear_range=0.2,              # Shear transformations
        zoom_range=0.2,               # Zoom in/out by 20%
        horizontal_flip=True,         # Randomly flip images horizontally
        fill_mode='nearest'           # Fill pixels after transformations
    )

    # For validation and testing, only rescale pixel values
    validation_datagen = ImageDataGenerator(rescale=1.0/255)
    test_datagen = ImageDataGenerator(rescale=1.0/255)

    # Create generators for training, validation, and testing
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=image_size,
        batch_size=training_batch_size,
        class_mode='categorical',     # Assuming you have 79 classes (multiclass classification)
        shuffle=True                  # Shuffle training data
    )

    validation_generator = validation_datagen.flow_from_directory(
        validation_dir,
        target_size=image_size,
        batch_size=validation_batch_size,
        class_mode='categorical',
        shuffle=False                 # Do not shuffle validation data
    )

    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=image_size,
        batch_size=testing_batch_size,
        class_mode='categorical',
        shuffle=False                 # Do not shuffle test data
    )

    # Print the class indices to verify the class mappings
    print("Class indices:", train_generator.class_indices)

    return train_generator, validation_generator, test_generator
