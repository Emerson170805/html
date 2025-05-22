import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense

# Secuencia de números (entrada y siguiente valor)
x = np.array([2, 4, 6, 8, 10, 12])
y = x + 2  # lo que debe predecir el modelo

# Modelo
modelo = Sequential([
    Dense(1, input_shape=(1,))
])
modelo.compile(optimizer='adam', loss='mse')
modelo.fit(x, y, epochs=500, verbose=0)

# Probar con números nuevos
for n in [14, 20, 25, 30]:
    pred = modelo.predict(np.array([[n]]))[0][0]
    print(f"Siguiente de {n} → {pred:.2f}")
