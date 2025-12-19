"""
Module de visualisation des résultats DBSCAN
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)


def plot_clusters_2d(X: np.ndarray, labels: np.ndarray, 
                     method: str = 'pca', save_path: str = None) -> None:
    """
    Visualise les clusters DBSCAN en 2D en utilisant PCA ou t-SNE.
    
    Args:
        X: Matrice de features normalisées (n_samples, n_features)
        labels: Labels de cluster de DBSCAN
        method: Méthode de réduction de dimension ('pca' ou 'tsne')
        save_path: Chemin pour sauvegarder le graphique (optionnel)
    """
    logger.info(f"Visualisation 2D avec {method.upper()}")
    
    # Réduction de dimension
    if method.lower() == 'pca':
        reducer = PCA(n_components=2, random_state=42)
        X_reduced = reducer.fit_transform(X)
        xlabel = f'PC1 (Variance expliquée: {reducer.explained_variance_ratio_[0]:.2%})'
        ylabel = f'PC2 (Variance expliquée: {reducer.explained_variance_ratio_[1]:.2%})'
    elif method.lower() == 'tsne':
        logger.info("Calcul t-SNE (peut prendre du temps...)")
        reducer = TSNE(n_components=2, random_state=42, perplexity=30)
        X_reduced = reducer.fit_transform(X)
        xlabel = 't-SNE Dimension 1'
        ylabel = 't-SNE Dimension 2'
    else:
        raise ValueError("method doit être 'pca' ou 'tsne'")
    
    # Créer la figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Obtenir les clusters uniques
    unique_labels = set(labels)
    n_clusters = len(unique_labels) - (1 if -1 in unique_labels else 0)
    
    # Couleurs pour les clusters
    colors = plt.cm.Spectral(np.linspace(0, 1, n_clusters))
    
    # Tracer chaque cluster
    for k, col in zip(unique_labels, colors if -1 not in unique_labels else 
                      [plt.cm.gray(0.5)] + list(colors)):
        if k == -1:
            # Anomalies en noir
            mask = labels == k
            ax.scatter(X_reduced[mask, 0], X_reduced[mask, 1], 
                      c='black', marker='x', s=100, 
                      label=f'Anomalies ({np.sum(mask)})', 
                      alpha=0.8, linewidths=2)
        else:
            mask = labels == k
            ax.scatter(X_reduced[mask, 0], X_reduced[mask, 1], 
                      c=[col], marker='o', s=50, 
                      label=f'Cluster {k} ({np.sum(mask)})', 
                      alpha=0.6)
    
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title('Visualisation des clusters DBSCAN', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Graphique sauvegardé: {save_path}")
    
    plt.close()


def plot_feature_distributions(df, feature_cols: list, labels: np.ndarray, 
                               save_path: str = None) -> None:
    """
    Visualise la distribution des features par cluster.
    
    Args:
        df: DataFrame original avec les features
        feature_cols: Liste des colonnes de features
        labels: Labels de cluster de DBSCAN
        save_path: Chemin pour sauvegarder le graphique (optionnel)
    """
    logger.info("Visualisation des distributions de features")
    
    n_features = len(feature_cols)
    fig, axes = plt.subplots(2, (n_features + 1) // 2, figsize=(15, 10))
    axes = axes.flatten() if n_features > 1 else [axes]
    
    for idx, col in enumerate(feature_cols):
        ax = axes[idx]
        
        # Séparer anomalies et normaux
        anomaly_mask = labels == -1
        normal_mask = ~anomaly_mask
        
        ax.hist(df.loc[normal_mask, col].values, bins=30, alpha=0.6, 
               label='Patients normaux', color='blue', density=True)
        ax.hist(df.loc[anomaly_mask, col].values, bins=30, alpha=0.8, 
               label='Anomalies', color='red', density=True)
        
        ax.set_xlabel(col, fontsize=10)
        ax.set_ylabel('Densité', fontsize=10)
        ax.set_title(f'Distribution: {col}', fontsize=11, fontweight='bold')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)
    
    # Masquer les axes non utilisés
    for idx in range(n_features, len(axes)):
        axes[idx].axis('off')
    
    plt.suptitle('Distribution des signes vitaux: Normaux vs Anomalies', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Graphique sauvegardé: {save_path}")
    
    plt.close()


def plot_cluster_statistics(labels: np.ndarray, save_path: str = None) -> None:
    """
    Visualise les statistiques des clusters.
    
    Args:
        labels: Labels de cluster de DBSCAN
        save_path: Chemin pour sauvegarder le graphique (optionnel)
    """
    logger.info("Visualisation des statistiques de clusters")
    
    unique_labels, counts = np.unique(labels, return_counts=True)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Graphique en barres
    colors = ['black' if label == -1 else plt.cm.Spectral(i/len(unique_labels)) 
              for i, label in enumerate(unique_labels)]
    bars = ax1.bar(range(len(unique_labels)), counts, color=colors, alpha=0.7)
    ax1.set_xticks(range(len(unique_labels)))
    ax1.set_xticklabels([f'Cluster {l}' if l != -1 else 'Anomalies' 
                         for l in unique_labels], rotation=45, ha='right')
    ax1.set_ylabel('Nombre de patients', fontsize=11)
    ax1.set_title('Nombre de patients par cluster', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Ajouter les valeurs sur les barres
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=9)
    
    # Graphique en camembert
    labels_pie = [f'Cluster {l}' if l != -1 else 'Anomalies' for l in unique_labels]
    ax2.pie(counts, labels=labels_pie, autopct='%1.1f%%', 
           colors=colors, startangle=90)
    ax2.set_title('Répartition des patients', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        logger.info(f"Graphique sauvegardé: {save_path}")
    
    plt.close()

