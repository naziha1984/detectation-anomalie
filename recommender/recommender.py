"""
Moteur de recommandation intelligent pour l'e-commerce.

Ce module implémente un système de recommandation hybride utilisant :
- Filtrage collaboratif basé sur les utilisateurs
- Filtrage collaboratif basé sur les produits
- Recommandations populaires
- Analyse de similarité
"""

import logging
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from typing import List, Dict, Tuple, Optional
import pickle
import os
from datetime import datetime

# Configuration du logging
logger = logging.getLogger(__name__)

class RecommendationEngine:
    """
    Moteur de recommandation intelligent pour l'e-commerce.
    
    Ce moteur utilise plusieurs algorithmes de recommandation :
    - Filtrage collaboratif user-based
    - Filtrage collaboratif item-based
    - Factorisation matricielle (SVD)
    - Recommandations populaires
    """
    
    def __init__(self, model_cache_dir: str = 'recommender/cache'):
        """
        Initialise le moteur de recommandation.
        
        Args:
            model_cache_dir (str): Répertoire pour le cache des modèles
        """
        self.model_cache_dir = model_cache_dir
        self.user_item_matrix = None
        self.user_similarity_matrix = None
        self.item_similarity_matrix = None
        self.svd_model = None
        self.product_popularity = None
        
        # Création du répertoire de cache si nécessaire
        os.makedirs(model_cache_dir, exist_ok=True)
        
        logger.info("Moteur de recommandation initialisé")
    
    def load_data_from_database(self, db_session):
        """
        Charge les données depuis la base de données SQLite.
        
        Args:
            db_session: Session SQLAlchemy
        """
        try:
            # Import des modèles ici pour éviter les imports circulaires
            from database.models import User, Product, Purchase
            
            # Récupération des données
            purchases = db_session.query(Purchase).all()
            users = db_session.query(User).all()
            products = db_session.query(Product).all()
            
            # Conversion en DataFrame
            purchase_data = []
            for purchase in purchases:
                purchase_data.append({
                    'user_id': purchase.user_id,
                    'product_id': purchase.product_id,
                    'quantity': purchase.quantity,
                    'rating': min(purchase.quantity, 5)  # Rating basé sur la quantité
                })
            
            self.df = pd.DataFrame(purchase_data)
            
            # Création des mappings
            self.user_id_to_index = {user.id: idx for idx, user in enumerate(users)}
            self.index_to_user_id = {idx: user.id for idx, user in enumerate(users)}
            self.product_id_to_index = {product.id: idx for idx, product in enumerate(products)}
            self.index_to_product_id = {idx: product.id for idx, product in enumerate(products)}
            
            logger.info(f"Données chargées: {len(self.df)} achats, {len(users)} utilisateurs, {len(products)} produits")
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement des données: {e}")
            raise
    
    def create_user_item_matrix(self):
        """
        Crée la matrice utilisateur-produit pour les calculs de similarité.
        """
        try:
            if self.df.empty:
                logger.warning("Aucune donnée disponible pour créer la matrice")
                return
            
            # Création de la matrice utilisateur-produit
            self.user_item_matrix = self.df.pivot_table(
                index='user_id',
                columns='product_id',
                values='rating',
                fill_value=0
            )
            
            # Normalisation des ratings par utilisateur (centrage)
            user_means = self.user_item_matrix.mean(axis=1)
            self.user_item_matrix_normalized = self.user_item_matrix.sub(user_means, axis=0)
            self.user_item_matrix_normalized = self.user_item_matrix_normalized.fillna(0)
            
            logger.info(f"Matrice utilisateur-produit créée: {self.user_item_matrix.shape}")
            
        except Exception as e:
            logger.error(f"Erreur lors de la création de la matrice: {e}")
            raise
    
    def compute_user_similarity(self):
        """
        Calcule la matrice de similarité entre utilisateurs.
        """
        try:
            if self.user_item_matrix_normalized is None:
                self.create_user_item_matrix()
            
            # Calcul de la similarité cosinus
            self.user_similarity_matrix = cosine_similarity(self.user_item_matrix_normalized)
            
            # Conversion en DataFrame pour faciliter l'utilisation
            user_ids = self.user_item_matrix.index
            self.user_similarity_df = pd.DataFrame(
                self.user_similarity_matrix,
                index=user_ids,
                columns=user_ids
            )
            
            logger.info("Matrice de similarité utilisateurs calculée")
            
        except Exception as e:
            logger.error(f"Erreur lors du calcul de la similarité utilisateurs: {e}")
            raise
    
    def compute_item_similarity(self):
        """
        Calcule la matrice de similarité entre produits.
        """
        try:
            if self.user_item_matrix is None:
                self.create_user_item_matrix()
            
            # Transposition pour avoir les produits en lignes
            item_user_matrix = self.user_item_matrix.T
            
            # Calcul de la similarité cosinus
            self.item_similarity_matrix = cosine_similarity(item_user_matrix)
            
            # Conversion en DataFrame
            product_ids = self.user_item_matrix.columns
            self.item_similarity_df = pd.DataFrame(
                self.item_similarity_matrix,
                index=product_ids,
                columns=product_ids
            )
            
            logger.info("Matrice de similarité produits calculée")
            
        except Exception as e:
            logger.error(f"Erreur lors du calcul de la similarité produits: {e}")
            raise
    
    def train_svd_model(self, n_components: int = 50):
        """
        Entraîne un modèle SVD pour la factorisation matricielle.
        
        Args:
            n_components (int): Nombre de composantes pour la SVD
        """
        try:
            if self.user_item_matrix is None:
                self.create_user_item_matrix()
            
            # Entraînement du modèle SVD
            self.svd_model = TruncatedSVD(n_components=n_components, random_state=42)
            self.svd_matrix = self.svd_model.fit_transform(self.user_item_matrix)
            
            logger.info(f"Modèle SVD entraîné avec {n_components} composantes")
            
        except Exception as e:
            logger.error(f"Erreur lors de l'entraînement du modèle SVD: {e}")
            raise
    
    def compute_product_popularity(self):
        """
        Calcule la popularité des produits basée sur les ventes.
        """
        try:
            if self.df.empty:
                logger.warning("Aucune donnée pour calculer la popularité")
                return
            
            # Calcul de la popularité par produit
            self.product_popularity = self.df.groupby('product_id')['quantity'].sum().sort_values(ascending=False)
            
            logger.info("Popularité des produits calculée")
            
        except Exception as e:
            logger.error(f"Erreur lors du calcul de la popularité: {e}")
            raise
    
    def get_user_recommendations(self, user_id: int, limit: int = 5, method: str = 'hybrid') -> List[int]:
        """
        Génère des recommandations pour un utilisateur donné.
        
        Args:
            user_id (int): ID de l'utilisateur
            limit (int): Nombre de recommandations à retourner
            method (str): Méthode de recommandation ('user', 'item', 'svd', 'popular', 'hybrid')
            
        Returns:
            List[int]: Liste des IDs des produits recommandés
        """
        try:
            if method == 'user':
                return self._get_user_based_recommendations(user_id, limit)
            elif method == 'item':
                return self._get_item_based_recommendations(user_id, limit)
            elif method == 'svd':
                return self._get_svd_recommendations(user_id, limit)
            elif method == 'popular':
                return self._get_popular_recommendations(user_id, limit)
            elif method == 'hybrid':
                return self._get_hybrid_recommendations(user_id, limit)
            else:
                raise ValueError(f"Méthode de recommandation inconnue: {method}")
                
        except Exception as e:
            logger.error(f"Erreur lors de la génération des recommandations: {e}")
            return []
    
    def _get_user_based_recommendations(self, user_id: int, limit: int) -> List[int]:
        """
        Recommandations basées sur la similarité utilisateur.
        """
        if self.user_similarity_df is None:
            self.compute_user_similarity()
        
        if user_id not in self.user_similarity_df.index:
            return self._get_popular_recommendations(user_id, limit)
        
        # Utilisateurs similaires
        similar_users = self.user_similarity_df[user_id].sort_values(ascending=False)[1:6]
        
        # Produits achetés par les utilisateurs similaires
        recommendations = []
        for similar_user_id, similarity in similar_users.items():
            user_purchases = self.df[self.df['user_id'] == similar_user_id]['product_id'].unique()
            recommendations.extend(user_purchases)
        
        # Filtrage des produits déjà achetés par l'utilisateur
        user_purchases = self.df[self.df['user_id'] == user_id]['product_id'].unique()
        recommendations = [p for p in recommendations if p not in user_purchases]
        
        # Déduplication et limitation
        unique_recommendations = list(dict.fromkeys(recommendations))[:limit]
        
        return unique_recommendations
    
    def _get_item_based_recommendations(self, user_id: int, limit: int) -> List[int]:
        """
        Recommandations basées sur la similarité produit.
        """
        if self.item_similarity_df is None:
            self.compute_item_similarity()
        
        if user_id not in self.user_item_matrix.index:
            return self._get_popular_recommendations(user_id, limit)
        
        # Produits achetés par l'utilisateur
        user_purchases = self.df[self.df['user_id'] == user_id]['product_id'].unique()
        
        if not user_purchases:
            return self._get_popular_recommendations(user_id, limit)
        
        # Calcul des scores de similarité
        scores = {}
        for purchased_product in user_purchases:
            if purchased_product in self.item_similarity_df.index:
                similar_products = self.item_similarity_df[purchased_product].sort_values(ascending=False)[1:6]
                for product_id, similarity in similar_products.items():
                    if product_id not in user_purchases:
                        scores[product_id] = scores.get(product_id, 0) + similarity
        
        # Tri par score et limitation
        recommendations = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        return [product_id for product_id, _ in recommendations]
    
    def _get_svd_recommendations(self, user_id: int, limit: int) -> List[int]:
        """
        Recommandations basées sur la factorisation matricielle SVD.
        """
        if self.svd_model is None:
            self.train_svd_model()
        
        if user_id not in self.user_item_matrix.index:
            return self._get_popular_recommendations(user_id, limit)
        
        # Index de l'utilisateur dans la matrice
        user_index = self.user_item_matrix.index.get_loc(user_id)
        
        # Prédiction des scores pour tous les produits
        user_svd = self.svd_matrix[user_index]
        predicted_scores = self.svd_model.inverse_transform([user_svd])[0]
        
        # Création d'un DataFrame avec les scores prédits
        scores_df = pd.DataFrame({
            'product_id': self.user_item_matrix.columns,
            'predicted_score': predicted_scores
        })
        
        # Filtrage des produits déjà achetés
        user_purchases = self.df[self.df['user_id'] == user_id]['product_id'].unique()
        scores_df = scores_df[~scores_df['product_id'].isin(user_purchases)]
        
        # Tri par score prédit et limitation
        recommendations = scores_df.nlargest(limit, 'predicted_score')['product_id'].tolist()
        
        return recommendations
    
    def _get_popular_recommendations(self, user_id: int, limit: int) -> List[int]:
        """
        Recommandations basées sur la popularité des produits.
        """
        if self.product_popularity is None:
            self.compute_product_popularity()
        
        if self.product_popularity is None or self.product_popularity.empty:
            return []
        
        # Filtrage des produits déjà achetés par l'utilisateur
        user_purchases = self.df[self.df['user_id'] == user_id]['product_id'].unique()
        popular_products = self.product_popularity[~self.product_popularity.index.isin(user_purchases)]
        
        return popular_products.head(limit).index.tolist()
    
    def _get_hybrid_recommendations(self, user_id: int, limit: int) -> List[int]:
        """
        Recommandations hybrides combinant plusieurs méthodes.
        """
        # Récupération des recommandations de chaque méthode
        user_recs = self._get_user_based_recommendations(user_id, limit * 2)
        item_recs = self._get_item_based_recommendations(user_id, limit * 2)
        popular_recs = self._get_popular_recommendations(user_id, limit * 2)
        
        # Combinaison avec pondération
        all_recommendations = []
        
        # Pondération des méthodes
        weights = {'user': 0.4, 'item': 0.4, 'popular': 0.2}
        
        # Ajout des recommandations avec pondération
        for rec in user_recs:
            all_recommendations.append((rec, weights['user']))
        
        for rec in item_recs:
            all_recommendations.append((rec, weights['item']))
        
        for rec in popular_recs:
            all_recommendations.append((rec, weights['popular']))
        
        # Agrégation des scores
        scores = {}
        for product_id, weight in all_recommendations:
            scores[product_id] = scores.get(product_id, 0) + weight
        
        # Tri par score et limitation
        recommendations = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        return [product_id for product_id, _ in recommendations]
    
    def get_similar_products(self, product_id: int, limit: int = 5) -> List[int]:
        """
        Trouve des produits similaires à un produit donné.
        
        Args:
            product_id (int): ID du produit de référence
            limit (int): Nombre de produits similaires à retourner
            
        Returns:
            List[int]: Liste des IDs des produits similaires
        """
        try:
            if self.item_similarity_df is None:
                self.compute_item_similarity()
            
            if product_id not in self.item_similarity_df.index:
                return []
            
            # Produits similaires
            similar_products = self.item_similarity_df[product_id].sort_values(ascending=False)[1:limit+1]
            
            return similar_products.index.tolist()
            
        except Exception as e:
            logger.error(f"Erreur lors de la recherche de produits similaires: {e}")
            return []
    
    def update_model(self):
        """
        Met à jour le modèle de recommandation avec les nouvelles données.
        """
        try:
            logger.info("Mise à jour du modèle de recommandation")
            
            # Recalcul de toutes les matrices
            self.create_user_item_matrix()
            self.compute_user_similarity()
            self.compute_item_similarity()
            self.train_svd_model()
            self.compute_product_popularity()
            
            # Sauvegarde du modèle mis à jour
            self.save_model()
            
            logger.info("Modèle de recommandation mis à jour avec succès")
            
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du modèle: {e}")
            raise
    
    def save_model(self):
        """
        Sauvegarde le modèle de recommandation sur disque.
        """
        try:
            model_data = {
                'user_item_matrix': self.user_item_matrix,
                'user_similarity_df': self.user_similarity_df,
                'item_similarity_df': self.item_similarity_df,
                'product_popularity': self.product_popularity,
                'svd_model': self.svd_model,
                'svd_matrix': self.svd_matrix,
                'timestamp': datetime.now()
            }
            
            cache_file = os.path.join(self.model_cache_dir, 'recommendation_model.pkl')
            with open(cache_file, 'wb') as f:
                pickle.dump(model_data, f)
            
            logger.info(f"Modèle sauvegardé dans {cache_file}")
            
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde du modèle: {e}")
    
    def load_model(self):
        """
        Charge le modèle de recommandation depuis le disque.
        """
        try:
            cache_file = os.path.join(self.model_cache_dir, 'recommendation_model.pkl')
            
            if not os.path.exists(cache_file):
                logger.info("Aucun modèle en cache trouvé")
                return False
            
            with open(cache_file, 'rb') as f:
                model_data = pickle.load(f)
            
            # Restauration des attributs
            self.user_item_matrix = model_data.get('user_item_matrix')
            self.user_similarity_df = model_data.get('user_similarity_df')
            self.item_similarity_df = model_data.get('item_similarity_df')
            self.product_popularity = model_data.get('product_popularity')
            self.svd_model = model_data.get('svd_model')
            self.svd_matrix = model_data.get('svd_matrix')
            
            logger.info("Modèle chargé depuis le cache")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle: {e}")
            return False

