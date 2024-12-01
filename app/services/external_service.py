import requests

BASE_URL = "https://locadaov3.onrender.com/api/"

def get_all_agencias():
    response = requests.get(f"{BASE_URL}Agencia")
    response.raise_for_status()
    return response.json()

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
