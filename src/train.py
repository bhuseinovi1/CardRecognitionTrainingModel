from models.preparing_data_generators import prepare_data_generators
from models.mobilenet import create_model
from models.evaluate import evaluate_results
from visualization.plot_finetuning_progress import plot_combined_history
from keras._tf_keras.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from keras._tf_keras.keras.optimizers import Adam
from keras._tf_keras.keras.applications.mobilenet_v2 import MobileNetV2
import datetime

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

    # Add a checkpoint for best validation loss
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    checkpoint = ModelCheckpoint(
        f"./models/best_model_{timestamp}.keras",
        monitor="val_loss",
        save_best_only=True,
        verbose=1
    )

    # Train the model
    model.compile(
        optimizer='adam', 
        loss='categorical_crossentropy', 
        metrics=['accuracy'])
    
    history = model.fit(
        train_generator, 
        epochs=10, 
        validation_data=validation_generator, 
        callbacks=[early_stopping, reduce_lr, checkpoint])

    # Fine-tuning: Unfreeze some layers of the base model
    for layer in base_model.layers[:-30]:
        layer.trainable = False
    for layer in base_model.layers[-30:]:  # Unfreeze the last 30 layers
        layer.trainable = True

    # Compile the model with a lower learning rate for fine-tuning
    model.compile(
        optimizer=Adam(learning_rate=1e-4),
        loss='categorical_crossentropy',
        metrics=['accuracy'])

    # Continue training with fine-tuning
    history_fine = model.fit(
        train_generator, 
        validation_data=validation_generator, 
        epochs=10, 
        callbacks=[early_stopping, reduce_lr, checkpoint])

    # Call the function with your history object
    plot_combined_history(history, history_fine)

    # Evaluate the model
    print("\nEvaluating on test set:")
    evaluate_results(model, test_generator)

    # Save the model
    model.save(f"./models/card_recognition_model_{timestamp}.keras")
    print(f"\nFinal model trained and saved as card_recognition_model_{timestamp}.keras")
    print(f"\nBest model trained and saved as best_card_recognition_model_{timestamp}.keras")

if __name__ == '__main__':
    main()