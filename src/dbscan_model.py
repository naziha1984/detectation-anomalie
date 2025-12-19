"""
Module DBSCAN pour la détection d'anomalies
"""

import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def compute_k_distance_curve(X: np.ndarray, k: int = 4, max_samples: int = 1000) -> np.ndarray:
    """
    Calcule la courbe k-distance pour déterminer le paramètre eps optimal.
    
    La courbe k-distance représente la distance au k-ième plus proche voisin
    pour chaque point. Le "coude" de cette courbe indique un bon choix pour eps.
    
    Args:
        X: Matrice de features normalisées (n_samples, n_features)
        k: Nombre de voisins à considérer (par défaut 4)
        max_samples: Nombre maximum d'échantillons à utiliser pour le calcul (pour performance)
        
    Returns:
        Array des distances k-voisins triées
    """
    logger.info(f"Calcul de la courbe k-distance (k={k})")
    
    # Sous-échantillonnage si trop de données
    if len(X) > max_samples:
        indices = np.random.choice(len(X), max_samples, replace=False)
        X_sample = X[indices]
        logger.info(f"Sous-échantillonnage à {max_samples} échantillons pour performance")
    else:
        X_sample = X
    
    # Calculer les k+1 plus proches voisins (k+1 car le point lui-même est inclus)
    nbrs = NearestNeighbors(n_neighbors=k+1, algorithm='auto').fit(X_sample)
    distances, indices = nbrs.kneighbors(X_sample)
    
    # Prendre la distance au k-ième voisin (index k car index 0 est le point lui-même)
    k_distances = distances[:, k]
    
    # Trier pour la visualisation
    k_distances_sorted = np.sort(k_distances)[::-1]
    
    logger.info(f"Courbe k-distance calculée: min={k_distances_sorted.min():.4f}, "
                f"max={k_distances_sorted.max():.4f}, median={np.median(k_distances_sorted):.4f}")
    
    return k_distances_sorted


def plot_k_distance_curve(k_distances: np.ndarray, k: int = 4, save_path: str = None) -> None:
    """
    Trace la courbe k-distance pour visualiser le choix optimal de eps.
    
    Args:
        k_distances: Distances k-voisins triées
        k: Nombre de voisins utilisé
        save_path: Chemin pour sauvegarder le graphique (optionnel)
    """
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(k_distances)), k_distances, 'b-', linewidth=2)
    plt.xlabel('Points triés par distance', fontsize=12)
    plt.ylabel(f'Distance au {k}-ième voisin', fontsize=12)
    plt.title(f'Courbe k-distance (k={k}) pour déterminer eps optimal', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Ajouter une ligne pour la médiane
    median_dist = np.median(k_distances)
    plt.axhline(y=median_dist, color='r', linestyle='--', 
                label=f'Médiane: {median_dist:.4f}')
    plt.legend()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Graphique sauvegardé: {save_path}")
    
    plt.close()


def suggest_eps_from_k_distance(k_distances: np.ndarray, percentile: float = 50.0) -> float:
    """
    Suggère une valeur eps basée sur la courbe k-distance.
    
    Args:
        k_distances: Distances k-voisins triées
        percentile: Percentile à utiliser pour suggérer eps (défaut: 50 = médiane)
        
    Returns:
        Valeur suggérée pour eps
    """
    suggested_eps = np.percentile(k_distances, percentile)
    logger.info(f"Valeur eps suggérée (percentile {percentile}): {suggested_eps:.4f}")
    return suggested_eps


def apply_dbscan(X: np.ndarray, eps: float, min_samples: int = 5) -> tuple:
    """
    Applique l'algorithme DBSCAN sur les données.
    
    DBSCAN identifie les clusters de densité et marque les points isolés
    comme anomalies (cluster = -1).
    
    Args:
        X: Matrice de features normalisées (n_samples, n_features)
        eps: Rayon de voisinage pour DBSCAN
        min_samples: Nombre minimum de points pour former un cluster
        
    Returns:
        Tuple (labels, model) où labels sont les labels de cluster (-1 = anomalie)
    """
    logger.info(f"Application de DBSCAN: eps={eps:.4f}, min_samples={min_samples}")
    
    model = DBSCAN(eps=eps, min_samples=min_samples, metric='euclidean')
    labels = model.fit_predict(X)
    
    # Statistiques
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise = list(labels).count(-1)
    n_normal = len(labels) - n_noise
    
    logger.info(f"DBSCAN terminé:")
    logger.info(f"  - Clusters identifiés: {n_clusters}")
    logger.info(f"  - Points normaux: {n_normal} ({100*n_normal/len(labels):.2f}%)")
    logger.info(f"  - Anomalies détectées: {n_noise} ({100*n_noise/len(labels):.2f}%)")
    
    return labels, model


def identify_anomalies(labels: np.ndarray, patient_ids: np.ndarray) -> np.ndarray:
    """
    Identifie les patients considérés comme anomalies (cluster = -1).
    
    Args:
        labels: Labels de cluster de DBSCAN
        patient_ids: IDs des patients
        
    Returns:
        Array des IDs patients identifiés comme anomalies
    """
    anomaly_mask = labels == -1
    anomaly_ids = patient_ids[anomaly_mask]
    
    logger.info(f"Anomalies identifiées: {len(anomaly_ids)} patients")
    
    return anomaly_ids

