import numpy as np
import matplotlib.pyplot as plt

# Function to plot learning rate changes
def plot_learning_rate(history):
    # Extract learning rate changes
    lr_schedule = history.history.get('lr', None)
    
    if lr_schedule is not None:
        epochs = np.arange(1, len(lr_schedule) + 1)
        plt.figure(figsize=(8, 4))
        plt.plot(epochs, lr_schedule, label='Learning Rate')
        plt.title('Learning Rate Schedule')
        plt.xlabel('Epochs')
        plt.ylabel('Learning Rate')
        plt.grid(True)
        plt.legend()
        plt.show()
    else:
        print("No learning rate changes recorded in history.")

