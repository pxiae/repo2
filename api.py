from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "API ACTIVA"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    resultados = []

    for e in data['estudiantes']:

        promedio = e['promedio']
        faltas = e['faltas']
        tareas = e['tareas_entregadas']
        total = e['tareas_totales']
        participacion = e['participacion']
        examenes = e['examenes']
        retrasos = e['retrasos']

        rendimiento = tareas / total if total > 0 else 0
        disciplina = faltas + retrasos

        score = (
            promedio * 0.4 +
            examenes * 0.2 +
            participacion * 0.1 +
            rendimiento * 100 * 0.2 -
            disciplina * 2
        )

        if score < 50:
            riesgo = "ALTO"
        elif score < 70:
            riesgo = "MEDIO"
        else:
            riesgo = "BAJO"

        resultados.append({
            "id": e['id'],
            "score": round(score, 2),
            "riesgo": riesgo
        })

    return jsonify(resultados)

if __name__ == '__main__':
    app.run()