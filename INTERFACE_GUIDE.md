# 🖥️ Guide d'Utilisation de l'Interface Web

## 🚀 Lancement de l'Interface

### Méthode 1: Script Windows (Recommandé)
Double-cliquez sur `run_app.bat` ou exécutez dans PowerShell:
```powershell
.\run_app.bat
```

### Méthode 2: Ligne de commande
```bash
streamlit run app.py
```

### Méthode 3: Avec options personnalisées
```bash
streamlit run app.py --server.port 8501 --server.address localhost
```

## 📋 Fonctionnalités de l'Interface

### 1. **Configuration dans la Barre Latérale**
- **Source des données**: Choisir entre fichier existant ou upload
- **Paramètres DBSCAN**: 
  - Déterminer eps automatiquement (recommandé)
  - Ou spécifier manuellement avec le slider
  - Ajuster min_samples

### 2. **Page d'Accueil**
- Aperçu des fonctionnalités
- Instructions d'utilisation
- Prévisualisation des données disponibles

### 3. **Résultats de l'Analyse**
Une fois l'analyse lancée, vous verrez:

#### 📊 Métriques Principales
- Total de patients analysés
- Nombre d'anomalies détectées
- Patients normaux
- Nombre de clusters identifiés

#### 📈 Métriques d'Évaluation
- Silhouette Score (qualité du clustering)
- Davies-Bouldin Score (séparation des clusters)
- Calinski-Harabasz Score

#### 📉 Visualisations Interactives
- **Courbe k-distance**: Pour déterminer le paramètre eps optimal
- **Visualisation 2D PCA**: Graphique interactif avec Plotly
  - Zoom, pan, hover pour voir les détails
  - Couleurs par cluster
- **Distributions des signes vitaux**: Comparaison patients normaux vs anomalies

#### ⚠️ Tableau des Anomalies
- Liste complète des patients identifiés comme anomalies
- Affichage de tous leurs signes vitaux

#### 📊 Statistiques par Cluster
- Moyennes et écarts-types pour chaque cluster
- Comparaison entre clusters

#### 💾 Téléchargement des Résultats
- Boutons pour télécharger:
  - Tous les patients avec leurs clusters (CSV)
  - Seulement les anomalies (CSV)

## 🎨 Caractéristiques de l'Interface

- **Design Moderne**: Interface claire et professionnelle
- **Responsive**: S'adapte à différentes tailles d'écran
- **Interactif**: Graphiques interactifs avec Plotly
- **Temps Réel**: Analyse en direct avec indicateurs de progression
- **Export Facile**: Téléchargement direct des résultats

## 🔧 Personnalisation

### Changer le Port
```bash
streamlit run app.py --server.port 8502
```

### Mode Sombre
L'interface s'adapte automatiquement au thème de votre système.

### Partage en Réseau
Pour accéder depuis d'autres appareils sur le même réseau:
```bash
streamlit run app.py --server.address 0.0.0.0
```

## ⚠️ Résolution de Problèmes

### L'application ne démarre pas
1. Vérifiez que Streamlit est installé: `pip install streamlit`
2. Vérifiez que vous êtes dans le bon répertoire
3. Vérifiez que `app.py` existe

### Erreur lors du chargement des données
- Vérifiez que le fichier CSV contient les colonnes requises:
  - `patient_id`
  - `blood_pressure_systolic`
  - `blood_pressure_diastolic`
  - `temperature_c`
  - `heart_rate_bpm`

### L'analyse est lente
- Réduisez le nombre de patients dans votre dataset
- Désactivez certaines visualisations si nécessaire

## 📱 Accès Mobile

L'interface est responsive et fonctionne sur mobile. Accédez-y via l'adresse IP de votre machine.

## 🔐 Sécurité

⚠️ **Note**: Cette interface est conçue pour un usage local. Pour un déploiement en production, configurez l'authentification et HTTPS.

