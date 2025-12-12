"""
Module de préprocessing des données patients
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clean_data(df: pd.DataFrame, patient_id_col: str = 'patient_id') -> pd.DataFrame:
    """
    Nettoie les données: gestion des valeurs manquantes, types, doublons.
    
    Args:
        df: DataFrame à nettoyer
        patient_id_col: Nom de la colonne contenant l'ID patient
        
    Returns:
        DataFrame nettoyé
    """
    logger.info("Début du nettoyage des données")
    df_clean = df.copy()
    
    # Vérifier les doublons
    initial_count = len(df_clean)
    if patient_id_col in df_clean.columns:
        df_clean = df_clean.drop_duplicates(subset=[patient_id_col], keep='first')
        duplicates = initial_count - len(df_clean)
        if duplicates > 0:
            logger.warning(f"{duplicates} doublons supprimés basés sur {patient_id_col}")
    
    # Colonnes numériques pour le nettoyage
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
    if patient_id_col in numeric_cols:
        numeric_cols.remove(patient_id_col)
    
    # Gestion des valeurs manquantes
    missing_before = df_clean[numeric_cols].isnull().sum().sum()
    if missing_before > 0:
        logger.warning(f"Valeurs manquantes détectées: {missing_before}")
        # Remplacer par la médiane pour les colonnes numériques
        for col in numeric_cols:
            if df_clean[col].isnull().sum() > 0:
                median_val = df_clean[col].median()
                df_clean[col].fillna(median_val, inplace=True)
                logger.info(f"Colonne {col}: valeurs manquantes remplacées par médiane ({median_val:.2f})")
    
    # Vérifier les valeurs aberrantes extrêmes (optionnel, on les garde pour DBSCAN)
    logger.info(f"Nettoyage terminé: {len(df_clean)} patients conservés")
    
    return df_clean


def prepare_features(df: pd.DataFrame, feature_cols: list, patient_id_col: str = 'patient_id') -> tuple:
    """
    Prépare les features pour l'analyse DBSCAN.
    
    Args:
        df: DataFrame nettoyé
        feature_cols: Liste des colonnes à utiliser comme features
        patient_id_col: Nom de la colonne ID patient
        
    Returns:
        Tuple (X, patient_ids) où X est la matrice de features et patient_ids les IDs
    """
    logger.info(f"Préparation des features: {feature_cols}")
    
    # Extraire les IDs patients si disponibles
    if patient_id_col in df.columns:
        patient_ids = df[patient_id_col].values
    else:
        patient_ids = np.arange(len(df))
        logger.warning(f"Colonne {patient_id_col} non trouvée, utilisation d'index numériques")
    
    # Extraire les features
    X = df[feature_cols].values
    
    # Vérifier les valeurs infinies ou NaN
    if np.isinf(X).any() or np.isnan(X).any():
        logger.warning("Valeurs infinies ou NaN détectées dans les features")
        X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
    
    logger.info(f"Features préparées: shape {X.shape}")
    
    return X, patient_ids


def normalize_features(X: np.ndarray) -> tuple:
    """
    Normalise les features avec StandardScaler.
    
    Args:
        X: Matrice de features (n_samples, n_features)
        
    Returns:
        Tuple (X_scaled, scaler) où X_scaled est la matrice normalisée
    """
    logger.info("Normalisation des features avec StandardScaler")
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    logger.info("Normalisation terminée")
    
    return X_scaled, scaler

