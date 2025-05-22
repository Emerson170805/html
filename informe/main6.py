# ---------------------------------------------
# 6. Autoencoder para compresión y reconstrucción
# ---------------------------------------------
from tensorflow.keras import Model, Input

input_ae = Input(shape=(100,))
encoded = Dense(32, activation='relu')(input_ae)
decoded = Dense(100, activation='sigmoid')(encoded)
model_autoencoder = Model(input_ae, decoded)
model_autoencoder.compile(optimizer='adam', loss='mse')
x_ae = np.random.rand(100, 100)
model_autoencoder.fit(x_ae, x_ae, epochs=5, verbose=0)
print("Autoencoder reconstrucción ejemplo:", model_autoencoder.predict(x_ae[:1])[0][:5])