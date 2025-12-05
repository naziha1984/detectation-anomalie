#!/bin/bash

echo "========================================"
echo "   E-COMMERCE IA - DEMARRAGE RAPIDE"
echo "========================================"
echo

echo "Installation des dépendances..."
pip install -r requirements.txt

echo
echo "Initialisation de la base de données..."
python database/db_init.py

echo
echo "Entraînement du modèle de recommandation..."
python recommender/train_model.py

echo
echo "Démarrage de l'application..."
echo "L'application sera accessible sur: http://localhost:5000"
echo
echo "Comptes de test disponibles:"
echo "- admin / admin123 (administrateur)"
echo "- kenza_douiri / password123"
echo "- fatima_gatt / password123"
echo "- naziha_jr / password123"
echo "- oubey_boubakri / password123"
echo "- med_ali / password123"
echo

python app.py
