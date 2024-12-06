import requests

ML_ENDPOINT = "http://127.0.0.1:5000/ml/process"

def send_to_ml(data, train=False):
    """
    Envia dados para o serviço de Machine Learning.
    :param data: Dados para previsão ou treinamento.
    :param train: Booleano indicando se é para treinar o modelo.
    """
    payload = {
        "data": data,
        "train": train
    }
    response = requests.post(ML_ENDPOINT, json=payload)
    response.raise_for_status()
    return response.json()
