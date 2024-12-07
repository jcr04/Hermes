import logging
from datetime import datetime
from flask import Blueprint, jsonify, request
from app.services.external_service import (
    get_all_agencias,
    get_all_alugueis,
    get_all_veiculos,
)
from app.services.ml_service import send_to_ml

eligibility_blueprint = Blueprint('eligibility', __name__)

@eligibility_blueprint.route('/', methods=['POST'])
def evaluate_or_train():
    try:
        payload = request.get_json()
        train = payload.get("train", False)

        # Buscar todos os dados necessários
        agencias = get_all_agencias()
        alugueis = get_all_alugueis()
        veiculos = get_all_veiculos()

        # Consolidar os dados
        consolidated_data = []
        for aluguel in alugueis:
            veiculo_dados = aluguel.get("veiculo", {})
            agencia_nome = aluguel.get("agencia")

            if not veiculo_dados or not agencia_nome:
                logging.debug(f"Dados incompletos no aluguel: {aluguel}")
                continue

            # Procurar o veículo correspondente
            veiculo = next((v for v in veiculos if v.get("id") == veiculo_dados.get("id")), None)
            if not veiculo:
                logging.debug(f"Veículo não encontrado: veiculoId={veiculo_dados.get('id')}")
                continue

            # Procurar a agência correspondente
            agencia = next((a for a in agencias if a["agencia"].get("nome") == agencia_nome), None)
            if not agencia:
                logging.debug(f"Agência não encontrada: agenciaNome={agencia_nome}")
                continue

            # Regras adicionais
            # Converter strings de data para objetos datetime
            data_inicio = aluguel.get("dataInicio")
            data_fim = aluguel.get("dataFim")

            if data_inicio and data_fim:
                try:
                    data_inicio = datetime.strptime(data_inicio, "%Y-%m-%dT%H:%M:%S.%fZ")
                    data_fim = datetime.strptime(data_fim, "%Y-%m-%dT%H:%M:%S.%fZ")
                    duracao_dias = (data_fim - data_inicio).days
                except ValueError:
                    logging.debug(f"Formato de data inválido: dataInicio={data_inicio}, dataFim={data_fim}")
                    duracao_dias = 0
            else:
                duracao_dias = 0

            # Outros valores do aluguel
            valor_aluguel = aluguel.get("valor", 0)
            status_aluguel = aluguel.get("status")
            adaptado_para_pcd = veiculo.get("adaptadoParaPCD", False)

            # Criar a entrada consolidada
            entry = {
                "id": aluguel.get("id", "N/A"),
                "features": [
                    1 if status_aluguel == "Ativo" else 0,  # Status
                    1 if adaptado_para_pcd else 0,           # Adaptado para PCD
                    valor_aluguel,                           # Valor do aluguel
                    duracao_dias                             # Duração do aluguel em dias
                ],
                "agencia": agencia_nome,
                "veiculo": veiculo_dados
            }

            # Adicionar rótulo para treinamento, se necessário
            if train:
                # Regra de rotulagem para treinamento
                entry["label"] = 1 if (status_aluguel == "Ativo" and duracao_dias > 1 and valor_aluguel < 5000) else 0

            consolidated_data.append(entry)

        # Enviar os dados consolidados para o modelo de ML
        result = send_to_ml(consolidated_data, train=train)
        logging.debug(f"Dados enviados para ML: {consolidated_data}")
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
