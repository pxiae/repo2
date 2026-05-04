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
        faltas = int(e.get('faltas', 0))
        tareas = int(e.get('tareas_no_entregadas', 0))
        participacion = float(e.get('participacion', 0))

        # 🧠 lógica mejorada
        score = promedio + (participacion * 0.2) - (faltas * 3) - (tareas * 4)

        if score < 40:
            riesgo = "ALTO"
        elif score < 60:
            riesgo = "MEDIO"
        else:
            riesgo = "BAJO"

        resultados.append({
            "id": e['id'],
            "nombre": e.get('nombre', ''),
            "riesgo": riesgo,
            "score": round(score, 2)
        })

    return jsonify(resultados)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)