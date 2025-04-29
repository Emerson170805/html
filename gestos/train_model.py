import pandas as pd
import os
from sklearn.neighbors import KNeighborsClassifier
import joblib

folder = 'gestures'
dataframes = []

for file in os.listdir(folder):
    if file.endswith('.csv'):
        df = pd.read_csv(os.path.join(folder, file), header=None)
        dataframes.append(df)

df_all = pd.concat(dataframes)
X = df_all.iloc[:, :-1].values
y = df_all.iloc[:, -1].values

model = KNeighborsClassifier(n_neighbors=3)
model.fit(X, y)

os.makedirs('model', exist_ok=True)
joblib.dump(model, 'model/gesture_knn.pkl')
print("Modelo entrenado y guardado en 'model/gesture_knn.pkl'")
