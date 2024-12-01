import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    DEBUG = os.getenv('DEBUG', True)
    ML_MODEL_PATH = os.getenv('ML_MODEL_PATH', './models/model.pkl')
