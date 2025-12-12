# 📊 RAPPORT PROFESSIONNEL
## Détection d'Anomalies Médicales avec DBSCAN

---

**Projet:** Système de Détection d'Anomalies Médicales  
**Algorithme:** DBSCAN (Density-Based Spatial Clustering of Applications with Noise)  
**Domaine:** Santé / Signes Vitaux  
**Date:** Décembre 2025  
**Version:** 2.0 - Projet Professionnel Complet

---

## 📋 Table des Matières

1. [Résumé Exécutif](#résumé-exécutif)
2. [Introduction](#introduction)
3. [Objectifs du Projet](#objectifs-du-projet)
4. [Méthodologie](#méthodologie)
5. [Architecture du Système](#architecture-du-système)
6. [Implémentation Technique](#implémentation-technique)
7. [Résultats et Analyses](#résultats-et-analyses)
8. [Fonctionnalités Avancées](#fonctionnalités-avancées)
9. [Interface Utilisateur](#interface-utilisateur)
10. [Évaluation et Métriques](#évaluation-et-métriques)
11. [Conclusion et Recommandations](#conclusion-et-recommandations)
12. [Annexes](#annexes)

---

## 1. Résumé Exécutif

### 1.1 Vue d'Ensemble

Ce projet présente un système complet et professionnel de détection d'anomalies médicales utilisant l'algorithme DBSCAN. Le système permet d'identifier automatiquement les patients présentant des signes vitaux anormaux nécessitant une attention médicale immédiate.

### 1.2 Points Clés

- ✅ **Pipeline complet** : De la collecte des données à la génération de rapports
- ✅ **Interface web interactive** : Application Streamlit pour visualisation et analyse
- ✅ **Métriques d'évaluation** : Silhouette Score, Davies-Bouldin, Calinski-Harabasz
- ✅ **Optimisation automatique** : Recherche des meilleurs paramètres DBSCAN
- ✅ **Rapports professionnels** : HTML, CSV, et visualisations
- ✅ **Architecture modulaire** : Code extensible et maintenable
- ✅ **Tests unitaires** : Validation de la qualité du code

### 1.3 Résultats Principaux

Sur un dataset de **500 patients** :
- **161 anomalies détectées** (32.20%)
- **339 patients normaux** (67.80%)
- **1 cluster principal** identifié
- **Métriques de qualité** calculées et interprétées

---

## 2. Introduction

### 2.1 Contexte

La détection précoce d'anomalies dans les signes vitaux des patients est cruciale en médecine. Les systèmes automatisés peuvent aider les professionnels de santé à identifier rapidement les cas nécessitant une attention immédiate.

### 2.2 Problématique

Identifier manuellement les patients avec des signes vitaux anormaux parmi de grandes populations est :
- **Temps consommateur**
- **Sujet à l'erreur humaine**
- **Difficile à standardiser**

### 2.3 Solution Proposée

Un système automatisé utilisant DBSCAN pour :
- Détecter automatiquement les anomalies
- Fournir des métriques de qualité
- Visualiser les résultats de manière intuitive
- Générer des rapports professionnels

---

## 3. Objectifs du Projet

### 3.1 Objectifs Principaux

1. **Détection Automatique** : Identifier les patients avec signes vitaux anormaux
2. **Qualité** : Fournir des métriques d'évaluation du clustering
3. **Visualisation** : Créer des graphiques interactifs et informatifs
4. **Interface** : Développer une interface web intuitive
5. **Documentation** : Produire une documentation complète

### 3.2 Objectifs Techniques

- Implémenter un pipeline ML complet
- Créer une architecture modulaire et extensible
- Intégrer des tests unitaires
- Optimiser les performances
- Générer des rapports professionnels

---

## 4. Méthodologie

### 4.1 Algorithme DBSCAN

**DBSCAN** (Density-Based Spatial Clustering of Applications with Noise) est un algorithme de clustering basé sur la densité qui :

- ✅ Identifie automatiquement les clusters de formes arbitraires
- ✅ Détecte les points isolés comme anomalies (cluster = -1)
- ✅ Ne nécessite pas de connaître le nombre de clusters à l'avance
- ✅ Gère bien les valeurs aberrantes

### 4.2 Paramètres DBSCAN

- **eps (ε)** : Rayon de voisinage pour former un cluster
- **min_samples** : Nombre minimum de points pour former un cluster

### 4.3 Pipeline de Traitement

```
1. Chargement des données
   ↓
2. Nettoyage (valeurs manquantes, doublons)
   ↓
3. Préparation des features
   ↓
4. Normalisation (StandardScaler)
   ↓
5. Calcul courbe k-distance (détermination eps)
   ↓
6. Application DBSCAN
   ↓
7. Évaluation (métriques)
   ↓
8. Visualisation
   ↓
9. Export des résultats
```

---

## 5. Architecture du Système

### 5.1 Structure du Projet

```
projet data/
│
├── data/                          # Données
│   ├── patients.csv               # Données d'entrée
│   ├── patients_with_clusters.csv # Résultats complets
│   ├── patients_anomalies.csv     # Liste des anomalies
│   ├── report.html                # Rapport HTML
│   └── *.png                      # Visualisations
│
├── src/                           # Code source
│   ├── config.py                  # Configuration centralisée
│   ├── data_loader.py             # Chargement des données
│   ├── preprocessing.py            # Nettoyage et normalisation
│   ├── dbscan_model.py            # Implémentation DBSCAN
│   ├── evaluation.py              # Métriques d'évaluation
│   ├── optimization.py            # Optimisation automatique
│   ├── visualization.py           # Visualisations
│   └── export_results.py         # Export des résultats
│
├── tests/                         # Tests unitaires
│   ├── test_data_loader.py
│   └── test_preprocessing.py
│
├── notebooks/                     # Analyse exploratoire
│   └── eda_dbscan.ipynb
│
├── app.py                         # Interface web Streamlit
├── main.py                        # Script principal CLI
├── requirements.txt               # Dépendances
└── README.md                      # Documentation
```

### 5.2 Modules Principaux

#### 5.2.1 Configuration (`config.py`)
- Gestion centralisée des paramètres
- Chemins de fichiers
- Configuration DBSCAN

#### 5.2.2 Chargement des Données (`data_loader.py`)
- Validation des colonnes requises
- Gestion des erreurs
- Logging informatif

#### 5.2.3 Préprocessing (`preprocessing.py`)
- Nettoyage des données
- Gestion des valeurs manquantes
- Normalisation StandardScaler

#### 5.2.4 DBSCAN (`dbscan_model.py`)
- Calcul courbe k-distance
- Application DBSCAN
- Identification des anomalies

#### 5.2.5 Évaluation (`evaluation.py`)
- Silhouette Score
- Davies-Bouldin Score
- Calinski-Harabasz Score
- Interprétations automatiques

#### 5.2.6 Optimisation (`optimization.py`)
- Recherche automatique des meilleurs paramètres
- Grid search sur eps et min_samples
- Optimisation basée sur métriques

#### 5.2.7 Visualisation (`visualization.py`)
- Graphiques 2D (PCA, t-SNE)
- Distributions des features
- Statistiques des clusters

#### 5.2.8 Export (`export_results.py`)
- Export CSV
- Rapport HTML professionnel
- Rapport textuel

---

## 6. Implémentation Technique

### 6.1 Technologies Utilisées

| Technologie | Version | Usage |
|------------|---------|-------|
| Python | 3.10+ | Langage principal |
| pandas | 2.0+ | Manipulation de données |
| numpy | 1.24+ | Calculs numériques |
| scikit-learn | 1.3+ | ML et preprocessing |
| matplotlib | 3.7+ | Visualisations statiques |
| seaborn | 0.12+ | Visualisations avancées |
| streamlit | 1.28+ | Interface web |
| plotly | 5.17+ | Graphiques interactifs |
| jupyter | 1.0+ | Notebooks |

### 6.2 Bonnes Pratiques Implémentées

- ✅ **Modularité** : Code organisé en modules réutilisables
- ✅ **Logging** : Système de logs complet
- ✅ **Gestion d'erreurs** : Try/except avec messages clairs
- ✅ **Documentation** : Docstrings complètes
- ✅ **Tests** : Tests unitaires pour validation
- ✅ **Configuration** : Paramètres centralisés
- ✅ **CLI** : Interface en ligne de commande avec argparse

---

## 7. Résultats et Analyses

### 7.1 Dataset d'Analyse

- **Nombre de patients** : 500
- **Features analysées** : 4
  - Pression artérielle systolique
  - Pression artérielle diastolique
  - Température corporelle
  - Fréquence cardiaque

### 7.2 Résultats du Clustering

#### 7.2.1 Distribution des Clusters

| Catégorie | Nombre | Pourcentage |
|-----------|--------|-------------|
| Patients normaux | 339 | 67.80% |
| Anomalies détectées | 161 | 32.20% |
| Clusters identifiés | 1 | - |

#### 7.2.2 Paramètres Utilisés

- **eps** : 0.6042 (déterminé automatiquement via k-distance)
- **min_samples** : 5
- **Méthode de normalisation** : StandardScaler

### 7.3 Analyse des Anomalies

Les 161 patients identifiés comme anomalies présentent des caractéristiques significativement différentes :

- **Pression artérielle** : Valeurs extrêmes (très élevées ou très basses)
- **Température** : Écarts importants par rapport à la normale
- **Fréquence cardiaque** : Rythmes anormaux

### 7.4 Visualisations Générées

1. **Courbe k-distance** : Détermination du paramètre eps optimal
2. **Visualisation 2D PCA** : Projection des clusters en 2 dimensions
3. **Distributions des features** : Comparaison patients normaux vs anomalies
4. **Statistiques des clusters** : Graphiques en barres et camembert

---

## 8. Fonctionnalités Avancées

### 8.1 Interface en Ligne de Commande (CLI)

Le script `main.py` offre une interface complète avec options :

```bash
python main.py --help                    # Aide
python main.py --optimize                # Optimisation auto
python main.py --eps 0.5                 # Paramètre personnalisé
python main.py --data custom.csv         # Fichier personnalisé
python main.py --verbose                 # Mode détaillé
```

### 8.2 Optimisation Automatique

Fonctionnalité permettant de trouver automatiquement les meilleurs paramètres :

- Test de différentes combinaisons eps/min_samples
- Évaluation basée sur Silhouette Score
- Retour des paramètres optimaux

### 8.3 Métriques d'Évaluation

Le système calcule et interprète automatiquement :

- **Silhouette Score** : Mesure la cohésion et séparation
- **Davies-Bouldin Score** : Mesure la séparation moyenne
- **Calinski-Harabasz Score** : Ratio de variance

### 8.4 Rapports Professionnels

#### 8.4.1 Rapport HTML
- Design moderne et responsive
- Métriques avec interprétations
- Statistiques détaillées
- Graphiques intégrés

#### 8.4.2 Export CSV
- Tous les patients avec clusters
- Liste des anomalies uniquement
- Format standard pour analyse externe

---

## 9. Interface Utilisateur

### 9.1 Application Streamlit

Interface web interactive permettant :

#### 9.1.1 Configuration
- Upload de fichiers CSV personnalisés
- Ajustement des paramètres DBSCAN en temps réel
- Choix entre détermination automatique ou manuelle de eps

#### 9.1.2 Visualisations Interactives
- Graphiques Plotly (zoom, pan, hover)
- Visualisation 2D PCA interactive
- Distributions des signes vitaux
- Statistiques par cluster

#### 9.1.3 Résultats
- Métriques en temps réel
- Tableau des anomalies
- Statistiques détaillées
- Téléchargement des résultats

### 9.2 Avantages de l'Interface

- ✅ **Accessibilité** : Pas besoin de connaissances en programmation
- ✅ **Interactivité** : Graphiques interactifs avec Plotly
- ✅ **Temps réel** : Résultats instantanés
- ✅ **Export facile** : Téléchargement direct des résultats

---

## 10. Évaluation et Métriques

### 10.1 Métriques Calculées

#### 10.1.1 Silhouette Score
- **Définition** : Mesure la cohésion intra-cluster et la séparation inter-clusters
- **Plage** : -1 à 1 (plus élevé = mieux)
- **Interprétation** :
  - > 0.7 : Excellent clustering
  - > 0.5 : Bon clustering
  - > 0.25 : Acceptable
  - < 0.25 : Faible

#### 10.1.2 Davies-Bouldin Score
- **Définition** : Mesure la séparation moyenne entre clusters
- **Plage** : 0 à ∞ (plus bas = mieux)
- **Interprétation** :
  - < 0.5 : Excellente séparation
  - < 1.0 : Bonne séparation
  - ≥ 1.0 : Séparation modérée

#### 10.1.3 Calinski-Harabasz Score
- **Définition** : Ratio de variance entre et dans les clusters
- **Plage** : 0 à ∞ (plus élevé = mieux)

### 10.2 Interprétation des Résultats

Le système fournit des interprétations automatiques pour chaque métrique, aidant les utilisateurs à comprendre la qualité du clustering.

---

## 11. Conclusion et Recommandations

### 11.1 Points Forts du Projet

1. **Complétude** : Pipeline end-to-end complet
2. **Professionnalisme** : Code propre, documenté, testé
3. **Flexibilité** : Interface CLI et web
4. **Extensibilité** : Architecture modulaire
5. **Documentation** : Documentation complète

### 11.2 Applications Potentielles

- **Hôpitaux** : Détection précoce de patients à risque
- **Centres de soins** : Surveillance continue des signes vitaux
- **Recherche médicale** : Analyse de patterns dans les données
- **Télémédecine** : Monitoring à distance

### 11.3 Recommandations

#### 11.3.1 Améliorations Futures

1. **Intégration de plus de features** : Ajouter d'autres signes vitaux
2. **Machine Learning avancé** : Essayer d'autres algorithmes (Isolation Forest, etc.)
3. **Temps réel** : Intégration avec systèmes de monitoring en temps réel
4. **Alertes automatiques** : Système d'alertes pour anomalies critiques
5. **Dashboard avancé** : Tableau de bord avec historique

#### 11.3.2 Déploiement

- **Production** : Déploiement sur serveur avec authentification
- **Scalabilité** : Optimisation pour grandes quantités de données
- **Sécurité** : Chiffrement des données médicales (RGPD/HIPAA)
- **API** : Création d'API REST pour intégration

### 11.4 Validation Médicale

⚠️ **Important** : Les résultats doivent toujours être validés par des professionnels de santé qualifiés avant toute décision clinique.

---

## 12. Annexes

### 12.1 Commandes Utiles

```bash
# Installation
pip install -r requirements.txt

# Exécution CLI
python main.py

# Interface web
streamlit run app.py

# Tests
python -m pytest tests/

# Notebook
jupyter notebook notebooks/eda_dbscan.ipynb
```

### 12.2 Structure des Données

#### Format d'Entrée (CSV)
```csv
patient_id,blood_pressure_systolic,blood_pressure_diastolic,temperature_c,heart_rate_bpm
P0001,120,80,37.0,72
P0002,140,90,38.5,85
...
```

#### Format de Sortie
- `patients_with_clusters.csv` : Tous les patients + labels de cluster
- `patients_anomalies.csv` : Seulement les anomalies
- `report.html` : Rapport HTML complet

### 12.3 Références

- Ester, M., et al. (1996). "A density-based algorithm for discovering clusters in large spatial databases with noise"
- scikit-learn Documentation: DBSCAN
- Streamlit Documentation

### 12.4 Contact et Support

Pour toute question ou contribution, consultez la documentation du projet dans `README.md`.

---

## 📊 Statistiques du Projet

- **Lignes de code** : ~2000+
- **Modules** : 8 modules principaux
- **Tests** : Suite de tests unitaires
- **Documentation** : README + Guide + Rapport
- **Interface** : CLI + Web (Streamlit)

---

**Fin du Rapport**

*Rapport généré automatiquement - Projet de Détection d'Anomalies Médicales avec DBSCAN*


