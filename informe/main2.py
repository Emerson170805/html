# ---------------------------------------------
# 2. Red Convolucional (CNN) para clasificación de imágenes
# ---------------------------------------------
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Definir el modelo CNN
model_cnn = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D(),
    Flatten(),
    Dense(10, activation='softmax')  # 10 clases de salida (como MNIST)
])

# Compilar el modelo
model_cnn.compile(optimizer='adam', loss='categorical_crossentropy')

# Mensaje de confirmación
print("✅ CNN modelo compilado correctamente (sin entrenamiento por falta de datos)")
