from keras._tf_keras.keras.applications.mobilenet_v2 import MobileNetV2
import numpy as np

def evaluate_results(model, test_generator):
    loss, accuracy = model.evaluate(test_generator)    
    print(f"Test accuracy: {accuracy * 100:.2f}%")
    print(f"Test loss: {loss:.4f}")

    predictions = model.predict(test_generator)
    predicted_classes = np.argmax(predictions, axis=1)

    actual_classes = test_generator.classes

    class_labels = list(test_generator.class_indices.keys())

    # Get the filenames
    filenames = test_generator.filenames

    # Initialize counters for correct predictions and total predictions for each class
    correct_predictions = {label: 0 for label in class_labels}
    total_predictions = {label: 0 for label in class_labels}

    # Update counters
    for predicted, actual in zip(predicted_classes, actual_classes):
        actual_label = class_labels[actual]
        total_predictions[actual_label] += 1
        if predicted == actual:
            correct_predictions[actual_label] += 1

    # Calculate and print the percentage of correct predictions for each class
    for label in class_labels:
        if total_predictions[label] > 0:
            accuracy = (correct_predictions[label] / total_predictions[label]) * 100
            print(f"Class: {label}, Accuracy: {accuracy:.2f}% ({correct_predictions[label]}/{total_predictions[label]})")
        else:
            print(f"Class: {label}, No samples in test set")

    # Print the results
    for i, (filename, predicted, actual) in enumerate(zip(filenames, predicted_classes, actual_classes)):
        print(f"Filename: {filename}, Predicted class = {class_labels[predicted]}, Actual class = {class_labels[actual]}")