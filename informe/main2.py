# ---------------------------------------------
# 2. Red Convolucional (CNN) para clasificación de imágenes
# ---------------------------------------------
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten

model_cnn = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D(),
    Flatten(),
    Dense(10, activation='softmax')
])
model_cnn.compile(optimizer='adam', loss='categorical_crossentropy')
print("CNN modelo compilado (sin entrenamiento real por falta de datos)")