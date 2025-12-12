"""
Script principal pour la détection d'anomalies médicales avec DBSCAN
Version améliorée avec interface en ligne de commande et fonctionnalités avancées
"""

import matplotlib
matplotlib.use('Agg')  # Backend non-interactif pour l'exécution en ligne de commande

import argparse
import logging
from pathlib import Path
import numpy as np

from src.config import Config
from src.data_loader import load_patient_data, validate_required_columns
from src.preprocessing import clean_data, prepare_features, normalize_features
from src.dbscan_model import (
    compute_k_distance_curve, 
    plot_k_distance_curve, 
    suggest_eps_from_k_distance,
    apply_dbscan,
    identify_anomalies
)
from src.visualization import (
    plot_clusters_2d,
    plot_feature_distributions,
    plot_cluster_statistics
)
from src.evaluation import evaluate_clustering, interpret_metrics
from src.optimization import optimize_dbscan_parameters
from src.export_results import export_results, generate_summary_report, generate_html_report

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse les arguments de la ligne de commande"""
    parser = argparse.ArgumentParser(
        description='Détection d\'anomalies médicales avec DBSCAN',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python main.py                          # Exécution avec paramètres par défaut
  python main.py --eps 0.5                # Spécifier eps manuellement
  python main.py --optimize               # Optimiser automatiquement les paramètres
  python main.py --data data/custom.csv    # Utiliser un fichier de données personnalisé
        """
    )
    
    parser.add_argument(
        '--data',
        type=str,
        default='data/patients.csv',
        help='Chemin vers le fichier CSV des données patients (défaut: data/patients.csv)'
    )
    
    parser.add_argument(
        '--eps',
        type=float,
        default=None,
        help='Valeur eps pour DBSCAN (défaut: déterminée automatiquement via k-distance)'
    )
    
    parser.add_argument(
        '--min-samples',
        type=int,
        default=5,
        help='Nombre minimum de points pour former un cluster (défaut: 5)'
    )
    
    parser.add_argument(
        '--optimize',
        action='store_true',
        help='Optimiser automatiquement les paramètres DBSCAN'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='data',
        help='Répertoire de sortie pour les résultats (défaut: data)'
    )
    
    parser.add_argument(
        '--no-visualizations',
        action='store_true',
        help='Ne pas générer les visualisations (plus rapide)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Mode verbose avec plus de détails'
    )
    
    return parser.parse_args()


def main():
    """
    Pipeline principal d'analyse DBSCAN pour la détection d'anomalies médicales.
    """
    args = parse_arguments()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("=" * 70)
    logger.info("DÉTECTION D'ANOMALIES MÉDICALES AVEC DBSCAN")
    logger.info("Version Améliorée - Projet Professionnel")
    logger.info("=" * 70)
    
    # Configuration
    config = Config()
    config.data_dir = Path(args.data).parent
    config.output_dir = Path(args.output_dir)
    config.eps = args.eps
    config.min_samples = args.min_samples
    
    # ========== ÉTAPE 1: CHARGEMENT DES DONNÉES ==========
    logger.info("\n[ÉTAPE 1] Chargement des données")
    logger.info("-" * 70)
    
    try:
        df = load_patient_data(args.data)
        validate_required_columns(df, config.required_columns)
    except Exception as e:
        logger.error(f"Erreur lors du chargement: {e}")
        return 1
    
    # ========== ÉTAPE 2: NETTOYAGE DES DONNÉES ==========
    logger.info("\n[ÉTAPE 2] Nettoyage des données")
    logger.info("-" * 70)
    
    df_clean = clean_data(df, patient_id_col=config.patient_id_col)
    
    # ========== ÉTAPE 3: PRÉPARATION DES FEATURES ==========
    logger.info("\n[ÉTAPE 3] Préparation des features")
    logger.info("-" * 70)
    
    X, patient_ids = prepare_features(df_clean, config.feature_cols, config.patient_id_col)
    
    # ========== ÉTAPE 4: NORMALISATION ==========
    logger.info("\n[ÉTAPE 4] Normalisation des features")
    logger.info("-" * 70)
    
    X_scaled, scaler = normalize_features(X)
    
    # ========== ÉTAPE 5: OPTIMISATION OU ANALYSE K-DISTANCE ==========
    if args.optimize:
        logger.info("\n[ÉTAPE 5] Optimisation automatique des paramètres")
        logger.info("-" * 70)
        
        optimization_results = optimize_dbscan_parameters(X_scaled)
        best_params = optimization_results['best_params']
        config.eps = best_params['eps']
        config.min_samples = best_params['min_samples']
        
        logger.info(f"Paramètres optimaux trouvés:")
        logger.info(f"  eps: {config.eps:.4f}")
        logger.info(f"  min_samples: {config.min_samples}")
    else:
        logger.info("\n[ÉTAPE 5] Calcul de la courbe k-distance")
        logger.info("-" * 70)
        
        k_distances = compute_k_distance_curve(
            X_scaled, 
            k=config.min_samples,
            max_samples=config.max_samples_k_distance
        )
        
        if not args.no_visualizations:
            plot_k_distance_curve(
                k_distances, 
                k=config.min_samples, 
                save_path=str(config.output_dir / 'k_distance_curve.png')
            )
        
        # Suggérer eps si non fourni
        if config.eps is None:
            config.eps = suggest_eps_from_k_distance(
                k_distances, 
                percentile=config.k_distance_percentile
            )
            logger.info(f"Valeur eps suggérée: {config.eps:.4f}")
    
    # ========== ÉTAPE 6: APPLICATION DBSCAN ==========
    logger.info("\n[ÉTAPE 6] Application de DBSCAN")
    logger.info("-" * 70)
    logger.info(f"Paramètres: eps={config.eps:.4f}, min_samples={config.min_samples}")
    
    labels, dbscan_model = apply_dbscan(
        X_scaled, 
        eps=config.eps, 
        min_samples=config.min_samples
    )
    
    # ========== ÉTAPE 7: ÉVALUATION ==========
    logger.info("\n[ÉTAPE 7] Évaluation de la qualité du clustering")
    logger.info("-" * 70)
    
    metrics = evaluate_clustering(X_scaled, labels)
    interpretations = interpret_metrics(metrics)
    
    # ========== ÉTAPE 8: IDENTIFICATION DES ANOMALIES ==========
    logger.info("\n[ÉTAPE 8] Identification des anomalies")
    logger.info("-" * 70)
    
    anomaly_ids = identify_anomalies(labels, patient_ids)
    
    # ========== ÉTAPE 9: VISUALISATIONS ==========
    if not args.no_visualizations:
        logger.info("\n[ÉTAPE 9] Génération des visualisations")
        logger.info("-" * 70)
        
        # Visualisation 2D avec PCA
        plot_clusters_2d(
            X_scaled, 
            labels, 
            method='pca', 
            save_path=str(config.output_dir / 'clusters_pca.png')
        )
        
        # Distribution des features
        plot_feature_distributions(
            df_clean, 
            config.feature_cols, 
            labels, 
            save_path=str(config.output_dir / 'feature_distributions.png')
        )
        
        # Statistiques des clusters
        plot_cluster_statistics(
            labels, 
            save_path=str(config.output_dir / 'cluster_statistics.png')
        )
    
    # ========== ÉTAPE 10: EXPORTATION DES RÉSULTATS ==========
    logger.info("\n[ÉTAPE 10] Exportation des résultats")
    logger.info("-" * 70)
    
    output_files = export_results(
        df_clean, 
        labels, 
        config.patient_id_col, 
        output_dir=str(config.output_dir)
    )
    
    # Génération du rapport textuel
    generate_summary_report(
        labels, 
        df_clean, 
        config.feature_cols, 
        output_file=str(config.output_dir / 'summary_report.txt')
    )
    
    # Génération du rapport HTML professionnel
    generate_html_report(
        labels,
        df_clean,
        config.feature_cols,
        metrics,
        interpretations,
        output_file=str(config.output_dir / 'report.html')
    )
    
    # ========== RÉSUMÉ FINAL ==========
    logger.info("\n" + "=" * 70)
    logger.info("✅ ANALYSE TERMINÉE AVEC SUCCÈS")
    logger.info("=" * 70)
    logger.info(f"\n📁 Fichiers générés:")
    logger.info(f"  ✓ {output_files['all_patients']}")
    logger.info(f"  ✓ {output_files['anomalies']}")
    logger.info(f"  ✓ {config.output_dir}/summary_report.txt")
    logger.info(f"  ✓ {config.output_dir}/report.html")
    
    if not args.no_visualizations:
        logger.info(f"  ✓ {config.output_dir}/k_distance_curve.png")
        logger.info(f"  ✓ {config.output_dir}/clusters_pca.png")
        logger.info(f"  ✓ {config.output_dir}/feature_distributions.png")
        logger.info(f"  ✓ {config.output_dir}/cluster_statistics.png")
    
    logger.info(f"\n📊 Résultats:")
    logger.info(f"  • Total patients: {len(labels)}")
    logger.info(f"  • Anomalies détectées: {len(anomaly_ids)} ({100*len(anomaly_ids)/len(labels):.2f}%)")
    logger.info(f"  • Clusters identifiés: {metrics['n_clusters']}")
    
    if metrics.get('silhouette_score') is not None:
        logger.info(f"  • Silhouette Score: {metrics['silhouette_score']:.4f}")
    
    logger.info(f"\n💡 Consultez le rapport HTML: {config.output_dir}/report.html")
    
    return 0


if __name__ == '__main__':
    exit(main())
