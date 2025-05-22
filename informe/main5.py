# ---------------------------------------------
# 5. Red GRU para procesamiento eficiente de secuencias
# ---------------------------------------------
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense

# Definición del modelo
model_gru = Sequential([
    GRU(64, input_shape=(10, 1)),
    Dense(1)
])

# Compilación del modelo
model_gru.compile(optimizer='adam', loss='mse')

# Datos aleatorios de entrenamiento
x_gru = np.random.rand(100, 10, 1)
y_gru = np.random.rand(100, 1)

# Entrenamiento
model_gru.fit(x_gru, y_gru, epochs=5, verbose=0)

# Predicción
print("GRU predicción para una muestra:", model_gru.predict(x_gru[:1])[0][0])
