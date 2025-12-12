"""
Module d'exportation des résultats
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def export_results(df: pd.DataFrame, labels: np.ndarray, 
                   patient_id_col: str, output_dir: str = 'data') -> dict:
    """
    Exporte les résultats de l'analyse DBSCAN en fichiers CSV.
    
    Args:
        df: DataFrame original avec les données patients
        labels: Labels de cluster de DBSCAN
        patient_id_col: Nom de la colonne ID patient
        output_dir: Répertoire de sortie pour les fichiers
        
    Returns:
        Dictionnaire avec les chemins des fichiers créés
    """
    logger.info("Exportation des résultats")
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Créer une copie du DataFrame avec les labels
    df_results = df.copy()
    df_results['cluster_label'] = labels
    df_results['is_anomaly'] = (labels == -1)
    
    # Fichier 1: Tous les patients avec leurs clusters
    output_file_all = output_path / 'patients_with_clusters.csv'
    df_results.to_csv(output_file_all, index=False)
    logger.info(f"Fichier créé: {output_file_all} ({len(df_results)} patients)")
    
    # Fichier 2: Seulement les anomalies
    df_anomalies = df_results[df_results['is_anomaly']].copy()
    output_file_anomalies = output_path / 'patients_anomalies.csv'
    df_anomalies.to_csv(output_file_anomalies, index=False)
    logger.info(f"Fichier créé: {output_file_anomalies} ({len(df_anomalies)} anomalies)")
    
    return {
        'all_patients': str(output_file_all),
        'anomalies': str(output_file_anomalies)
    }


def generate_summary_report(labels: np.ndarray, df: pd.DataFrame, 
                            feature_cols: list, output_file: str = 'data/summary_report.txt') -> None:
    """
    Génère un rapport textuel résumant l'analyse.
    
    Args:
        labels: Labels de cluster de DBSCAN
        df: DataFrame original
        feature_cols: Liste des colonnes de features
        output_file: Chemin du fichier de rapport
    """
    logger.info("Génération du rapport de synthèse")
    
    output_path = Path(output_file)
    output_path.parent.mkdir(exist_ok=True)
    
    n_total = len(labels)
    n_anomalies = np.sum(labels == -1)
    n_normal = n_total - n_anomalies
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("RAPPORT D'ANALYSE DBSCAN - DÉTECTION D'ANOMALIES MÉDICALES\n")
        f.write("=" * 70 + "\n\n")
        
        f.write("RÉSUMÉ GÉNÉRAL\n")
        f.write("-" * 70 + "\n")
        f.write(f"Nombre total de patients analysés: {n_total}\n")
        f.write(f"Patients normaux (clusters): {n_normal} ({100*n_normal/n_total:.2f}%)\n")
        f.write(f"Anomalies détectées: {n_anomalies} ({100*n_anomalies/n_total:.2f}%)\n")
        f.write(f"Nombre de clusters identifiés: {n_clusters}\n\n")
        
        f.write("STATISTIQUES DES ANOMALIES\n")
        f.write("-" * 70 + "\n")
        anomaly_mask = labels == -1
        if n_anomalies > 0:
            for col in feature_cols:
                if col in df.columns:
                    mean_val = df.loc[anomaly_mask, col].mean()
                    std_val = df.loc[anomaly_mask, col].std()
                    f.write(f"{col}: moyenne={mean_val:.2f}, écart-type={std_val:.2f}\n")
        f.write("\n")
        
        f.write("INTERPRÉTATION\n")
        f.write("-" * 70 + "\n")
        f.write("Les patients marqués comme anomalies (cluster = -1) présentent des\n")
        f.write("signes vitaux qui s'écartent significativement de la population normale.\n")
        f.write("Ces patients nécessitent une attention médicale immédiate.\n\n")
        
        f.write("Les clusters identifiés représentent des groupes de patients avec\n")
        f.write("des profils de signes vitaux similaires, ce qui peut aider à\n")
        f.write("la catégorisation et au suivi médical.\n")
    
    logger.info(f"Rapport sauvegardé: {output_path}")


def generate_html_report(labels: np.ndarray, df: pd.DataFrame, 
                         feature_cols: list, metrics: dict,
                         interpretations: dict, output_file: str = 'data/report.html') -> None:
    """
    Génère un rapport HTML professionnel avec toutes les informations.
    
    Args:
        labels: Labels de cluster de DBSCAN
        df: DataFrame original
        feature_cols: Liste des colonnes de features
        metrics: Dictionnaire de métriques d'évaluation
        interpretations: Dictionnaire d'interprétations
        output_file: Chemin du fichier HTML
    """
    logger.info("Génération du rapport HTML")
    
    output_path = Path(output_file)
    output_path.parent.mkdir(exist_ok=True)
    
    n_total = len(labels)
    n_anomalies = np.sum(labels == -1)
    n_normal = n_total - n_anomalies
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    anomaly_mask = labels == -1
    
    # Statistiques des anomalies
    anomaly_stats = {}
    if n_anomalies > 0:
        for col in feature_cols:
            if col in df.columns:
                anomaly_stats[col] = {
                    'mean': df.loc[anomaly_mask, col].mean(),
                    'std': df.loc[anomaly_mask, col].std(),
                    'min': df.loc[anomaly_mask, col].min(),
                    'max': df.loc[anomaly_mask, col].max()
                }
    
    # Statistiques des clusters normaux
    normal_stats = {}
    if n_normal > 0:
        normal_mask = ~anomaly_mask
        for col in feature_cols:
            if col in df.columns:
                normal_stats[col] = {
                    'mean': df.loc[normal_mask, col].mean(),
                    'std': df.loc[normal_mask, col].std(),
                    'min': df.loc[normal_mask, col].min(),
                    'max': df.loc[normal_mask, col].max()
                }
    
    # Formater les métriques pour l'affichage
    silhouette_str = f"{metrics.get('silhouette_score'):.4f}" if metrics.get('silhouette_score') is not None else 'N/A'
    db_str = f"{metrics.get('davies_bouldin_score'):.4f}" if metrics.get('davies_bouldin_score') is not None else 'N/A'
    ch_str = f"{metrics.get('calinski_harabasz_score'):.2f}" if metrics.get('calinski_harabasz_score') is not None else 'N/A'
    
    html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport d'Analyse DBSCAN - Détection d'Anomalies Médicales</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 4px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            margin-bottom: 15px;
            border-left: 4px solid #3498db;
            padding-left: 15px;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .summary-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .summary-card h3 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .summary-card p {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
        .anomaly-card {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}
        .normal-card {{
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        }}
        .cluster-card {{
            background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #3498db;
            color: white;
            font-weight: bold;
        }}
        tr:hover {{
            background: #f5f5f5;
        }}
        .metric-box {{
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }}
        .metric-box strong {{
            color: #2c3e50;
        }}
        .interpretation {{
            background: #e8f5e9;
            padding: 15px;
            border-left: 4px solid #4caf50;
            margin: 10px 0;
        }}
        .warning {{
            background: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin: 10px 0;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            text-align: center;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        .chart-placeholder {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            text-align: center;
            color: #6c757d;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔬 Rapport d'Analyse DBSCAN - Détection d'Anomalies Médicales</h1>
        
        <p><strong>Date d'analyse:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        
        <h2>📊 Résumé Exécutif</h2>
        <div class="summary-grid">
            <div class="summary-card">
                <h3>{n_total}</h3>
                <p>Patients Analysés</p>
            </div>
            <div class="summary-card anomaly-card">
                <h3>{n_anomalies}</h3>
                <p>Anomalies Détectées<br>({100*n_anomalies/n_total:.1f}%)</p>
            </div>
            <div class="summary-card normal-card">
                <h3>{n_normal}</h3>
                <p>Patients Normaux<br>({100*n_normal/n_total:.1f}%)</p>
            </div>
            <div class="summary-card cluster-card">
                <h3>{n_clusters}</h3>
                <p>Clusters Identifiés</p>
            </div>
        </div>
        
        <h2>📈 Métriques d'Évaluation</h2>
        <div class="metric-box">
            <strong>Silhouette Score:</strong> {silhouette_str}<br>
            <small>{interpretations.get('silhouette', '')}</small>
        </div>
        <div class="metric-box">
            <strong>Davies-Bouldin Score:</strong> {db_str}<br>
            <small>{interpretations.get('davies_bouldin', '')}</small>
        </div>
        <div class="metric-box">
            <strong>Calinski-Harabasz Score:</strong> {ch_str}
        </div>
        <div class="interpretation">
            <strong>Interprétation du ratio d'anomalies:</strong> {interpretations.get('noise', '')}
        </div>
        
        <h2>🏥 Statistiques des Signes Vitaux - Patients Normaux</h2>
        <table>
            <thead>
                <tr>
                    <th>Signe Vital</th>
                    <th>Moyenne</th>
                    <th>Écart-type</th>
                    <th>Min</th>
                    <th>Max</th>
                </tr>
            </thead>
            <tbody>
"""
    
    for col in feature_cols:
        if col in normal_stats:
            stats = normal_stats[col]
            html_content += f"""
                <tr>
                    <td><strong>{col}</strong></td>
                    <td>{stats['mean']:.2f}</td>
                    <td>{stats['std']:.2f}</td>
                    <td>{stats['min']:.2f}</td>
                    <td>{stats['max']:.2f}</td>
                </tr>
"""
    
    html_content += """
            </tbody>
        </table>
        
        <h2>⚠️ Statistiques des Signes Vitaux - Anomalies</h2>
        <table>
            <thead>
                <tr>
                    <th>Signe Vital</th>
                    <th>Moyenne</th>
                    <th>Écart-type</th>
                    <th>Min</th>
                    <th>Max</th>
                </tr>
            </thead>
            <tbody>
"""
    
    for col in feature_cols:
        if col in anomaly_stats:
            stats = anomaly_stats[col]
            html_content += f"""
                <tr>
                    <td><strong>{col}</strong></td>
                    <td>{stats['mean']:.2f}</td>
                    <td>{stats['std']:.2f}</td>
                    <td>{stats['min']:.2f}</td>
                    <td>{stats['max']:.2f}</td>
                </tr>
"""
    
    html_content += f"""
            </tbody>
        </table>
        
        <h2>📋 Visualisations</h2>
        <div class="chart-placeholder">
            <p>📊 Les graphiques suivants sont disponibles dans le dossier data/:</p>
            <ul style="text-align: left; display: inline-block;">
                <li>k_distance_curve.png - Courbe k-distance pour déterminer eps</li>
                <li>clusters_pca.png - Visualisation 2D des clusters (PCA)</li>
                <li>feature_distributions.png - Distributions des signes vitaux</li>
                <li>cluster_statistics.png - Statistiques des clusters</li>
            </ul>
        </div>
        
        <h2>💡 Recommandations</h2>
        <div class="warning">
            <strong>⚠️ Attention Médicale Requise:</strong><br>
            Les {n_anomalies} patients identifiés comme anomalies nécessitent une évaluation médicale immédiate.
            Leurs signes vitaux s'écartent significativement de la population normale et peuvent indiquer
            des conditions critiques nécessitant une intervention rapide.
        </div>
        
        <div class="interpretation">
            <strong>✅ Actions Recommandées:</strong><br>
            <ul style="margin-left: 20px; margin-top: 10px;">
                <li>Examiner manuellement chaque patient identifié comme anomalie</li>
                <li>Valider les résultats avec des experts médicaux</li>
                <li>Considérer les clusters identifiés pour la catégorisation des patients</li>
                <li>Surveiller les tendances dans les données au fil du temps</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>Rapport généré automatiquement par le système de détection d'anomalies DBSCAN</p>
            <p>Pour toute question, consultez la documentation du projet</p>
        </div>
    </div>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    logger.info(f"Rapport HTML sauvegardé: {output_path}")
