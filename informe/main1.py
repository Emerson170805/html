# ---------------------------------------------
# 1. Red neuronal Densa (Regresión simple)
# ---------------------------------------------
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
import numpy as np

x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 6, 8, 10])

model_dense = Sequential([
    Dense(1, input_shape=(1,))
])
model_dense.compile(optimizer='adam', loss='mse')
model_dense.fit(x, y, epochs=300, verbose=0)
print("Dense predicción para 6:", model_dense.predict(np.array([[6]]))[0][0])