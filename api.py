from flask import Flask, request, jsonify
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np
import google.generativeai as genai
import os

app = Flask(__name__)

# ==============================
# 🔥 CONFIGURAR GEMINI API
# ==============================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# ==============================
# 🔥 DATOS DE ENTRENAMIENTO
# ==============================
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

# ==============================
# 🔥 MODELO KNN
# ==============================
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X_train_scaled, y_train)

# ==============================
# 🧠 FUNCIÓN IA (GEMINI)
# ==============================
def generar_recomendacion_ia(nombre, promedio, asistencia, tareas, riesgo):

    if not GEMINI_API_KEY:
        return "⚠️ IA no configurada"

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt = f"""
        Eres un asistente educativo.

        Estudiante: {nombre}
        Promedio: {promedio}
        Asistencia: {asistencia}
        Tareas: {tareas}
        Nivel de riesgo: {riesgo}

        Genera una recomendación pedagógica breve, clara y profesional.
        """

        response = model.generate_content(prompt)

        return response.text.strip()

    except Exception as e:
        return f"❌ Error IA: {str(e)}"

# ==============================
# 🏠 HOME
# ==============================
@app.route('/')
def home():
    return "API KNN + GEMINI ACTIVA"

# ==============================
# 🔮 PREDICCIÓN
# ==============================
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
        # 🔥 REGLAS (BASE)
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
        # 🧠 IA (GEMINI)
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

# ==============================
# 🚀 RUN
# ==============================
if __name__ == '__main__':
    app.run(debug=True)