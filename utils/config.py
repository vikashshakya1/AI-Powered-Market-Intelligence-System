# utils/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # File Paths
    DATA_RAW_PATH = 'data/raw'
    DATA_PROCESSED_PATH = 'data/processed'
    DATA_OUTPUTS_PATH = 'data/outputs'
    
    # API Endpoints - UPDATED with your specific host
    RAPIDAPI_URL = "https://appstore-scrapper-api.p.rapidapi.com/app/details"
    RAPIDAPI_HOST = "appstore-scrapper-api.p.rapidapi.com"
    
    # LLM Settings
    DEFAULT_LLM_PROVIDER = os.getenv('DEFAULT_LLM_PROVIDER', 'openai')
    DEFAULT_MODEL = "gpt-3.5-turbo"
    
    # Data Settings
    SAMPLE_SIZE = 1000
    MAX_APPS_FETCH = 50
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        missing = []
        if not cls.RAPIDAPI_KEY:
            missing.append("RAPIDAPI_KEY")
        if not cls.OPENAI_API_KEY and not cls.GEMINI_API_KEY:
            missing.append("Either OPENAI_API_KEY or GEMINI_API_KEY")
        
        if missing:
            print(f"Warning: Missing environment variables: {', '.join(missing)}")
            print("Some features may not work properly.")
        
        return len(missing) == 0