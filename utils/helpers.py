import json
import pandas as pd
import numpy as np
from typing import Any, Dict, List
import logging

def setup_logging():
    """Setup basic logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('market_intelligence.log'),
            logging.StreamHandler()
        ]
    )

class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy data types"""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif pd.isna(obj):
            return None
        return super().default(obj)

def safe_divide(numerator, denominator, default=0):
    """Safely divide two numbers, return default if denominator is 0"""
    if denominator == 0 or denominator is None or pd.isna(denominator):
        return default
    return numerator / denominator

def format_large_number(num):
    """Format large numbers for display"""
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return str(num)

def save_json(data: Dict, filepath: str):
    """Save data to JSON file with proper error handling"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, cls=NumpyEncoder)
        logging.info(f"Data saved to {filepath}")
        return True
    except Exception as e:
        logging.error(f"Error saving to {filepath}: {str(e)}")
        return False

def load_json(filepath: str) -> Dict:
    """Load data from JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading from {filepath}: {str(e)}")
        return {}

def validate_dataframe(df: pd.DataFrame, required_columns: List[str] = None) -> bool:
    """Validate dataframe structure and data quality"""
    if df.empty:
        logging.warning("DataFrame is empty")
        return False
    
    if required_columns:
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            logging.warning(f"Missing required columns: {missing_columns}")
            return False
    
    # Check for excessive null values
    null_percentage = df.isnull().sum() / len(df)
    high_null_columns = null_percentage[null_percentage > 0.5].index.tolist()
    if high_null_columns:
        logging.warning(f"Columns with high null percentage: {high_null_columns}")
    
    return True