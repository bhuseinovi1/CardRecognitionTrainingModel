from models.preparing_data_generators import prepare_data_generators
from models.mobilenet import create_model
from models.evaluate import evaluate_results
from visualization.plot_training_history import plot_training_history
from visualization.plot_finetuning_progress import plot_combined_history
from visualization.plot_learning_rate import plot_learning_rate
from keras._tf_keras.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras._tf_keras.keras.optimizers import Adam
from keras._tf_keras.keras.applications.mobilenet_v2 import MobileNetV2

def main():
    # Prepare data generators
    train_generator, validation_generator, test_generator = prepare_data_generators()

    # Calculate and print the number of classes
    num_classes = train_generator.num_classes
    print("Number of classes:", num_classes)

    # Load MobileNetV2 model
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    model = create_model(base_model, num_classes)
    model.summary()

    # Early stopping: Monitor validation loss
    early_stopping = EarlyStopping(
        monitor='val_loss',   # Metric to monitor
        patience=5,           # Stop after 5 epochs without improvement
        restore_best_weights=True  # Roll back to the best model weights
    )

    # Reduce learning rate on plateau
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',   # Metric to monitor
        factor=0.5,           # Reduce learning rate by half
        patience=3,           # Wait 3 epochs before reducing
        min_lr=1e-6           # Minimum learning rate
    )

    # Train the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    history = model.fit(train_generator, epochs=15, validation_data=validation_generator, callbacks=[early_stopping, reduce_lr])

    # # Fine-tuning: Unfreeze some layers of the base model
    # for layer in base_model.layers[-30:]:  # Unfreeze the last 30 layers
    #     layer.trainable = True

    # # Compile the model with a lower learning rate for fine-tuning
    # model.compile(optimizer=Adam(learning_rate=1e-4),loss='categorical_crossentropy',metrics=['accuracy'])

    # # Continue training with fine-tuning
    # history_fine = model.fit(train_generator, validation_data=validation_generator, epochs=20, callbacks=[early_stopping, reduce_lr])

    # Call the function with your history object
    plot_training_history(history)
    # plot_combined_history(history, history_fine)

    # Evaluate the model
    evaluate_results(model, test_generator)

    # Save the model
    model.save("./models/card_recognition_model.keras")
    print("Model trained and saved.")

if __name__ == '__main__':
    main()