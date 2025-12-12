"""
Application Streamlit pour l'interface web du projet de détection d'anomalies médicales
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Configuration de la page
st.set_page_config(
    page_title="Détection d'Anomalies Médicales - DBSCAN",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Import des modules du projet
import sys
sys.path.append(str(Path(__file__).parent))

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
from src.evaluation import evaluate_clustering, interpret_metrics
from src.export_results import export_results, generate_html_report


def main():
    """Fonction principale de l'application Streamlit"""
    
    # Header
    st.markdown('<h1 class="main-header">🏥 Détection d\'Anomalies Médicales avec DBSCAN</h1>', 
                unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar - Configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Option de chargement des données
        data_source = st.radio(
            "Source des données",
            ["Fichier existant", "Upload fichier CSV"]
        )
        
        if data_source == "Fichier existant":
            data_file = st.selectbox(
                "Sélectionner le fichier",
                ["data/patients.csv"],
                index=0
            )
        else:
            uploaded_file = st.file_uploader(
                "Charger un fichier CSV",
                type=['csv'],
                help="Le fichier doit contenir les colonnes: patient_id, blood_pressure_systolic, blood_pressure_diastolic, temperature_c, heart_rate_bpm"
            )
            if uploaded_file is not None:
                data_file = uploaded_file
            else:
                st.stop()
        
        st.markdown("---")
        st.header("🔧 Paramètres DBSCAN")
        
        use_auto_eps = st.checkbox("Déterminer eps automatiquement", value=True)
        
        if not use_auto_eps:
            eps_value = st.slider(
                "Valeur eps",
                min_value=0.1,
                max_value=2.0,
                value=0.6,
                step=0.1
            )
        else:
            eps_value = None
        
        min_samples = st.slider(
            "Min Samples",
            min_value=3,
            max_value=20,
            value=5,
            step=1
        )
        
        st.markdown("---")
        
        if st.button("🚀 Lancer l'analyse", type="primary"):
            st.session_state.run_analysis = True
    
    # Contenu principal
    if 'run_analysis' not in st.session_state:
        st.session_state.run_analysis = False
    
    if not st.session_state.run_analysis:
        # Page d'accueil
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("""
            **📊 Analyse Complète**
            - Chargement et nettoyage des données
            - Normalisation des features
            - Application de DBSCAN
            """)
        
        with col2:
            st.info("""
            **📈 Visualisations**
            - Courbe k-distance
            - Clusters 2D (PCA)
            - Distributions des signes vitaux
            """)
        
        with col3:
            st.info("""
            **📋 Résultats**
            - Détection d'anomalies
            - Métriques d'évaluation
            - Rapports détaillés
            """)
        
        st.markdown("---")
        st.markdown("### 📖 Instructions")
        st.markdown("""
        1. Configurez les paramètres dans la barre latérale
        2. Sélectionnez ou uploadez votre fichier de données
        3. Cliquez sur **"Lancer l'analyse"** pour démarrer
        """)
        
        # Afficher les données existantes si disponibles
        if Path("data/patients.csv").exists():
            st.markdown("### 📁 Données disponibles")
            try:
                df_preview = pd.read_csv("data/patients.csv", nrows=5)
                st.dataframe(df_preview, use_container_width=True)
            except:
                pass
    
    else:
        # Exécuter l'analyse
        with st.spinner("🔄 Analyse en cours..."):
            try:
                # Chargement des données
                st.header("📥 Chargement des données")
                
                if isinstance(data_file, str):
                    df = load_patient_data(data_file)
                else:
                    df = pd.read_csv(data_file)
                    validate_required_columns(df, ['patient_id', 'blood_pressure_systolic', 
                                                  'blood_pressure_diastolic', 'temperature_c', 
                                                  'heart_rate_bpm'])
                
                st.success(f"✅ {len(df)} patients chargés avec succès")
                
                # Afficher un aperçu des données
                with st.expander("👀 Aperçu des données"):
                    st.dataframe(df.head(10), use_container_width=True)
                    st.write(f"**Shape:** {df.shape}")
                    st.write(f"**Colonnes:** {', '.join(df.columns)}")
                
                # Nettoyage
                st.header("🧹 Nettoyage des données")
                df_clean = clean_data(df, patient_id_col='patient_id')
                st.success(f"✅ {len(df_clean)} patients après nettoyage")
                
                # Préparation des features
                feature_cols = ['blood_pressure_systolic', 'blood_pressure_diastolic', 
                               'temperature_c', 'heart_rate_bpm']
                X, patient_ids = prepare_features(df_clean, feature_cols, 'patient_id')
                X_scaled, scaler = normalize_features(X)
                
                # Calcul de eps si nécessaire
                if eps_value is None:
                    st.header("📊 Calcul de la courbe k-distance")
                    k_distances = compute_k_distance_curve(X_scaled, k=min_samples)
                    eps_value = suggest_eps_from_k_distance(k_distances, percentile=50.0)
                    
                    # Afficher la courbe k-distance
                    fig_kdist = plt.figure(figsize=(10, 6))
                    plt.plot(range(len(k_distances)), k_distances, 'b-', linewidth=2)
                    plt.axhline(y=eps_value, color='r', linestyle='--', 
                               label=f'eps suggéré: {eps_value:.4f}')
                    plt.xlabel('Points triés par distance')
                    plt.ylabel(f'Distance au {min_samples}-ième voisin')
                    plt.title('Courbe k-distance pour déterminer eps optimal')
                    plt.legend()
                    plt.grid(True, alpha=0.3)
                    st.pyplot(fig_kdist)
                    plt.close()
                
                # Application DBSCAN
                st.header("🔍 Application de DBSCAN")
                labels, dbscan_model = apply_dbscan(X_scaled, eps=eps_value, min_samples=min_samples)
                
                # Métriques
                metrics = evaluate_clustering(X_scaled, labels)
                interpretations = interpret_metrics(metrics)
                
                # Affichage des métriques principales
                col1, col2, col3, col4 = st.columns(4)
                
                n_total = len(labels)
                n_anomalies = np.sum(labels == -1)
                n_normal = n_total - n_anomalies
                n_clusters = metrics['n_clusters']
                
                with col1:
                    st.metric("Total Patients", n_total)
                
                with col2:
                    st.metric("Anomalies", n_anomalies, f"{100*n_anomalies/n_total:.1f}%")
                
                with col3:
                    st.metric("Patients Normaux", n_normal, f"{100*n_normal/n_total:.1f}%")
                
                with col4:
                    st.metric("Clusters", n_clusters)
                
                # Métriques d'évaluation
                st.header("📈 Métriques d'Évaluation")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if metrics.get('silhouette_score') is not None:
                        st.metric("Silhouette Score", f"{metrics['silhouette_score']:.4f}")
                        st.caption(interpretations.get('silhouette', ''))
                    else:
                        st.metric("Silhouette Score", "N/A")
                
                with col2:
                    if metrics.get('davies_bouldin_score') is not None:
                        st.metric("Davies-Bouldin Score", f"{metrics['davies_bouldin_score']:.4f}")
                        st.caption(interpretations.get('davies_bouldin', ''))
                    else:
                        st.metric("Davies-Bouldin Score", "N/A")
                
                with col3:
                    if metrics.get('calinski_harabasz_score') is not None:
                        st.metric("Calinski-Harabasz", f"{metrics['calinski_harabasz_score']:.2f}")
                    else:
                        st.metric("Calinski-Harabasz", "N/A")
                
                # Visualisation 2D avec PCA
                st.header("📊 Visualisation 2D des Clusters")
                
                pca = PCA(n_components=2, random_state=42)
                X_pca = pca.fit_transform(X_scaled)
                
                df_viz = pd.DataFrame({
                    'PC1': X_pca[:, 0],
                    'PC2': X_pca[:, 1],
                    'Cluster': labels,
                    'Patient_ID': patient_ids
                })
                
                # Créer le graphique interactif avec Plotly
                fig = px.scatter(
                    df_viz,
                    x='PC1',
                    y='PC2',
                    color='Cluster',
                    hover_data=['Patient_ID'],
                    title='Visualisation 2D des Clusters (PCA)',
                    color_continuous_scale='Viridis'
                )
                fig.update_traces(marker=dict(size=8, opacity=0.7))
                st.plotly_chart(fig, use_container_width=True)
                
                # Distributions des features
                st.header("📉 Distributions des Signes Vitaux")
                
                df_clean['cluster_label'] = labels
                df_clean['is_anomaly'] = (labels == -1)
                
                for col in feature_cols:
                    fig_dist = plt.figure(figsize=(10, 4))
                    
                    normal_data = df_clean[df_clean['is_anomaly'] == False][col]
                    anomaly_data = df_clean[df_clean['is_anomaly'] == True][col]
                    
                    plt.hist(normal_data, bins=30, alpha=0.6, label='Patients normaux', 
                            color='blue', density=True)
                    plt.hist(anomaly_data, bins=30, alpha=0.8, label='Anomalies', 
                            color='red', density=True)
                    plt.xlabel(col)
                    plt.ylabel('Densité')
                    plt.title(f'Distribution: {col}')
                    plt.legend()
                    plt.grid(True, alpha=0.3)
                    st.pyplot(fig_dist)
                    plt.close()
                
                # Tableau des anomalies
                st.header("⚠️ Patients Identifiés comme Anomalies")
                
                df_anomalies = df_clean[df_clean['is_anomaly'] == True].copy()
                st.dataframe(
                    df_anomalies[['patient_id'] + feature_cols],
                    use_container_width=True
                )
                
                # Statistiques par cluster
                st.header("📊 Statistiques par Cluster")
                
                cluster_stats = df_clean.groupby('cluster_label')[feature_cols].agg(['mean', 'std'])
                st.dataframe(cluster_stats, use_container_width=True)
                
                # Téléchargement des résultats
                st.header("💾 Télécharger les Résultats")
                
                # Exporter les résultats
                output_files = export_results(df_clean, labels, 'patient_id', output_dir='data')
                
                col1, col2 = st.columns(2)
                
                with col1:
                    df_all = pd.read_csv(output_files['all_patients'])
                    csv_all = df_all.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Télécharger tous les patients (CSV)",
                        data=csv_all,
                        file_name="patients_with_clusters.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    df_anom = pd.read_csv(output_files['anomalies'])
                    csv_anom = df_anom.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Télécharger anomalies uniquement (CSV)",
                        data=csv_anom,
                        file_name="patients_anomalies.csv",
                        mime="text/csv"
                    )
                
                st.success("✅ Analyse terminée avec succès!")
                
            except Exception as e:
                st.error(f"❌ Erreur lors de l'analyse: {str(e)}")
                st.exception(e)


if __name__ == "__main__":
    main()

