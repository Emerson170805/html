import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense

# Secuencia de números (entrada y siguiente valor)
x = np.array([2, 4, 6, 8, 10, 12])
y = x + 2  # salida esperada: el siguiente número

# Modelo con 3 capas ocultas
modelo = Sequential([
    Dense(16, activation='relu', input_shape=(1,)),
    Dense(16, activation='relu'),
    Dense(8, activation='relu'),
    Dense(1)  # salida
])

modelo.compile(optimizer='adam', loss='mse')
modelo.fit(x, y, epochs=500, verbose=0)

# Probar con números nuevos
for n in [14, 20, 25, 30]:
    pred = modelo.predict(np.array([[n]]))[0][0]
    print(f"Siguiente de {n} → {pred:.2f}")
