# ---------------------------------------------
# 6. Autoencoder para compresión y reconstrucción
# ---------------------------------------------
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense

# Definición del modelo
input_ae = Input(shape=(100,))
encoded = Dense(32, activation='relu')(input_ae)
decoded = Dense(100, activation='sigmoid')(encoded)
model_autoencoder = Model(inputs=input_ae, outputs=decoded)

# Compilación
model_autoencoder.compile(optimizer='adam', loss='mse')

# Datos aleatorios de entrada
x_ae = np.random.rand(100, 100)

# Entrenamiento del autoencoder
model_autoencoder.fit(x_ae, x_ae, epochs=5, verbose=0)

# Reconstrucción de un ejemplo
reconstruido = model_autoencoder.predict(x_ae[:1])[0][:5]
print("Autoencoder reconstrucción ejemplo (primeros 5 valores):", reconstruido)
