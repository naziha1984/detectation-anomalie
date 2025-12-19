"""
Tests pour le module data_loader
"""

import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os

from src.data_loader import load_patient_data, validate_required_columns


class TestDataLoader(unittest.TestCase):
    """Tests pour le chargement des données"""
    
    def setUp(self):
        """Créer un fichier CSV de test"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = Path(self.temp_dir) / 'test_patients.csv'
        
        # Créer des données de test
        data = {
            'patient_id': [f'P{i:04d}' for i in range(1, 11)],
            'blood_pressure_systolic': np.random.normal(120, 15, 10),
            'blood_pressure_diastolic': np.random.normal(80, 10, 10),
            'temperature_c': np.random.normal(37.0, 0.5, 10),
            'heart_rate_bpm': np.random.normal(72, 12, 10)
        }
        df = pd.DataFrame(data)
        df.to_csv(self.test_file, index=False)
    
    def tearDown(self):
        """Nettoyer les fichiers temporaires"""
        if self.test_file.exists():
            os.remove(self.test_file)
        os.rmdir(self.temp_dir)
    
    def test_load_patient_data(self):
        """Test du chargement des données"""
        df = load_patient_data(str(self.test_file))
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 10)
        self.assertIn('patient_id', df.columns)
    
    def test_load_nonexistent_file(self):
        """Test avec un fichier inexistant"""
        with self.assertRaises(FileNotFoundError):
            load_patient_data('nonexistent.csv')
    
    def test_validate_required_columns(self):
        """Test de validation des colonnes"""
        df = load_patient_data(str(self.test_file))
        required = ['patient_id', 'blood_pressure_systolic', 'blood_pressure_diastolic', 
                   'temperature_c', 'heart_rate_bpm']
        self.assertTrue(validate_required_columns(df, required))
    
    def test_validate_missing_columns(self):
        """Test avec des colonnes manquantes"""
        df = load_patient_data(str(self.test_file))
        required = ['patient_id', 'missing_column']
        with self.assertRaises(ValueError):
            validate_required_columns(df, required)


if __name__ == '__main__':
    unittest.main()

