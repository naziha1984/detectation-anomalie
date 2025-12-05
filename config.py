"""
Configuration de l'application E-Commerce IA

Ce module contient toutes les configurations de l'application,
incluant les variables d'environnement et les paramètres par défaut.
"""

import os
from pathlib import Path

class Config:
    """
    Configuration de base de l'application.
    """
    # Configuration Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'votre-cle-secrete-super-securisee-2024'
    
    # Configuration de la base de données
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///ecommerce.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuration des uploads
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'static/images'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    
    # Configuration du système de recommandation
    RECOMMENDATION_CACHE_DIR = os.environ.get('RECOMMENDATION_CACHE_DIR') or 'recommender/cache'
    RECOMMENDATION_UPDATE_INTERVAL = int(os.environ.get('RECOMMENDATION_UPDATE_INTERVAL', 3600))  # 1 heure
    
    # Configuration du logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/app.log')
    
    # Configuration de l'application
    APP_NAME = 'SmartShopPlus'
    APP_VERSION = '1.0.0'
    APP_DESCRIPTION = 'Site e-commerce avec système de recommandation intelligent'

class DevelopmentConfig(Config):
    """
    Configuration pour l'environnement de développement.
    """
    DEBUG = True
    TESTING = False
    
    # Base de données de développement
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ecommerce_dev.db'
    
    # Logging plus verbeux
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """
    Configuration pour l'environnement de production.
    """
    DEBUG = False
    TESTING = False
    
    # Base de données de production (PostgreSQL recommandé)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:password@localhost/ecommerce'
    
    # Logging de production
    LOG_LEVEL = 'WARNING'
    
    # Sécurité renforcée
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY doit être définie en production")

class TestingConfig(Config):
    """
    Configuration pour les tests.
    """
    TESTING = True
    DEBUG = True
    
    # Base de données de test
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Désactiver le logging pendant les tests
    LOG_LEVEL = 'CRITICAL'

# Dictionnaire des configurations disponibles
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """
    Retourne la configuration appropriée selon l'environnement.
    
    Returns:
        Config: Configuration de l'application
    """
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
