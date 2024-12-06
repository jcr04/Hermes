import requests

BASE_URL = "https://locadaov3.onrender.com/api/"

def get_all_agencias():
    """
    Busca os detalhes de todas as agências.
    """
    # Obter os IDs de todas as agências
    response = requests.get(f"{BASE_URL}Agencia")
    response.raise_for_status()
    agencia_ids = response.json()

    # Buscar os detalhes de cada agência usando os IDs
    agencias = []
    for agencia_id in agencia_ids:
        detalhe_response = requests.get(f"{BASE_URL}Agencia/{agencia_id}")
        detalhe_response.raise_for_status()
        agencias.append(detalhe_response.json())

    return agencias

def get_all_clientes():
    response = requests.get(f"{BASE_URL}Clientes")
    response.raise_for_status()
    return response.json()

def get_all_alugueis():
    response = requests.get(f"{BASE_URL}Alugueis")
    response.raise_for_status()
    return response.json()

def get_all_veiculos():
    response = requests.get(f"{BASE_URL}Veiculos")
    response.raise_for_status()
    return response.json()
