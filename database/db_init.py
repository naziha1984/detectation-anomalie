"""
Script d'initialisation de la base de données e-commerce.

Ce module crée les tables de base de données et insère des données d'exemple
pour le développement et les tests de l'application e-commerce.

Auteur: Développeur Senior Python Full Stack
Date: 2024
"""

import os
import sys
import logging
from datetime import datetime, timedelta
import random

# Ajout du répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from database.models import User, Product, Purchase, Cart

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_sample_products():
    """
    Crée des produits d'exemple pour le catalogue e-commerce.
    
    Returns:
        list: Liste des produits créés
    """
    products_data = [
        {
            'name': 'iPhone 15 Pro',
            'description': 'Smartphone Apple avec écran Super Retina XDR de 6,1 pouces, processeur A17 Pro, triple caméra 48MP',
            'price': 1199.99,
            'category': 'Électronique',
            'image_url': '/static/images/iphone15pro.jpg',
            'stock_quantity': 50
        },
        {
            'name': 'MacBook Air M2',
            'description': 'Ordinateur portable Apple avec puce M2, écran Liquid Retina 13,6 pouces, 8 Go RAM, 256 Go SSD',
            'price': 1299.99,
            'category': 'Informatique',
            'image_url': '/static/images/macbookair.jpg',
            'stock_quantity': 30
        },
        {
            'name': 'AirPods Pro 2',
            'description': 'Écouteurs sans fil Apple avec réduction de bruit active, boîtier de charge MagSafe',
            'price': 279.99,
            'category': 'Audio',
            'image_url': '/static/images/airpodspro.jpg',
            'stock_quantity': 100
        },
        {
            'name': 'iPad Air 5',
            'description': 'Tablette Apple avec puce M1, écran Liquid Retina 10,9 pouces, 64 Go de stockage',
            'price': 599.99,
            'category': 'Tablettes',
            'image_url': '/static/images/ipadair.jpg',
            'stock_quantity': 40
        },
        {
            'name': 'Apple Watch Series 9',
            'description': 'Montre connectée Apple avec écran Always-On, GPS, suivi de santé avancé',
            'price': 429.99,
            'category': 'Montres connectées',
            'image_url': '/static/images/applewatch.jpg',
            'stock_quantity': 60
        },
        {
            'name': 'Samsung Galaxy S24',
            'description': 'Smartphone Samsung avec écran Dynamic AMOLED 6,2 pouces, triple caméra 50MP, 128 Go',
            'price': 899.99,
            'category': 'Électronique',
            'image_url': '/static/images/galaxys24.jpg',
            'stock_quantity': 35
        },
        {
            'name': 'Sony WH-1000XM5',
            'description': 'Casque audio sans fil avec réduction de bruit, autonomie 30h, charge rapide',
            'price': 399.99,
            'category': 'Audio',
            'image_url': '/static/images/sonywh1000xm5.jpg',
            'stock_quantity': 25
        },
        {
            'name': 'Dell XPS 13',
            'description': 'Ordinateur portable Dell avec processeur Intel i7, écran 13,4 pouces 4K, 16 Go RAM',
            'price': 1499.99,
            'category': 'Informatique',
            'image_url': '/static/images/dellxps13.jpg',
            'stock_quantity': 20
        },
        {
            'name': 'Nintendo Switch OLED',
            'description': 'Console de jeu portable Nintendo avec écran OLED 7 pouces, manettes Joy-Con',
            'price': 349.99,
            'category': 'Gaming',
            'image_url': '/static/images/switcholed.jpg',
            'stock_quantity': 45
        },
        {
            'name': 'PlayStation 5',
            'description': 'Console de jeu Sony PlayStation 5 avec lecteur Blu-ray Ultra HD, manette DualSense',
            'price': 499.99,
            'category': 'Gaming',
            'image_url': '/static/images/ps5.jpg',
            'stock_quantity': 15
        },
        {
            'name': 'Canon EOS R6',
            'description': 'Appareil photo hybride Canon avec capteur plein format 20MP, stabilisation 5 axes',
            'price': 2499.99,
            'category': 'Photo',
            'image_url': '/static/images/canoneosr6.jpg',
            'stock_quantity': 10
        },
        {
            'name': 'DJI Mini 3 Pro',
            'description': 'Drone DJI avec caméra 4K, stabilisation 3 axes, autonomie 47 minutes',
            'price': 759.99,
            'category': 'Drones',
            'image_url': '/static/images/djimini3pro.jpg',
            'stock_quantity': 8
        }
    ]
    
    products = []
    for product_data in products_data:
        product = Product(**product_data)
        products.append(product)
        db.session.add(product)
    
    logger.info(f"Création de {len(products)} produits d'exemple")
    return products

def create_sample_users():
    """
    Crée des utilisateurs d'exemple pour les tests.
    
    Returns:
        list: Liste des utilisateurs créés
    """
    users_data = [
        {
            'username': 'admin',
            'email': 'admin@smartshopplus.com',
            'password': 'admin123',
            'is_admin': True
        },
        {
            'username': 'kenza_douiri',
            'email': 'kenza_douiri@email.com',
            'password': 'password123',
            'is_admin': False
        },
        {
            'username': 'fatima_gatt',
            'email': 'fatima.gatt@email.com',
            'password': 'password123',
            'is_admin': False
        },
        {
            'username': 'naziha_jr',
            'email': 'naziha.jr@email.com',
            'password': 'password123',
            'is_admin': False
        },
        {
            'username': 'oubey_boubakri',
            'email': 'oubey.boubakri@email.com',
            'password': 'password123',
            'is_admin': False
        },
        {
            'username': 'med_ali',
            'email': 'med.abdelwahab@email.com',
            'password': 'password123',
            'is_admin': False
        }
    ]
    
    users = []
    for user_data in users_data:
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            password_hash=User.generate_password_hash(user_data['password']),
            is_admin=user_data['is_admin']
        )
        users.append(user)
        db.session.add(user)
    
    logger.info(f"Création de {len(users)} utilisateurs d'exemple")
    return users

def create_sample_purchases(users, products):
    """
    Crée des achats d'exemple pour simuler l'historique des utilisateurs.
    
    Args:
        users (list): Liste des utilisateurs
        products (list): Liste des produits
    """
    purchases = []
    
    # Génération d'achats aléatoires pour chaque utilisateur
    for user in users:
        if user.is_admin:
            continue  # Skip admin user for purchases
        
        # Nombre d'achats aléatoire entre 3 et 8
        num_purchases = random.randint(3, 8)
        
        for _ in range(num_purchases):
            # Sélection aléatoire d'un produit
            product = random.choice(products)
            
            # Quantité aléatoire entre 1 et 3
            quantity = random.randint(1, 3)
            
            # Date d'achat aléatoire dans les 6 derniers mois
            purchase_date = datetime.utcnow() - timedelta(
                days=random.randint(1, 180),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            purchase = Purchase(
                user_id=user.id,
                product_id=product.id,
                quantity=quantity,
                price=product.price
            )
            purchase.purchase_date = purchase_date
            
            purchases.append(purchase)
            db.session.add(purchase)
    
    logger.info(f"Création de {len(purchases)} achats d'exemple")
    return purchases

def init_database():
    """
    Initialise la base de données avec toutes les tables et données d'exemple.
    """
    try:
        logger.info("Début de l'initialisation de la base de données")
        
        # Création de toutes les tables
        db.create_all()
        logger.info("Tables de base de données créées")
        
        # Vérification si des données existent déjà
        if User.query.count() > 0:
            logger.info("Des données existent déjà dans la base de données")
            return
        
        # Création des données d'exemple
        logger.info("Création des produits d'exemple...")
        products = create_sample_products()
        
        logger.info("Création des utilisateurs d'exemple...")
        users = create_sample_users()
        
        # Commit pour s'assurer que les utilisateurs et produits sont créés
        db.session.commit()
        
        logger.info("Création des achats d'exemple...")
        create_sample_purchases(users, products)
        
        # Commit final
        db.session.commit()
        
        logger.info("Initialisation de la base de données terminée avec succès")
        
        # Affichage des statistiques
        logger.info(f"Statistiques de la base de données:")
        logger.info(f"- Utilisateurs: {User.query.count()}")
        logger.info(f"- Produits: {Product.query.count()}")
        logger.info(f"- Achats: {Purchase.query.count()}")
        
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation de la base de données: {e}")
        db.session.rollback()
        raise

def clear_database():
    """
    Supprime toutes les données de la base de données.
    ATTENTION: Cette fonction supprime TOUTES les données !
    """
    try:
        logger.warning("Suppression de toutes les données de la base de données")
        
        # Suppression dans l'ordre inverse des dépendances
        Cart.query.delete()
        Purchase.query.delete()
        Product.query.delete()
        User.query.delete()
        
        db.session.commit()
        logger.info("Base de données vidée avec succès")
        
    except Exception as e:
        logger.error(f"Erreur lors de la suppression des données: {e}")
        db.session.rollback()
        raise

if __name__ == '__main__':
    """
    Point d'entrée du script d'initialisation.
    """
    with app.app_context():
        # Vérification des arguments de ligne de commande
        if len(sys.argv) > 1 and sys.argv[1] == '--clear':
            clear_database()
        else:
            init_database()
        
        print("\n" + "="*50)
        print("INITIALISATION DE LA BASE DE DONNÉES TERMINÉE")
        print("="*50)
        print("Vous pouvez maintenant lancer l'application avec:")
        print("python app.py")
        print("\nComptes de test disponibles:")
        print("- admin / admin123 (administrateur)")
        print("- ahmed_ali / password123")
        print("- fatima_gatt / password123")
        print("- mohamed_benali / password123")
        print("- amina_trabelsi / password123")
        print("- khalid_omari / password123")
        print("="*50)

