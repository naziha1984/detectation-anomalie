# Détection d'Anomalies Médicales avec DBSCAN

## 📋 Description du Projet

Ce projet implémente un pipeline complet de détection d'anomalies pour les patients à partir de leurs signes vitaux en utilisant l'algorithme **DBSCAN** (Density-Based Spatial Clustering of Applications with Noise). 

L'objectif est d'identifier automatiquement les patients présentant des signes vitaux anormaux qui nécessitent une attention médicale immédiate.

## 🎯 Pourquoi DBSCAN pour le domaine médical ?

**DBSCAN** est particulièrement adapté à la détection d'anomalies médicales pour plusieurs raisons :

1. **Détection automatique d'anomalies** : DBSCAN identifie naturellement les points isolés (cluster = -1) comme des anomalies, sans nécessiter de labels supervisés.

2. **Robustesse aux outliers** : Contrairement aux algorithmes de clustering comme K-means, DBSCAN ne nécessite pas de connaître à l'avance le nombre de clusters et gère bien les valeurs aberrantes.

3. **Clustering basé sur la densité** : Les patients avec des signes vitaux similaires forment des clusters de densité, tandis que les patients avec des valeurs anormales restent isolés.

4. **Pas d'hypothèse sur la forme des clusters** : DBSCAN peut identifier des clusters de formes arbitraires, ce qui est important pour des données médicales complexes.

5. **Interprétabilité** : Les résultats sont facilement interprétables : les patients normaux sont regroupés en clusters, les anomalies sont isolées.

## 🏗️ Architecture du Projet

```
project/
│── data/
│     ├── patients.csv                    # Données d'entrée
│     ├── patients_with_clusters.csv      # Résultats avec clusters
│     ├── patients_anomalies.csv          # Liste des anomalies
│     ├── summary_report.txt              # Rapport textuel
│     └── report.html                     # Rapport HTML professionnel
│── notebooks/
│     └── eda_dbscan.ipynb                # Analyse exploratoire
│── src/
│     ├── __init__.py
│     ├── config.py                       # Configuration centralisée
│     ├── data_loader.py                  # Chargement des données
│     ├── preprocessing.py                # Nettoyage et normalisation
│     ├── dbscan_model.py                 # Implémentation DBSCAN
│     ├── visualization.py                # Visualisations
│     ├── evaluation.py                   # Métriques d'évaluation
│     ├── optimization.py                # Optimisation automatique
│     └── export_results.py               # Export des résultats
│── tests/
│     ├── test_data_loader.py            # Tests unitaires
│     └── test_preprocessing.py           # Tests preprocessing
│── main.py                               # Script principal avec CLI
│── README.md                             # Documentation
│── requirements.txt                     # Dépendances Python
```

## 📦 Installation

### Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner ou télécharger le projet**

2. **Créer un environnement virtuel (recommandé)**

```bash
python -m venv venv
```

3. **Activer l'environnement virtuel**

   - Sur Windows:
   ```bash
   venv\Scripts\activate
   ```

   - Sur Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

4. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

## 🖥️ Interface Web (NOUVEAU!)

Le projet inclut maintenant une **interface web interactive** avec Streamlit pour visualiser et analyser les données facilement!

### Lancement Rapide

**Windows:**
```bash
run_app.bat
```

**Linux/Mac:**
```bash
streamlit run app.py
```

L'interface s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

### Fonctionnalités de l'Interface

- 📊 **Visualisations interactives** avec Plotly
- ⚙️ **Configuration en temps réel** des paramètres DBSCAN
- 📈 **Métriques en direct** avec interprétations
- 📥 **Upload de fichiers CSV** personnalisés
- 💾 **Téléchargement des résultats** directement depuis l'interface
- 🎨 **Design moderne et responsive**

Consultez `INTERFACE_GUIDE.md` pour plus de détails.

---

## 🚀 Utilisation

### Méthode 1: Exécution du script principal (Recommandé)

**Utilisation de base :**
```bash
python main.py
```

**Options avancées :**
```bash
# Spécifier manuellement les paramètres DBSCAN
python main.py --eps 0.5 --min-samples 5

# Optimiser automatiquement les paramètres
python main.py --optimize

# Utiliser un fichier de données personnalisé
python main.py --data data/mes_donnees.csv

# Changer le répertoire de sortie
python main.py --output-dir results/

# Mode verbose avec plus de détails
python main.py --verbose

# Sans générer les visualisations (plus rapide)
python main.py --no-visualizations

# Voir toutes les options
python main.py --help
```

Le script exécute automatiquement toutes les étapes :
1. Chargement des données
2. Nettoyage et préprocessing
3. Normalisation
4. Calcul de la courbe k-distance (ou optimisation)
5. Application de DBSCAN
6. Évaluation avec métriques (Silhouette, Davies-Bouldin, etc.)
7. Visualisation des résultats
8. Export des résultats (CSV, TXT, HTML)

### Méthode 2: Utilisation du notebook Jupyter

```bash
jupyter notebook notebooks/eda_dbscan.ipynb
```

Le notebook permet une analyse interactive avec possibilité d'ajuster les paramètres et d'explorer les résultats étape par étape.

## 📊 Format des Données d'Entrée

Le fichier `data/patients.csv` doit contenir les colonnes suivantes :

| Colonne | Description | Exemple |
|---------|-------------|---------|
| `patient_id` | Identifiant unique du patient | P0001 |
| `blood_pressure_systolic` | Pression artérielle systolique (mmHg) | 120 |
| `blood_pressure_diastolic` | Pression artérielle diastolique (mmHg) | 80 |
| `temperature_c` | Température corporelle (°C) | 37.0 |
| `heart_rate_bpm` | Fréquence cardiaque (battements/min) | 72 |

## 🔧 Paramètres DBSCAN

### Détermination automatique de `eps`

Le projet calcule automatiquement la courbe **k-distance** pour suggérer une valeur optimale de `eps`. Cette courbe représente la distance au k-ième plus proche voisin pour chaque point.

**Comment interpréter la courbe k-distance :**
- Le "coude" (point d'inflexion) de la courbe indique une bonne valeur pour `eps`
- La médiane des distances k-voisins est souvent un bon point de départ
- Des valeurs trop petites créent trop d'anomalies
- Des valeurs trop grandes regroupent tout en un seul cluster

### Paramètres par défaut

- `eps`: Déterminé automatiquement via la courbe k-distance (médiane)
- `min_samples`: 5 (nombre minimum de points pour former un cluster)

Vous pouvez ajuster ces paramètres dans `main.py` ou dans le notebook.

## 📈 Interprétation des Résultats

### Clusters identifiés

- **Cluster -1** : Patients identifiés comme **anomalies**
  - Signes vitaux s'écartant significativement de la population normale
  - Nécessitent une attention médicale immédiate

- **Clusters 0, 1, 2, ...** : Groupes de patients avec des profils similaires
  - Peuvent représenter différents états de santé
  - Utiles pour la catégorisation et le suivi médical

### Fichiers de sortie

1. **`patients_with_clusters.csv`** : Tous les patients avec leur label de cluster
2. **`patients_anomalies.csv`** : Seulement les patients identifiés comme anomalies
3. **`summary_report.txt`** : Rapport textuel résumant l'analyse
4. **`report.html`** : 🆕 Rapport HTML professionnel avec métriques et statistiques détaillées
5. **Graphiques PNG** : Visualisations sauvegardées dans `data/`
   - `k_distance_curve.png` - Courbe k-distance
   - `clusters_pca.png` - Visualisation 2D des clusters
   - `feature_distributions.png` - Distributions des signes vitaux
   - `cluster_statistics.png` - Statistiques des clusters

## 🔍 Visualisations Générées

1. **Courbe k-distance** : Aide à déterminer le paramètre `eps` optimal
2. **Visualisation 2D des clusters** : Projection PCA montrant les clusters et anomalies
3. **Distributions des features** : Comparaison des signes vitaux entre patients normaux et anomalies
4. **Statistiques des clusters** : Graphiques en barres et camembert

## 📊 Métriques d'Évaluation

Le projet calcule automatiquement plusieurs métriques pour évaluer la qualité du clustering :

- **Silhouette Score** : Mesure la cohésion et la séparation des clusters (plus élevé = mieux)
- **Davies-Bouldin Score** : Mesure la séparation moyenne entre clusters (plus bas = mieux)
- **Calinski-Harabasz Score** : Ratio de variance entre et dans les clusters (plus élevé = mieux)

Ces métriques sont incluses dans le rapport HTML avec des interprétations automatiques.

## ⚙️ Optimisation Automatique

Le projet inclut une fonctionnalité d'optimisation automatique des paramètres DBSCAN :

```bash
python main.py --optimize
```

Cette fonction teste différentes combinaisons de `eps` et `min_samples` et sélectionne les meilleurs paramètres basés sur le Silhouette Score.

## ⚠️ Avertissements et Limitations

1. **Validation médicale requise** : Les résultats doivent être validés par des experts médicaux avant toute décision clinique.

2. **Paramètres à ajuster** : Les paramètres DBSCAN peuvent nécessiter un ajustement selon votre dataset spécifique.

3. **Normalisation importante** : Les données sont normalisées avec StandardScaler pour éviter que certaines features dominent l'analyse.

4. **Interprétation contextuelle** : Les anomalies détectées doivent être interprétées dans le contexte médical approprié.

## 🛠️ Personnalisation

### Modifier les colonnes de features

Créez un fichier de configuration personnalisé ou modifiez `src/config.py` :

```python
from src.config import Config

config = Config()
config.feature_cols = [
    'blood_pressure_systolic',
    'blood_pressure_diastolic',
    'temperature_c',
    'heart_rate_bpm',
    'autre_feature'  # Ajouter vos propres features
]
```

### Ajuster les paramètres DBSCAN

Utilisez les arguments en ligne de commande :

```bash
python main.py --eps 0.5 --min-samples 10
```

Ou modifiez `src/config.py` pour des valeurs par défaut personnalisées.

## 🧪 Tests Unitaires

Le projet inclut des tests unitaires pour valider le fonctionnement :

```bash
# Exécuter tous les tests
python -m pytest tests/

# Exécuter un test spécifique
python -m pytest tests/test_data_loader.py

# Avec couverture de code
python -m pytest tests/ --cov=src
```

## 📚 Références

- [DBSCAN - scikit-learn Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html)
- [Density-Based Clustering - Wikipedia](https://en.wikipedia.org/wiki/DBSCAN)
- Ester, M., Kriegel, H. P., Sander, J., & Xu, X. (1996). A density-based algorithm for discovering clusters in large spatial databases with noise.

## 📝 Licence

Ce projet est fourni à des fins éducatives et de recherche.

## 👤 Auteur

Projet développé pour la détection d'anomalies médicales avec DBSCAN.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

---

**Note importante** : Ce projet est destiné à des fins de recherche et d'éducation. Il ne doit pas être utilisé comme seul outil de diagnostic médical sans validation par des professionnels de santé qualifiés.

