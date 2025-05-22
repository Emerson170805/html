# ---------------------------------------------
# 4. Red LSTM para memoria a largo plazo
# ---------------------------------------------
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Definición del modelo LSTM
model_lstm = Sequential([
    LSTM(64, input_shape=(10, 1)),
    Dense(1)
])

# Compilación del modelo
model_lstm.compile(optimizer='adam', loss='mse')

# Datos aleatorios de entrenamiento (100 muestras, secuencias de 10 valores)
x_lstm = np.random.rand(100, 10, 1)
y_lstm = np.random.rand(100, 1)

# Entrenamiento
model_lstm.fit(x_lstm, y_lstm, epochs=5, verbose=0)

# Predicción con una muestra de entrada
prediccion = model_lstm.predict(x_lstm[:1])[0][0]
print("LSTM predicción para una muestra:", prediccion)
