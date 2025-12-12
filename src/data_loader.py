"""
Module de chargement des données patients
"""

import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_patient_data(file_path: str) -> pd.DataFrame:
    """
    Charge les données patients depuis un fichier CSV.
    
    Args:
        file_path: Chemin vers le fichier CSV contenant les données patients
        
    Returns:
        DataFrame pandas contenant les données patients
        
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        ValueError: Si le fichier est vide ou mal formaté
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Le fichier {file_path} n'existe pas.")
    
    logger.info(f"Chargement des données depuis {file_path}")
    
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Données chargées avec succès: {len(df)} patients, {len(df.columns)} colonnes")
        return df
    except Exception as e:
        logger.error(f"Erreur lors du chargement: {e}")
        raise ValueError(f"Impossible de charger le fichier: {e}")


def validate_required_columns(df: pd.DataFrame, required_cols: list) -> bool:
    """
    Vérifie que toutes les colonnes requises sont présentes dans le DataFrame.
    
    Args:
        df: DataFrame à valider
        required_cols: Liste des colonnes requises
        
    Returns:
        True si toutes les colonnes sont présentes
        
    Raises:
        ValueError: Si des colonnes sont manquantes
    """
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        raise ValueError(
            f"Colonnes manquantes: {missing_cols}. "
            f"Colonnes disponibles: {list(df.columns)}"
        )
    
    logger.info("Validation des colonnes: OK")
    return True

