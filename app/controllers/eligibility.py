import logging
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from app.services.external_service import (
    get_all_agencias,
    get_all_alugueis,
    get_all_veiculos,
    get_all_clientes
)
from app.services.ml_service import send_to_ml

'''
Explicação sobre as regras de funcionamento ao final do código
'''

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
        clientes = get_all_clientes()

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
            
            # Procurar o cliente correspondente
            cliente = next((c for c in clientes if c["id"] == aluguel.get("clienteId")), None)
            if not cliente:
                logging.debug(f"Cliente não encontrado para o aluguel: aluguelId{aluguel.get('id')}")
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

            # Verificar se o cliente é maior de idade
            idade_valida = 1 if cliente.get("idade", 0) >= 18 else 0 

            # Calcular validade da CNH
            if cliente.get("temCNH", False) and cliente.get("validadeCNH"):
                validade_cnh = datetime.strptime(cliente["validadeCNH"], "%Y-%m-%dT%H:%M:%S.%fZ")
                cnh_valida = 1 if validade_cnh >= datetime.now(timezone.utc) else 0
            else:
                cnh_valida = 0

            # Criar a entrada consolidada
            entry = {
                "id": aluguel.get("id", "N/A"),
                "features": [
                    1 if status_aluguel == "Ativo" else 0,    # 1. Status do aluguel
                    1 if cliente.get("isPCD", False) else 0,  # 2. Cliente é PCD
                    1 if adaptado_para_pcd else 0,            # 3. Veículo adaptado para PCD

                    valor_aluguel,                            # 4. Valor do aluguel
                    duracao_dias,                             # 5. Duração do aluguel em dias
                    1 if cliente.get("temCNH", False) else 0, # 6. Cliente possui CNH

                    cnh_valida,                              # 7. CNH válida (1 ou 0)
                    idade_valida,                            # 8. Cliente é maior de idade (1 ou 0)
                    agencia.get("numeroVeiculos", 0)         # 9. Número de veículos disponíveis na agência
                ],
                "agencia": agencia_nome,
                "veiculo": veiculo_dados
            }

            # Adicionar rótulo para treinamento, se necessário
            if train:
                label = 1  # Começa assumindo que é válido

                # Regra de rotulagem para treinamento
                if not (status_aluguel == "Ativo" and duracao_dias > 1 and valor_aluguel < 5000):
                    label = 0

                # Regra só libera carro adaptado para pcd para clientes pdcs
                if veiculo["adaptadoParaPCD"] and not cliente["isPCD"]:
                    label = 0

                # Regra em que o cliente solicitante deve possuir cnh
                if not cliente["temCNH"]:
                    label = 0

                # Regra em que o cliente deve ter 18 anos ou mais
                if cliente["idade"] < 18:
                    label = 0

                # Regra em que a CNH do cliente deve ser válida
                if cnh_valida == 0:
                    label = 0

                # Regra em que a agência deve ter mais de 4 veículos disponíveis para permitir o aluguel
                if agencia.get("numeroVeiculos", 0) <= 4:
                    label = 0

                # Regra em que a dataFim deve ser posterior à dataInicio
                #if data_fim and data_inicio and data_fim <= data_inicio:
                #    label = 0

                entry["label"] = label            

            consolidated_data.append(entry)

        # Enviar os dados consolidados para o modelo de ML
        result = send_to_ml(consolidated_data, train=train)
        logging.debug(f"Dados enviados para ML: {consolidated_data}")
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


'''
INFOS SOBRE AS REGRAS:

Nas features, os valores das posições 1, 2, 3, 6, 7 e 8 podem variar somente entre 0 e 1.
0 representando o não e 1 representando o sim.
O 4º valor deve ser inferior a 5000, 
o 5º valor deve ser maior que 1, 
já o 9º deve ser superior a 4.

É importante notar que, se todas essas condições forem cumpridas, o valor da label será 1.
Porém, caso pelo menos uma dessas condições forem descumpridas, o valor da label será 0.

Há uma situação curiosa, porém, que é no 2º e 3º valores, que representam, respectivamente, o cliente pcd e o veículo adaptado para pcd.

A regra que ficou definida para este caso foi de que se esses dois valores forem ambos 1, ou ambos 0, ou mesmo o 2º valor sendo 1 e o 3º sendo 0, a label continuará sendo 1.

Simplificando: Se o condutor não for pcd (0) ele só poderá solicitar um carro comum, 
não adaptado para pcd (0). Mas se o cliente for pcd (1), ele poderá solicitar um carro adaptado
para pcd (1) ou mesmo um carro comum (0), vai da necessidade e escolha dele.
'''