from flask import Blueprint, request, jsonify

ml_blueprint = Blueprint('ml', __name__)

@ml_blueprint.route('/process', methods=['POST'])
def process_ml():
    try:
        data = request.get_json()

        # Lógica simulada para validação de elegibilidade
        results = []
        for entry in data:
            elegivel = True
            motivo = "Atende a todos os critérios."

            # Regras de validação básicas
            if entry["status"] != "Ativo":
                elegivel = False
                motivo = "O status do aluguel não é Ativo."
            elif not entry["veiculo"]["adaptadoParaPCD"] and entry["agencia"] == "PCD":
                elegivel = False
                motivo = "Veículo não adaptado para PCD."

            results.append({
                "id": entry["id"],
                "elegivel": elegivel,
                "motivo": motivo
            })

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500