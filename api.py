from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "API ACTIVA"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    resultados = []

    for e in data:
        promedio = float(e.get('promedio', 0))

        # 🔥 LÓGICA INTELIGENTE
        if promedio < 51:
            riesgo = "ALTO"
        elif promedio < 65:
            riesgo = "MEDIO"
        else:
            riesgo = "BAJO"

        resultados.append({
            "id": e.get('id'),
            "nombre": e.get('nombre'),
            "promedio": promedio,
            "riesgo": riesgo
        })

    return jsonify(resultados)