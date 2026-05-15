import tensorflow as tf
import os

print("Building the crop disease model...")

# 1. Define a simple Convolutional Neural Network (CNN)
model = tf.keras.models.Sequential([
    # Input layer expects a 224x224 RGB image
    tf.keras.layers.InputLayer(input_shape=(224, 224, 3)),
    
    # A basic convolutional layer to extract features
    tf.keras.layers.Conv2D(16, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    
    # Flatten the results to feed into a dense layer
    tf.keras.layers.GlobalAveragePooling2D(),
    
    # Output layer with 4 nodes (for our 4 classes) using softmax for probabilities
    tf.keras.layers.Dense(4, activation='softmax')
])

# 2. Compile the model
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# 3. Save the model as an .h5 file
save_path = os.path.join(os.path.dirname(__file__), 'crop_disease_model.h5')
model.save(save_path)

print(f"Success! Model saved at: {save_path}")
print("You can now run your Flask app.")
