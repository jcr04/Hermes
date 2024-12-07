from flask import Blueprint, request, jsonify
from app.services.ml_model import train_model_with_data, predict_eligibility

ml_blueprint = Blueprint('ml', __name__)

@ml_blueprint.route('/process', methods=['POST'])
def process_ml():
    try:
        payload = request.get_json()
        data = payload.get("data", [])
        train = payload.get("train", False)

        if train:
            # Validação de dados para treinamento
            training_data = []
            for entry in data:
                if "features" in entry and "label" in entry:
                    training_data.append((entry["features"], entry["label"]))

            if not training_data:
                return jsonify({"error": "Dados insuficientes para treinamento."}), 400

            train_model_with_data(training_data)
            return jsonify({"message": "Modelo treinado com sucesso!"}), 200

        else:
            # Validação de dados para previsão
            features = [entry["features"] for entry in data if "features" in entry]
            if not features:
                return jsonify({"error": "Dados insuficientes para previsão."}), 400

            predictions = predict_eligibility(features)

            results = []
            for i, entry in enumerate(data):
                results.append({
                    "id": entry["id"],
                    "elegivel": bool(predictions[i]),
                    "motivo": "Elegível" if predictions[i] else "Não atende aos critérios."
                })

            return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
