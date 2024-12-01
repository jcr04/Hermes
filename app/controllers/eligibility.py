from flask import Blueprint, jsonify
from app.services.external_service import (
    get_all_agencias,
    get_all_alugueis,
    get_all_veiculos,
)
from app.services.ml_service import send_to_ml

eligibility_blueprint = Blueprint('eligibility', __name__)

@eligibility_blueprint.route('/', methods=['GET'])
def evaluate_eligibility():
    try:
        # Obter dados das APIs externas
        agencias = get_all_agencias()
        alugueis = get_all_alugueis()
        veiculos = get_all_veiculos()

        # Consolidar os dados
        consolidated_data = []
        for aluguel in alugueis:
            # Validar se as chaves veiculoId e agenciaId existem
            veiculo_id = aluguel.get("veiculoId")
            agencia_id = aluguel.get("agenciaId")

            if not veiculo_id or not agencia_id:
                # Ignorar itens com dados incompletos
                continue

            veiculo = next((v for v in veiculos if v['id'] == veiculo_id), {})
            agencia = next((a for a in agencias if a['id'] == agencia_id), {})

            consolidated_data.append({
                "id": aluguel["id"],
                "dataInicio": aluguel["dataInicio"],
                "dataFim": aluguel["dataFim"],
                "status": aluguel["status"],
                "valor": aluguel["valor"],
                "agencia": agencia.get("nome", "Desconhecida"),
                "veiculo": {
                    "id": veiculo.get("id", "N/A"),
                    "marca": veiculo.get("marca", "N/A"),
                    "modelo": veiculo.get("modelo", "N/A"),
                    "placa": veiculo.get("placa", "N/A"),
                    "cor": veiculo.get("cor", "N/A"),
                    "anoFabricacao": veiculo.get("anoFabricacao", 0),
                    "adaptadoParaPCD": veiculo.get("adaptadoParaPCD", False)
                }
            })

        # Enviar dados consolidados para o modelo de machine learning
        ml_result = send_to_ml(consolidated_data)

        # Retornar resultado da ML
        return jsonify(ml_result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
