# ---------------------------------------------
# 4. Red LSTM para memoria a largo plazo
# ---------------------------------------------
from tensorflow.keras.layers import LSTM

model_lstm = Sequential([
    LSTM(64, input_shape=(10, 1)),
    Dense(1)
])
model_lstm.compile(optimizer='adam', loss='mse')
x_lstm = np.random.rand(100, 10, 1)
y_lstm = np.random.rand(100, 1)
model_lstm.fit(x_lstm, y_lstm, epochs=5, verbose=0)
print("LSTM predicción para una muestra:", model_lstm.predict(x_lstm[:1])[0][0])