import requests

ML_ENDPOINT = "http://127.0.0.1:5000/ml/process"

def send_to_ml(data):
    """
    Envia dados consolidados para a máquina de aprendizado para processamento de elegibilidade.
    """
    response = requests.post(ML_ENDPOINT, json=data)
    response.raise_for_status() 
    return response.json()
