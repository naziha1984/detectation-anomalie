#!/usr/bin/env python3
"""
Script de démarrage pour l'application E-Commerce IA

Ce script facilite le démarrage de l'application en :
1. Vérifiant les dépendances
2. Initialisant la base de données
3. Entraînant le modèle de recommandation
4. Lançant l'application Flask

Usage: python run.py
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """
    Vérifie que toutes les dépendances sont installées.
    """
    logger.info("Vérification des dépendances...")
    
    try:
        import flask
        import sqlalchemy
        import pandas
        import numpy
        import sklearn
        import matplotlib
        import seaborn
        logger.info("✅ Toutes les dépendances sont installées")
        return True
    except ImportError as e:
        logger.error(f"❌ Dépendance manquante: {e}")
        logger.error("Installez les dépendances avec: pip install -r requirements.txt")
        return False

def install_dependencies():
    """
    Installe les dépendances depuis requirements.txt
    """
    logger.info("Installation des dépendances...")
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        logger.info("✅ Dépendances installées avec succès")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Erreur lors de l'installation: {e}")
        return False

def initialize_database():
    """
    Initialise la base de données avec des données d'exemple.
    """
    logger.info("Initialisation de la base de données...")
    
    try:
        from database.db_init import init_database
        init_database()
        logger.info("✅ Base de données initialisée")
        return True
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'initialisation: {e}")
        return False

def train_recommendation_model():
    """
    Entraîne le modèle de recommandation.
    """
    logger.info("Entraînement du modèle de recommandation...")
    
    try:
        from recommender.train_model import main as train_main
        train_main()
        logger.info("✅ Modèle de recommandation entraîné")
        return True
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'entraînement: {e}")
        return False

def start_application():
    """
    Lance l'application Flask.
    """
    logger.info("Démarrage de l'application...")
    
    try:
        from app import app
        logger.info("🚀 Application démarrée sur http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        logger.error(f"❌ Erreur lors du démarrage: {e}")
        return False

def main():
    """
    Fonction principale du script de démarrage.
    """
    print("="*60)
    print("🛍️ E-COMMERCE IA - SCRIPT DE DÉMARRAGE")
    print("="*60)
    
    # Vérification des dépendances
    if not check_dependencies():
        logger.info("Tentative d'installation automatique...")
        if not install_dependencies():
            logger.error("❌ Impossible d'installer les dépendances automatiquement")
            logger.error("Installez manuellement avec: pip install -r requirements.txt")
            return False
    
    # Initialisation de la base de données
    if not initialize_database():
        logger.error("❌ Échec de l'initialisation de la base de données")
        return False
    
    # Entraînement du modèle
    if not train_recommendation_model():
        logger.warning("⚠️ Échec de l'entraînement du modèle (l'application fonctionnera quand même)")
    
    print("\n" + "="*60)
    print("✅ PRÉPARATION TERMINÉE")
    print("="*60)
    print("🌐 L'application sera accessible sur: http://localhost:5000")
    print("👤 Comptes de test disponibles:")
    print("   - admin / admin123 (administrateur)")
    print("   - kenza_douiri / password123")
    print("   - fatima_gatt / password123")
    print("   - naziha_jr / password123")
    print("   - oubey_boubakri / password123")
    print("   - med_ali / password123")
    print("="*60)
    
    # Démarrage de l'application
    start_application()

if __name__ == '__main__':
    main()
