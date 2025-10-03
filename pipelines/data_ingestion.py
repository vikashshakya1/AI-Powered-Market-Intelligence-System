import pandas as pd
import requests
import time
import os
from typing import List, Optional, Dict
import logging
from utils.config import Config
from utils.helpers import safe_divide, validate_dataframe

logger = logging.getLogger(__name__)

class DataIngestion:
    def __init__(self, rapidapi_key: str = None):
        self.rapidapi_key = rapidapi_key or Config.RAPIDAPI_KEY
        self.base_path = "data"
        
    def load_playstore_data(self, file_path: str = None) -> pd.DataFrame:
        """Load Google Play Store data from CSV"""
        if file_path is None:
            file_path = os.path.join(Config.DATA_RAW_PATH, "googleplaystore.csv")
        
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Loaded {len(df)} records from Play Store dataset")
            return df
        except FileNotFoundError:
            logger.error(f"Play Store data file not found: {file_path}")
            # Create sample data for demonstration
            return self._create_sample_playstore_data()
        except Exception as e:
            logger.error(f"Error loading Play Store data: {str(e)}")
            return pd.DataFrame()

    def _create_sample_playstore_data(self) -> pd.DataFrame:
        """Create sample Play Store data for testing"""
        import faker
        fake = faker.Faker()
        
        categories = ['GAME', 'SOCIAL', 'PRODUCTIVITY', 'EDUCATION', 'HEALTH', 'FINANCE']
        types = ['Free', 'Paid']
        content_ratings = ['Everyone', 'Teen', 'Mature 17+']
        
        data = []
        for i in range(1000):
            data.append({
                'App': fake.word().title() + ' App',
                'Category': fake.random_element(categories),
                'Rating': fake.random_int(min=1, max=50) / 10,
                'Reviews': fake.random_int(min=100, max=1000000),
                'Size': f"{fake.random_int(min=1, max=100)}M",
                'Installs': fake.random_element(['1,000+', '10,000+', '100,000+', '1,000,000+', '10,000,000+']),
                'Type': fake.random_element(types),
                'Price': '0' if fake.boolean() else f"${fake.random_int(min=1, max=20)}",
                'Content Rating': fake.random_element(content_ratings),
                'Last Updated': fake.date_this_decade()
            })
        
        return pd.DataFrame(data)

    def fetch_appstore_data(self, app_ids: List[str] = None, max_apps: int = None) -> pd.DataFrame:
    """Fetch data from App Store using RapidAPI"""
    if not self.rapidapi_key:
        logger.warning("RapidAPI key not provided. Skipping App Store data.")
        return self._create_sample_appstore_data()
        
    if max_apps is None:
        max_apps = Config.MAX_APPS_FETCH
        
    url = Config.RAPIDAPI_URL
    headers = {
        "X-RapidAPI-Key": self.rapidapi_key,
        "X-RapidAPI-Host": Config.RAPIDAPI_HOST
    }
    
    # If no app_ids provided, use some popular iOS apps with bundle identifiers
    if not app_ids:
        app_ids = [
            "com.facebook.Facebook",      # Facebook
            "net.whatsapp.WhatsApp",      # WhatsApp
            "com.burbn.instagram",        # Instagram
            "com.atebits.Tweetie2",       # Twitter (X)
            "com.zhiliaoapp.musically",   # TikTok
            "com.netflix.Netflix",        # Netflix
            "com.google.Gmail",           # Gmail
            "com.spotify.client",         # Spotify
        ]
    
    app_data = []
    apps_to_fetch = app_ids[:max_apps]
    
    logger.info(f"Fetching data for {len(apps_to_fetch)} apps from App Store")
    
    for app_id in apps_to_fetch:
        try:
            # Try with bundle identifier format
            querystring = {"bundle_id": app_id, "country": "us"}
            response = requests.get(url, headers=headers, params=querystring)
            
            if response.status_code == 200:
                data = response.json()
                # Try different field mappings based on API response structure
                app_data.append({
                    'app_id': app_id,
                    'name': data.get('name', data.get('title', data.get('trackName', ''))),
                    'category': data.get('genre', data.get('category', data.get('primaryGenreName', ''))),
                    'rating': data.get('averageUserRating', data.get('rating', data.get('averageRating', 0))),
                    'review_count': data.get('userRatingCount', data.get('reviewCount', data.get('ratingCount', 0))),
                    'price': data.get('price', data.get('trackPrice', 0)),
                    'developer': data.get('artistName', data.get('developer', data.get('sellerName', ''))),
                    'size_bytes': data.get('fileSizeBytes', data.get('size', 0)),
                    'last_updated': data.get('currentVersionReleaseDate', data.get('updated', data.get('versionReleaseDate', ''))),
                    'version': data.get('version', data.get('currentVersion', '')),
                    'description': str(data.get('description', data.get('appDescription', '')))[:200]
                })
                logger.info(f"Successfully fetched data for app {app_id}")
            else:
                logger.warning(f"Failed to fetch data for app {app_id}: {response.status_code}")
                # Try alternative endpoint or parameters
                logger.info(f"Trying alternative approach for {app_id}")
            
            # Rate limiting
            time.sleep(2)  # Increased delay for rate limits
            
        except Exception as e:
            logger.error(f"Error fetching data for app {app_id}: {str(e)}")
            continue
    
    if not app_data:
        logger.warning("No App Store data fetched, using sample data")
        return self._create_sample_appstore_data()
    
    logger.info(f"Successfully fetched data for {len(app_data)} apps")
    return pd.DataFrame(app_data)

    def _create_sample_appstore_data(self) -> pd.DataFrame:
        """Create sample App Store data for testing"""
        import faker
        fake = faker.Faker()
        
        categories = ['Games', 'Social Networking', 'Productivity', 'Education', 'Health & Fitness', 'Finance']
        
        data = []
        for i in range(200):
            data.append({
                'app_id': str(fake.random_int(min=100000000, max=999999999)),
                'name': fake.word().title() + ' App',
                'category': fake.random_element(categories),
                'rating': fake.random_int(min=10, max=50) / 10,
                'review_count': fake.random_int(min=100, max=500000),
                'price': 0 if fake.boolean(70) else fake.random_int(min=1, max=20),
                'developer': fake.company(),
                'size_bytes': fake.random_int(min=10000000, max=500000000),
                'last_updated': fake.date_this_year(),
                'version': f"{fake.random_int(1, 10)}.{fake.random_int(0, 9)}.{fake.random_int(0, 9)}",
                'description': fake.text(max_nb_chars=200)
            })
        
        return pd.DataFrame(data)

    def create_unified_schema(self, playstore_df: pd.DataFrame, appstore_df: pd.DataFrame) -> pd.DataFrame:
        """Combine both datasets into unified schema"""
        logger.info("Creating unified schema for combined dataset")
        
        # Map Play Store data to unified schema
        playstore_mapped = playstore_df.rename(columns={
            'App': 'name',
            'Category': 'category',
            'Rating': 'rating',
            'Reviews': 'review_count',
            'Size': 'size_original',
            'Installs': 'installs_original',
            'Type': 'type',
            'Price': 'price_original',
            'Content Rating': 'content_rating',
            'Last Updated': 'last_updated'
        })[['name', 'category', 'rating', 'review_count', 'size_original', 
            'installs_original', 'type', 'price_original', 'content_rating', 'last_updated']]
        
        playstore_mapped['platform'] = 'android'
        playstore_mapped['source'] = 'play_store'
        playstore_mapped['app_id'] = playstore_mapped['name'].str.lower().str.replace(' ', '_') + '_android'
        
        # Map App Store data to unified schema
        if not appstore_df.empty:
            appstore_mapped = appstore_df.rename(columns={
                'name': 'name',
                'category': 'category',
                'rating': 'rating',
                'review_count': 'review_count',
                'price': 'price_original'
            })[['app_id', 'name', 'category', 'rating', 'review_count', 'price_original', 
                'developer', 'size_bytes', 'last_updated']]
            
            appstore_mapped['platform'] = 'ios'
            appstore_mapped['source'] = 'app_store'
            appstore_mapped['type'] = 'Free'
            appstore_mapped['content_rating'] = 'Unknown'
            appstore_mapped['size_original'] = appstore_mapped['size_bytes'].apply(
                lambda x: f"{x/(1024*1024):.1f}M" if not pd.isna(x) else 'Varies with device'
            )
            appstore_mapped['installs_original'] = 'Not Available'
            
            # Combine both datasets
            combined_df = pd.concat([playstore_mapped, appstore_mapped], ignore_index=True, sort=False)
        else:
            combined_df = playstore_mapped
        
        # Fill missing values
        combined_df['rating'] = pd.to_numeric(combined_df['rating'], errors='coerce').fillna(0)
        combined_df['review_count'] = pd.to_numeric(combined_df['review_count'], errors='coerce').fillna(0)
        
        logger.info(f"Unified dataset created with {len(combined_df)} total records")
        return combined_df

    def save_clean_data(self, df: pd.DataFrame, filename: str = "combined_apps_data.csv"):
        """Save cleaned combined dataset"""
        os.makedirs(Config.DATA_PROCESSED_PATH, exist_ok=True)
        filepath = os.path.join(Config.DATA_PROCESSED_PATH, filename)
        
        try:
            df.to_csv(filepath, index=False)
            logger.info(f"Saved clean data to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving clean data: {str(e)}")
            return None