from flask import Flask, request, jsonify
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np
import requests
import os

app = Flask(__name__)

# ==============================
# 🔥 DATOS DE ENTRENAMIENTO
# ==============================
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

# ==============================
# 🔥 MODELO KNN
# ==============================
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X_train_scaled, y_train)

# ==============================
# 🔑 API KEY (Render ENV)
# ==============================
API_KEY = os.getenv("OPENAI_API_KEY")

# ==============================
# 🧠 IA OPCIONAL
# ==============================
def generar_recomendacion_ia(nombre, promedio, asistencia, tareas, riesgo):

    if not API_KEY:
        return "❌ SIN API KEY"

    prompt = f"""
    Estudiante: {nombre}
    Promedio: {promedio}
    Asistencia: {asistencia}
    Tareas: {tareas}
    Riesgo: {riesgo}

    Genera una recomendación pedagógica corta.
    """

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4.1-mini",
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=10
        )

        print(response.text)  # 🔥 IMPORTANTE

        return response.json()['choices'][0]['message']['content']

    except Exception as e:
        return f"❌ ERROR IA: {str(e)}"


@app.route('/')
def home():
    return "API KNN + IA ACTIVA"


@app.route('/predict', methods=['POST'])
def predict():

    data = request.json
    resultados = []

    for e in data:

        features = e.get('features', [0, 0, 0, 0])
        features_scaled = scaler.transform([features])

        pred = modelo.predict(features_scaled)[0]

        promedio = features[0]
        asistencia = features[1]
        tareas = features[2]
        prom_tareas = features[3]

        # ==============================
        # 🔥 REGLAS INTELIGENTES
        # ==============================
        recomendaciones = []

        if promedio < 51:
            recomendaciones.append("Bajo rendimiento académico")

        if asistencia < 60:
            recomendaciones.append("Baja asistencia")

        if tareas < 50:
            recomendaciones.append("Poca entrega de tareas")

        if promedio < 51 and asistencia < 60:
            recomendaciones.append("Intervención urgente")

        if promedio >= 80 and asistencia > 80:
            recomendaciones.append("Buen desempeño")

        recomendacion_texto = ", ".join(recomendaciones) if recomendaciones else "Rendimiento estable"

        # ==============================
        # 🧠 IA (OPCIONAL)
        # ==============================
        recomendacion_ia = generar_recomendacion_ia(
            e.get('nombre'),
            promedio,
            asistencia,
            tareas,
            pred
        )

        resultados.append({
            "id": e.get('id'),
            "nombre": e.get('nombre'),
            "promedio": promedio,
            "asistencia": asistencia,
            "tareas": tareas,
            "prom_tareas": prom_tareas,
            "riesgo": pred,
            "recomendacion": recomendacion_texto,
            "recomendacion_ia": recomendacion_ia
        })

    return jsonify(resultados)