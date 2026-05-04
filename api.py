from flask import Flask, request, jsonify
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np

app = Flask(__name__)

# 🔥 DATOS DE ENTRENAMIENTO (puedes mejorarlos luego con datos reales)
# [promedio, asistencia, tareas%, promedio_tareas]
X_train = np.array([
    [30, 40, 20, 35],
    [45, 50, 40, 50],
    [55, 60, 60, 55],
    [65, 70, 70, 65],
    [75, 80, 80, 75],
    [85, 90, 90, 85],
])

y_train = np.array([
    "ALTO",
    "ALTO",
    "MEDIO",
    "MEDIO",
    "BAJO",
    "BAJO"
])

# 🔥 NORMALIZACIÓN (CLAVE PARA KNN)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X_train_scaled, y_train)


@app.route('/')
def home():
    return "API KNN MULTIVARIABLE ACTIVA"


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    resultados = []

    for e in data:
        features = e.get('features', [0, 0, 0, 0])

        # 🔥 ESCALAR igual que entrenamiento
        features_scaled = scaler.transform([features])

        pred = modelo.predict(features_scaled)[0]

        resultados.append({
            "id": e.get('id'),
            "nombre": e.get('nombre'),
            "promedio": features[0],
            "riesgo": pred
        })

    return jsonify(resultados)