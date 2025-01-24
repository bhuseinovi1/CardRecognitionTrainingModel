from preparing_data_generators import prepare_data_generators
from mobilenet import create_model

def main():
    # Prepare data generators
    train_generator, validation_generator, test_generator = prepare_data_generators()

    # Calculate and print the number of classes
    num_classes = train_generator.num_classes
    print("Number of classes:", num_classes)

    # Load MobileNetV3Small model
    model = create_model(num_classes) # 79 classes
    model.summary()

    # Train the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    history = model.fit(train_generator, epochs=5, validation_data=validation_generator)

    # Evaluate the model
    loss, accuracy = model.evaluate(test_generator)    
    print(f"Test accuracy: {accuracy * 100:.2f}%")
    print(f"Test loss: {loss:.4f}")

if __name__ == '__main__':
    main()