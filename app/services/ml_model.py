import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

MODEL_PATH = './models/eligibility_model.pkl'

# Treinar o modelo com dados fornecidos
def train_model_with_data(data):
    """
    Treina o modelo com os dados fornecidos.
    :param data: Lista de pares (X, y) onde X são as features e y os labels.
    """
    X = [
        [1, 1, 150],  # Elegível
        [0, 0, 200],  # Não Elegível (status inativo)
        [1, 0, 250],  # Não Elegível (não adaptado para PCD)
        [1, 1, 300],  # Elegível
        [0, 1, 100],  # Não Elegível
    ]
    y = [1, 0, 0, 1, 0]
    X, y = zip(*data)  # Separar features e labels
    X = np.array(X)
    y = np.array(y)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Salvar o modelo treinado
    os.makedirs('./models', exist_ok=True)
    with open(MODEL_PATH, 'wb') as model_file:
        pickle.dump(model, model_file)

# Prever elegibilidade com o modelo treinado
def predict_eligibility(data):
    """
    Faz previsões de elegibilidade com base nos dados fornecidos.
    :param data: Lista de features.
    :return: Lista de previsões.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Modelo não treinado. Treine o modelo antes de fazer previsões.")
    
    with open(MODEL_PATH, 'rb') as model_file:
        model = pickle.load(model_file)

    features = np.array(data)
    predictions = model.predict(features)
    return predictions.tolist()
