import pandas as pd
import numpy as np
import re
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DataCleaner:
    def __init__(self):
        self.cleaning_stats = {}
    
    def clean_playstore_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and normalize Play Store data"""
        logger.info("Starting Play Store data cleaning")
        
        # Create a copy to avoid SettingWithCopyWarning
        df_clean = df.copy()
        
        # Initial stats
        initial_count = len(df_clean)
        self.cleaning_stats['initial_count'] = initial_count
        
        # Handle missing values
        df_clean['Rating'] = pd.to_numeric(df_clean['Rating'], errors='coerce')
        df_clean['Reviews'] = pd.to_numeric(df_clean['Reviews'], errors='coerce')
        
        # Fill missing ratings with category mean
        df_clean['Rating'] = df_clean.groupby('Category')['Rating'].transform(
            lambda x: x.fillna(x.mean())
        )
        df_clean['Rating'] = df_clean['Rating'].fillna(df_clean['Rating'].mean())
        
        # Clean installs column
        df_clean['Installs'] = self._clean_installs_column(df_clean['Installs'])
        
        # Clean size column
        df_clean['Size_MB'] = df_clean['Size'].apply(self._convert_size_to_mb)
        
        # Clean price column
        df_clean['Price'] = self._clean_price_column(df_clean['Price'])
        
        # Convert last updated to datetime
        df_clean['Last Updated'] = pd.to_datetime(df_clean['Last Updated'], errors='coerce')
        
        # Clean category names
        df_clean['Category'] = df_clean['Category'].str.upper()
        
        # Remove duplicates
        df_clean = df_clean.drop_duplicates(subset=['App'], keep='first')
        
        # Remove apps with suspicious data
        df_clean = df_clean[df_clean['Reviews'] >= 0]
        df_clean = df_clean[df_clean['Rating'] <= 5]
        
        final_count = len(df_clean)
        self.cleaning_stats['final_count'] = final_count
        self.cleaning_stats['removed_count'] = initial_count - final_count
        
        logger.info(f"Play Store cleaning complete: {final_count} records remaining "
                   f"({self.cleaning_stats['removed_count']} removed)")
        
        return df_clean

    def _clean_installs_column(self, installs_series: pd.Series) -> pd.Series:
        """Clean and convert installs column to numeric"""
        def convert_installs(installs):
            if pd.isna(installs) or installs == '0':
                return 0
            if installs == '0+':
                return 1
            # Remove + and commas, convert to numeric
            clean_str = str(installs).replace('+', '').replace(',', '')
            try:
                return int(clean_str)
            except (ValueError, TypeError):
                return 0
        
        return installs_series.apply(convert_installs)

    def _convert_size_to_mb(self, size_str):
        """Convert size string to MB"""
        if pd.isna(size_str) or size_str == 'Varies with device':
            return np.nan
        
        size_str = str(size_str).upper()
        
        # Handle ranges like "1.2M - 5.6M"
        if ' - ' in size_str:
            size_str = size_str.split(' - ')[0]
        
        try:
            if 'M' in size_str:
                return float(size_str.replace('M', '').strip())
            elif 'K' in size_str:
                return float(size_str.replace('K', '').strip()) / 1024
            elif 'G' in size_str:
                return float(size_str.replace('G', '').strip()) * 1024
            else:
                return float(size_str)
        except (ValueError, TypeError):
            return np.nan

    def _clean_price_column(self, price_series: pd.Series) -> pd.Series:
        """Clean price column and convert to numeric"""
        def convert_price(price):
            if pd.isna(price) or price == '0':
                return 0.0
            price_str = str(price)
            # Remove dollar signs and convert to float
            clean_price = price_str.replace('$', '').strip()
            try:
                return float(clean_price)
            except (ValueError, TypeError):
                return 0.0
        
        return price_series.apply(convert_price)

    def get_cleaning_report(self) -> Dict[str, Any]:
        """Generate a report of cleaning operations performed"""
        return {
            'initial_record_count': self.cleaning_stats.get('initial_count', 0),
            'final_record_count': self.cleaning_stats.get('final_count', 0),
            'records_removed': self.cleaning_stats.get('removed_count', 0),
            'cleaning_operations': [
                'Missing value imputation',
                'Data type conversion',
                'Duplicate removal',
                'Data validation'
            ]
        }