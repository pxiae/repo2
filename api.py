from flask import Flask, request, jsonify
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

app = Flask(__name__)

# 🔥 Datos de entrenamiento (ejemplo, puedes mejorar con datos reales)
X_train = np.array([
    [30], [40], [50], [55], [60], [65], [70], [80], [90]
])

y_train = np.array([
    "ALTO", "ALTO", "ALTO", "MEDIO", "MEDIO", "MEDIO", "BAJO", "BAJO", "BAJO"
])

# Modelo KNN
modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X_train, y_train)


@app.route('/')
def home():
    return "API ACTIVA CON KNN"


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    resultados = []

    for e in data:
        promedio = float(e.get('promedio', 0))

        pred = modelo.predict([[promedio]])[0]

        resultados.append({
            "id": e.get('id'),
            "nombre": e.get('nombre'),
            "promedio": promedio,
            "riesgo": pred
        })

    return jsonify(resultados)