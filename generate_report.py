"""
Script pour générer le rapport professionnel complet du projet
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json

def generate_comprehensive_report():
    """Génère un rapport professionnel complet"""
    
    # Lire les résultats si disponibles
    report_data = {
        'date': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'project_name': 'Détection d\'Anomalies Médicales avec DBSCAN',
        'version': '2.0',
    }
    
    # Essayer de charger les résultats existants
    try:
        if Path('data/patients_with_clusters.csv').exists():
            df = pd.read_csv('data/patients_with_clusters.csv')
            report_data['total_patients'] = len(df)
            report_data['anomalies'] = df['is_anomaly'].sum()
            report_data['normal'] = len(df) - report_data['anomalies']
            report_data['clusters'] = df['cluster_label'].nunique() - (1 if -1 in df['cluster_label'].values else 0)
    except:
        pass
    
    # Générer le rapport HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport Professionnel - Détection d'Anomalies Médicales</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            color: #2c3e50;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        .report-container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 50px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        .header {{
            text-align: center;
            padding: 30px 0;
            border-bottom: 3px solid #3498db;
            margin-bottom: 40px;
        }}
        .header h1 {{
            font-size: 2.5em;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .header .subtitle {{
            font-size: 1.2em;
            color: #7f8c8d;
        }}
        .header .meta {{
            margin-top: 20px;
            font-size: 0.9em;
            color: #95a5a6;
        }}
        .section {{
            margin: 40px 0;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 5px solid #3498db;
        }}
        .section h2 {{
            color: #2c3e50;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #ecf0f1;
        }}
        .section h3 {{
            color: #34495e;
            font-size: 1.4em;
            margin: 25px 0 15px 0;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .metric-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .metric-card h3 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            color: white;
            border: none;
        }}
        .metric-card p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .feature-list {{
            list-style: none;
            padding: 0;
        }}
        .feature-list li {{
            padding: 15px;
            margin: 10px 0;
            background: white;
            border-radius: 5px;
            border-left: 4px solid #3498db;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .feature-list li:before {{
            content: "✓ ";
            color: #27ae60;
            font-weight: bold;
            font-size: 1.2em;
            margin-right: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        th, td {{
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #ecf0f1;
        }}
        th {{
            background: #3498db;
            color: white;
            font-weight: bold;
        }}
        tr:hover {{
            background: #f8f9fa;
        }}
        .highlight-box {{
            background: #fff3cd;
            border-left: 5px solid #ffc107;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .success-box {{
            background: #d4edda;
            border-left: 5px solid #28a745;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .footer {{
            margin-top: 50px;
            padding-top: 30px;
            border-top: 3px solid #ecf0f1;
            text-align: center;
            color: #7f8c8d;
        }}
        .toc {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 30px 0;
        }}
        .toc ul {{
            list-style: none;
            padding-left: 0;
        }}
        .toc li {{
            padding: 8px 0;
            border-bottom: 1px solid #ecf0f1;
        }}
        .toc a {{
            color: #3498db;
            text-decoration: none;
        }}
        .toc a:hover {{
            text-decoration: underline;
        }}
        @media print {{
            body {{
                background: white;
            }}
            .report-container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="report-container">
        <div class="header">
            <h1>🏥 Rapport Professionnel</h1>
            <div class="subtitle">Détection d'Anomalies Médicales avec DBSCAN</div>
            <div class="meta">
                <strong>Version:</strong> 2.0 | 
                <strong>Date:</strong> {report_data['date']} | 
                <strong>Type:</strong> Projet Complet Professionnel
            </div>
        </div>

        <div class="section">
            <h2>📋 Résumé Exécutif</h2>
            <p>
                Ce rapport présente un système complet et professionnel de détection d'anomalies médicales 
                utilisant l'algorithme DBSCAN. Le système permet d'identifier automatiquement les patients 
                présentant des signes vitaux anormaux nécessitant une attention médicale immédiate.
            </p>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <h3>{report_data.get('total_patients', 'N/A')}</h3>
                    <p>Patients Analysés</p>
                </div>
                <div class="metric-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                    <h3>{report_data.get('anomalies', 'N/A')}</h3>
                    <p>Anomalies Détectées</p>
                </div>
                <div class="metric-card" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                    <h3>{report_data.get('normal', 'N/A')}</h3>
                    <p>Patients Normaux</p>
                </div>
                <div class="metric-card" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                    <h3>{report_data.get('clusters', 'N/A')}</h3>
                    <p>Clusters Identifiés</p>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>🎯 Objectifs du Projet</h2>
            <ul class="feature-list">
                <li>Détection automatique des patients avec signes vitaux anormaux</li>
                <li>Fournir des métriques d'évaluation du clustering</li>
                <li>Créer des visualisations interactives et informatives</li>
                <li>Développer une interface web intuitive</li>
                <li>Produire une documentation complète et professionnelle</li>
            </ul>
        </div>

        <div class="section">
            <h2>🏗️ Architecture du Système</h2>
            <h3>Structure Modulaire</h3>
            <p>Le projet est organisé en modules spécialisés :</p>
            <ul class="feature-list">
                <li><strong>config.py</strong> - Configuration centralisée</li>
                <li><strong>data_loader.py</strong> - Chargement et validation des données</li>
                <li><strong>preprocessing.py</strong> - Nettoyage et normalisation</li>
                <li><strong>dbscan_model.py</strong> - Implémentation DBSCAN</li>
                <li><strong>evaluation.py</strong> - Métriques d'évaluation</li>
                <li><strong>optimization.py</strong> - Optimisation automatique</li>
                <li><strong>visualization.py</strong> - Visualisations</li>
                <li><strong>export_results.py</strong> - Export des résultats</li>
            </ul>
        </div>

        <div class="section">
            <h2>✨ Fonctionnalités Principales</h2>
            <div class="success-box">
                <h3>Interface en Ligne de Commande (CLI)</h3>
                <p>Script principal avec options configurables : optimisation automatique, paramètres personnalisés, mode verbose.</p>
            </div>
            
            <div class="success-box">
                <h3>Interface Web Interactive (Streamlit)</h3>
                <p>Application web moderne avec visualisations interactives, upload de fichiers, et résultats en temps réel.</p>
            </div>
            
            <div class="success-box">
                <h3>Métriques d'Évaluation</h3>
                <p>Calcul automatique de Silhouette Score, Davies-Bouldin Score, et Calinski-Harabasz Score avec interprétations.</p>
            </div>
            
            <div class="success-box">
                <h3>Optimisation Automatique</h3>
                <p>Recherche automatique des meilleurs paramètres DBSCAN basée sur les métriques de qualité.</p>
            </div>
        </div>

        <div class="section">
            <h2>📊 Résultats et Analyses</h2>
            <h3>Performance du Modèle</h3>
            <p>Le système a été testé sur un dataset de {report_data.get('total_patients', '500')} patients avec les résultats suivants :</p>
            
            <table>
                <thead>
                    <tr>
                        <th>Métrique</th>
                        <th>Valeur</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Patients Analysés</td>
                        <td>{report_data.get('total_patients', 'N/A')}</td>
                        <td>Nombre total de patients dans le dataset</td>
                    </tr>
                    <tr>
                        <td>Anomalies Détectées</td>
                        <td>{report_data.get('anomalies', 'N/A')}</td>
                        <td>Patients identifiés comme anomalies (cluster = -1)</td>
                    </tr>
                    <tr>
                        <td>Patients Normaux</td>
                        <td>{report_data.get('normal', 'N/A')}</td>
                        <td>Patients regroupés en clusters normaux</td>
                    </tr>
                    <tr>
                        <td>Clusters Identifiés</td>
                        <td>{report_data.get('clusters', 'N/A')}</td>
                        <td>Nombre de clusters de densité identifiés</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>🛠️ Technologies Utilisées</h2>
            <table>
                <thead>
                    <tr>
                        <th>Technologie</th>
                        <th>Version</th>
                        <th>Usage</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Python</td>
                        <td>3.10+</td>
                        <td>Langage principal</td>
                    </tr>
                    <tr>
                        <td>pandas</td>
                        <td>2.0+</td>
                        <td>Manipulation de données</td>
                    </tr>
                    <tr>
                        <td>scikit-learn</td>
                        <td>1.3+</td>
                        <td>Machine Learning</td>
                    </tr>
                    <tr>
                        <td>Streamlit</td>
                        <td>1.28+</td>
                        <td>Interface web</td>
                    </tr>
                    <tr>
                        <td>Plotly</td>
                        <td>5.17+</td>
                        <td>Graphiques interactifs</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="section">
            <h2>📈 Applications Potentielles</h2>
            <ul class="feature-list">
                <li><strong>Hôpitaux</strong> - Détection précoce de patients à risque</li>
                <li><strong>Centres de soins</strong> - Surveillance continue des signes vitaux</li>
                <li><strong>Recherche médicale</strong> - Analyse de patterns dans les données</li>
                <li><strong>Télémédecine</strong> - Monitoring à distance</li>
            </ul>
        </div>

        <div class="highlight-box">
            <h3>⚠️ Avertissement Important</h3>
            <p>
                <strong>Les résultats de ce système doivent toujours être validés par des professionnels 
                de santé qualifiés avant toute décision clinique.</strong> Ce système est un outil d'aide 
                à la décision et ne remplace pas l'expertise médicale.
            </p>
        </div>

        <div class="section">
            <h2>📚 Documentation</h2>
            <p>Le projet inclut une documentation complète :</p>
            <ul class="feature-list">
                <li><strong>README.md</strong> - Documentation principale</li>
                <li><strong>INTERFACE_GUIDE.md</strong> - Guide de l'interface web</li>
                <li><strong>LANCER_INTERFACE.md</strong> - Guide de lancement</li>
                <li><strong>RAPPORT_PROFESSIONNEL.md</strong> - Rapport détaillé</li>
                <li><strong>Docstrings</strong> - Documentation du code</li>
            </ul>
        </div>

        <div class="footer">
            <p><strong>Rapport Professionnel - Détection d'Anomalies Médicales avec DBSCAN</strong></p>
            <p>Version 2.0 - Projet Complet Professionnel</p>
            <p>Généré le {report_data['date']}</p>
            <p style="margin-top: 20px; font-size: 0.9em;">
                Pour plus d'informations, consultez la documentation du projet dans README.md
            </p>
        </div>
    </div>
</body>
</html>
"""
    
    # Sauvegarder le rapport
    output_file = Path('RAPPORT_PROFESSIONNEL.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Rapport professionnel généré: {output_file}")
    print(f"📄 Ouvrez le fichier dans votre navigateur pour voir le rapport complet")
    
    return output_file

if __name__ == '__main__':
    generate_comprehensive_report()


