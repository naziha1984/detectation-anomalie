"""
Module d'évaluation des performances du modèle DBSCAN
"""

import numpy as np
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def evaluate_clustering(X: np.ndarray, labels: np.ndarray) -> dict:
    """
    Évalue la qualité du clustering DBSCAN avec plusieurs métriques.
    
    Args:
        X: Matrice de features normalisées (n_samples, n_features)
        labels: Labels de cluster de DBSCAN
        
    Returns:
        Dictionnaire contenant les métriques d'évaluation
    """
    logger.info("Évaluation de la qualité du clustering")
    
    # Filtrer les anomalies pour certaines métriques
    non_noise_mask = labels != -1
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = np.sum(labels == -1)
    n_samples = len(labels)
    
    metrics = {
        'n_clusters': n_clusters,
        'n_noise_points': n_noise,
        'n_clustered_points': np.sum(non_noise_mask),
        'noise_ratio': n_noise / n_samples if n_samples > 0 else 0.0,
    }
    
    # Calculer les métriques seulement si on a au moins 2 clusters
    if n_clusters >= 2 and np.sum(non_noise_mask) > 1:
        try:
            # Silhouette Score (exclut le bruit)
            silhouette = silhouette_score(X[non_noise_mask], labels[non_noise_mask])
            metrics['silhouette_score'] = silhouette
            
            # Calinski-Harabasz Index (exclut le bruit)
            ch_score = calinski_harabasz_score(X[non_noise_mask], labels[non_noise_mask])
            metrics['calinski_harabasz_score'] = ch_score
            
            # Davies-Bouldin Index (exclut le bruit)
            db_score = davies_bouldin_score(X[non_noise_mask], labels[non_noise_mask])
            metrics['davies_bouldin_score'] = db_score
            
            logger.info(f"Silhouette Score: {silhouette:.4f}")
            logger.info(f"Calinski-Harabasz Score: {ch_score:.4f}")
            logger.info(f"Davies-Bouldin Score: {db_score:.4f}")
            
        except Exception as e:
            logger.warning(f"Impossible de calculer certaines métriques: {e}")
            metrics['silhouette_score'] = None
            metrics['calinski_harabasz_score'] = None
            metrics['davies_bouldin_score'] = None
    else:
        logger.warning("Pas assez de clusters pour calculer certaines métriques")
        metrics['silhouette_score'] = None
        metrics['calinski_harabasz_score'] = None
        metrics['davies_bouldin_score'] = None
    
    return metrics


def interpret_metrics(metrics: dict) -> dict:
    """
    Interprète les métriques de clustering.
    
    Args:
        metrics: Dictionnaire de métriques
        
    Returns:
        Dictionnaire avec les interprétations
    """
    interpretations = {}
    
    # Silhouette Score
    if metrics.get('silhouette_score') is not None:
        sil = metrics['silhouette_score']
        if sil > 0.7:
            interpretations['silhouette'] = "Excellent clustering (silhouette > 0.7)"
        elif sil > 0.5:
            interpretations['silhouette'] = "Bon clustering (silhouette > 0.5)"
        elif sil > 0.25:
            interpretations['silhouette'] = "Clustering acceptable (silhouette > 0.25)"
        else:
            interpretations['silhouette'] = "Clustering faible (silhouette < 0.25)"
    else:
        interpretations['silhouette'] = "Non calculable (trop peu de clusters)"
    
    # Davies-Bouldin Score (plus bas = mieux)
    if metrics.get('davies_bouldin_score') is not None:
        db = metrics['davies_bouldin_score']
        if db < 0.5:
            interpretations['davies_bouldin'] = "Excellent séparation des clusters (DB < 0.5)"
        elif db < 1.0:
            interpretations['davies_bouldin'] = "Bonne séparation (DB < 1.0)"
        else:
            interpretations['davies_bouldin'] = "Séparation modérée (DB >= 1.0)"
    else:
        interpretations['davies_bouldin'] = "Non calculable"
    
    # Ratio de bruit
    noise_ratio = metrics.get('noise_ratio', 0)
    if noise_ratio < 0.1:
        interpretations['noise'] = "Peu d'anomalies détectées (< 10%)"
    elif noise_ratio < 0.3:
        interpretations['noise'] = "Proportion modérée d'anomalies (10-30%)"
    else:
        interpretations['noise'] = "Beaucoup d'anomalies détectées (> 30%)"
    
    return interpretations

