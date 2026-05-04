from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():

    data = request.get_json()

    resultados = []

    for e in data:
        promedio = e.get('promedio', 0)
        faltas = e.get('faltas', 0)
        estudiante_id = e.get('id')

        if promedio < 51 and faltas > 3:
            riesgo = "ALTO"
            score = 25
        else:
            riesgo = "BAJO"
            score = 75

        resultados.append({
            "id": estudiante_id,
            "riesgo": riesgo,
            "score": score
        })

    return jsonify(resultados)

if __name__ == "__main__":
    app.run()