"""
Module de configuration centralisée pour le projet
"""

from dataclasses import dataclass
from typing import List
from pathlib import Path


@dataclass
class Config:
    """Configuration centralisée du projet"""
    
    # Chemins des fichiers
    data_dir: Path = Path('data')
    output_dir: Path = Path('data')
    notebooks_dir: Path = Path('notebooks')
    
    # Colonnes du dataset
    patient_id_col: str = 'patient_id'
    feature_cols: List[str] = None
    
    # Paramètres DBSCAN
    eps: float = None  # Sera déterminé automatiquement si None
    min_samples: int = 5
    k_distance_percentile: float = 50.0  # Percentile pour suggérer eps
    
    # Paramètres de visualisation
    figure_dpi: int = 300
    figure_size: tuple = (12, 8)
    
    # Paramètres de calcul
    max_samples_k_distance: int = 1000  # Pour le sous-échantillonnage
    
    def __post_init__(self):
        """Initialise les valeurs par défaut"""
        if self.feature_cols is None:
            self.feature_cols = [
                'blood_pressure_systolic',
                'blood_pressure_diastolic',
                'temperature_c',
                'heart_rate_bpm'
            ]
        
        # Créer les répertoires si nécessaire
        self.data_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
    
    @property
    def data_file(self) -> Path:
        """Chemin du fichier de données"""
        return self.data_dir / 'patients.csv'
    
    @property
    def required_columns(self) -> List[str]:
        """Colonnes requises dans le dataset"""
        return [self.patient_id_col] + self.feature_cols

