import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
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
    
    # Divisão dos dados em treinamento e validação
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Configuração e treinamento do modelo
    model = RandomForestClassifier(
        n_estimators=200,  # Aumentar o número de árvores para maior precisão
        max_depth=10,      # Limitar a profundidade para evitar overfitting
        random_state=42
    )
    model.fit(X_train, y_train)

    # Avaliação do modelo
    y_pred = model.predict(X_val)
    report = classification_report(y_val, y_pred, output_dict=True)
    print("Relatório de Classificação:", report)


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
