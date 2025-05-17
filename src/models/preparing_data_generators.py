from keras._tf_keras.keras.preprocessing.image import ImageDataGenerator

def prepare_data_generators(base_dir='../datasets',
                            image_size=(224, 224),
                            training_batch_size=32, 
                            validation_batch_size=16, 
                            testing_batch_size=16):

    # Define the paths to your dataset folders
    train_dir = f"{base_dir}/training"
    validation_dir = f"{base_dir}/validation"
    test_dir = f"{base_dir}/testing"

    # Create an ImageDataGenerator for training without data augmentation
    # Data augmentation has already been applied to the dataset
    train_datagen = ImageDataGenerator(
        rescale=1.0/255,              # Normalize pixel values to [0, 1]
    )

    # For validation and testing, only rescale pixel values
    validation_datagen = ImageDataGenerator(rescale=1.0/255)
    test_datagen = ImageDataGenerator(rescale=1.0/255)

    # Create generators for training, validation, and testing
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=image_size,
        batch_size=training_batch_size,
        class_mode='categorical',     # Multiclass classification
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

    return train_generator, validation_generator, test_generator
