"""
Tests pour le module preprocessing
"""

import unittest
import pandas as pd
import numpy as np

from src.preprocessing import clean_data, prepare_features, normalize_features


class TestPreprocessing(unittest.TestCase):
    """Tests pour le preprocessing"""
    
    def setUp(self):
        """Créer des données de test"""
        self.df = pd.DataFrame({
            'patient_id': [f'P{i:04d}' for i in range(1, 21)],
            'blood_pressure_systolic': np.random.normal(120, 15, 20),
            'blood_pressure_diastolic': np.random.normal(80, 10, 20),
            'temperature_c': np.random.normal(37.0, 0.5, 20),
            'heart_rate_bpm': np.random.normal(72, 12, 20)
        })
        # Ajouter quelques valeurs manquantes
        self.df.loc[0, 'blood_pressure_systolic'] = np.nan
        self.df.loc[1, 'temperature_c'] = np.nan
    
    def test_clean_data(self):
        """Test du nettoyage des données"""
        df_clean = clean_data(self.df, patient_id_col='patient_id')
        self.assertEqual(len(df_clean), 20)
        # Vérifier que les NaN sont remplis
        self.assertFalse(df_clean['blood_pressure_systolic'].isnull().any())
    
    def test_prepare_features(self):
        """Test de préparation des features"""
        feature_cols = ['blood_pressure_systolic', 'blood_pressure_diastolic', 
                       'temperature_c', 'heart_rate_bpm']
        X, patient_ids = prepare_features(self.df, feature_cols, 'patient_id')
        self.assertEqual(X.shape[0], 20)
        self.assertEqual(X.shape[1], 4)
        self.assertEqual(len(patient_ids), 20)
    
    def test_normalize_features(self):
        """Test de normalisation"""
        feature_cols = ['blood_pressure_systolic', 'blood_pressure_diastolic', 
                       'temperature_c', 'heart_rate_bpm']
        X, _ = prepare_features(self.df, feature_cols, 'patient_id')
        X_scaled, scaler = normalize_features(X)
        
        # Vérifier que la moyenne est proche de 0
        self.assertAlmostEqual(X_scaled.mean(), 0, places=1)
        # Vérifier que l'écart-type est proche de 1
        self.assertAlmostEqual(X_scaled.std(), 1, places=1)


if __name__ == '__main__':
    unittest.main()

