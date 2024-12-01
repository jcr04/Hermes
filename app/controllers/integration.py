from flask import Blueprint, jsonify
from app.services.external_service import (
    get_all_agencias,
    get_all_clientes,
    get_all_alugueis,
    get_all_veiculos,
)

integration_blueprint = Blueprint('integration', __name__)

@integration_blueprint.route('/agencias', methods=['GET'])
def fetch_agencias():
    agencias = get_all_agencias()
    return jsonify(agencias)

@integration_blueprint.route('/clientes', methods=['GET'])
def fetch_clientes():
    clientes = get_all_clientes()
    return jsonify(clientes)

@integration_blueprint.route('/alugueis', methods=['GET'])
def fetch_alugueis():
    alugueis = get_all_alugueis()
    return jsonify(alugueis)

@integration_blueprint.route('/veiculos', methods=['GET'])
def fetch_veiculos():
    veiculos = get_all_veiculos()
    return jsonify(veiculos)
