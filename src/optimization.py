"""
Module d'optimisation automatique des paramètres DBSCAN
"""

import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def optimize_dbscan_parameters(X: np.ndarray, 
                                eps_range: tuple = None,
                                min_samples_range: tuple = None,
                                metric: str = 'silhouette') -> dict:
    """
    Optimise automatiquement les paramètres DBSCAN.
    
    Args:
        X: Matrice de features normalisées
        eps_range: Tuple (min, max, step) pour eps. Si None, utilise k-distance
        min_samples_range: Tuple (min, max) pour min_samples
        metric: Métrique à optimiser ('silhouette' ou 'clusters')
        
    Returns:
        Dictionnaire avec les meilleurs paramètres et scores
    """
    logger.info("Optimisation automatique des paramètres DBSCAN")
    
    from src.dbscan_model import compute_k_distance_curve, suggest_eps_from_k_distance
    
    # Déterminer la plage eps si non fournie
    if eps_range is None:
        k_distances = compute_k_distance_curve(X, k=5)
        eps_min = np.percentile(k_distances, 10)
        eps_max = np.percentile(k_distances, 90)
        eps_step = (eps_max - eps_min) / 20
        eps_range = (eps_min, eps_max, eps_step)
        logger.info(f"Plage eps déterminée: {eps_min:.4f} à {eps_max:.4f}")
    
    if min_samples_range is None:
        min_samples_range = (3, 10)
    
    best_score = -np.inf if metric == 'silhouette' else 0
    best_params = None
    results = []
    
    eps_values = np.arange(eps_range[0], eps_range[1], eps_range[2])
    min_samples_values = range(min_samples_range[0], min_samples_range[1] + 1)
    
    logger.info(f"Test de {len(eps_values)} valeurs eps et {len(min_samples_values)} valeurs min_samples")
    
    for eps in eps_values:
        for min_samples in min_samples_values:
            # Appliquer DBSCAN
            dbscan = DBSCAN(eps=eps, min_samples=min_samples)
            labels = dbscan.fit_predict(X)
            
            # Compter les clusters (excluant le bruit)
            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            n_noise = np.sum(labels == -1)
            
            # Éviter les cas extrêmes
            if n_clusters == 0 or n_clusters > len(X) // 2:
                continue
            
            # Calculer le score
            if metric == 'silhouette' and n_clusters >= 2:
                non_noise_mask = labels != -1
                if np.sum(non_noise_mask) > 1:
                    try:
                        score = silhouette_score(X[non_noise_mask], labels[non_noise_mask])
                    except:
                        score = -1
                else:
                    score = -1
            elif metric == 'clusters':
                # Maximiser le nombre de clusters tout en minimisant le bruit
                score = n_clusters - (n_noise / len(X))
            else:
                score = 0
            
            results.append({
                'eps': eps,
                'min_samples': min_samples,
                'n_clusters': n_clusters,
                'n_noise': n_noise,
                'score': score
            })
            
            # Mettre à jour les meilleurs paramètres
            if score > best_score:
                best_score = score
                best_params = {
                    'eps': eps,
                    'min_samples': min_samples,
                    'n_clusters': n_clusters,
                    'n_noise': n_noise,
                    'score': score
                }
    
    logger.info(f"Meilleurs paramètres trouvés:")
    logger.info(f"  eps: {best_params['eps']:.4f}")
    logger.info(f"  min_samples: {best_params['min_samples']}")
    logger.info(f"  Score: {best_params['score']:.4f}")
    logger.info(f"  Clusters: {best_params['n_clusters']}")
    logger.info(f"  Anomalies: {best_params['n_noise']}")
    
    return {
        'best_params': best_params,
        'all_results': results
    }

