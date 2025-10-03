import unittest
import pandas as pd
import numpy as np
import os
import sys

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.data_ingestion import DataIngestion
from pipelines.data_cleaning import DataCleaner

class TestDataPipeline(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.ingestion = DataIngestion()
        self.cleaner = DataCleaner()
        
        # Create sample test data
        self.sample_playstore_data = pd.DataFrame({
            'App': ['Test App 1', 'Test App 2', 'Test App 3'],
            'Category': ['GAME', 'SOCIAL', 'PRODUCTIVITY'],
            'Rating': [4.5, 3.8, 4.2],
            'Reviews': ['1000', '5000', '2500'],
            'Size': ['10M', '25M', 'Varies with device'],
            'Installs': ['1,000+', '10,000+', '100,000+'],
            'Type': ['Free', 'Free', 'Paid'],
            'Price': ['0', '0', '$2.99'],
            'Content Rating': ['Everyone', 'Teen', 'Everyone'],
            'Last Updated': ['2023-01-01', '2023-02-01', '2023-03-01']
        })
    
    def test_data_ingestion_initialization(self):
        """Test data ingestion class initialization"""
        self.assertIsInstance(self.ingestion, DataIngestion)
    
    def test_playstore_data_loading(self):
        """Test Play Store data loading functionality"""
        df = self.ingestion.load_playstore_data()
        # Should return DataFrame even with sample data
        self.assertIsInstance(df, pd.DataFrame)
    
    def test_data_cleaning(self):
        """Test data cleaning functionality"""
        cleaned_df = self.cleaner.clean_playstore_data(self.sample_playstore_data)
        
        # Check that DataFrame is returned
        self.assertIsInstance(cleaned_df, pd.DataFrame)
        
        # Check that numeric columns are properly converted
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned_df['Rating']))
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned_df['Reviews']))
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned_df['Installs']))
        self.assertTrue(pd.api.types.is_numeric_dtype(cleaned_df['Price']))
    
    def test_size_conversion(self):
        """Test size conversion to MB"""
        # Test MB conversion
        self.assertEqual(self.cleaner._convert_size_to_mb('10M'), 10.0)
        # Test KB conversion
        self.assertAlmostEqual(self.cleaner._convert_size_to_mb('1024K'), 1.0)
        # Test varies with device
        self.assertTrue(pd.isna(self.cleaner._convert_size_to_mb('Varies with device')))
    
    def test_installs_conversion(self):
        """Test installs string to numeric conversion"""
        self.assertEqual(self.cleaner._clean_installs_column(pd.Series(['1,000+'])).iloc[0], 1000)
        self.assertEqual(self.cleaner._clean_installs_column(pd.Series(['0+'])).iloc[0], 1)
        self.assertEqual(self.cleaner._clean_installs_column(pd.Series(['0'])).iloc[0], 0)
    
    def test_price_conversion(self):
        """Test price string to numeric conversion"""
        self.assertEqual(self.cleaner._clean_price_column(pd.Series(['$2.99'])).iloc[0], 2.99)
        self.assertEqual(self.cleaner._clean_price_column(pd.Series(['0'])).iloc[0], 0.0)
        self.assertEqual(self.cleaner._clean_price_column(pd.Series(['Free'])).iloc[0], 0.0)
    
    def test_unified_schema_creation(self):
        """Test unified schema creation"""
        playstore_df = self.cleaner.clean_playstore_data(self.sample_playstore_data)
        appstore_df = self.ingestion._create_sample_appstore_data()
        
        combined_df = self.ingestion.create_unified_schema(playstore_df, appstore_df)
        
        # Check required columns exist
        required_columns = ['name', 'category', 'rating', 'review_count', 'platform']
        for col in required_columns:
            self.assertIn(col, combined_df.columns)
        
        # Check both platforms are represented
        platforms = combined_df['platform'].unique()
        self.assertIn('android', platforms)
        self.assertIn('ios', platforms)

if __name__ == '__main__':
    unittest.main()