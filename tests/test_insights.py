import unittest
import pandas as pd
import numpy as np
import os
import sys

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.llm_insights import LLMInsightsGenerator
from pipelines.d2c_analyzer import D2CAnalyzer

class TestInsightsGeneration(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.llm_generator = LLMInsightsGenerator()  # Will use mock mode
        self.d2c_analyzer = D2CAnalyzer()
        
        # Create sample data for testing
        self.sample_app_data = pd.DataFrame({
            'name': [f'App {i}' for i in range(100)],
            'category': np.random.choice(['GAME', 'SOCIAL', 'PRODUCTIVITY', 'EDUCATION'], 100),
            'rating': np.random.uniform(1, 5, 100),
            'review_count': np.random.randint(100, 100000, 100),
            'platform': np.random.choice(['android', 'ios'], 100),
            'price_original': np.random.choice(['0', '$0.99', '$1.99', '$4.99'], 100),
            'last_updated': pd.date_range('2022-01-01', periods=100, freq='D')
        })
        
        # Create sample D2C data
        self.sample_d2c_data = pd.DataFrame({
            'campaign_id': [f'Campaign_{i}' for i in range(50)],
            'category': np.random.choice(['Electronics', 'Fashion', 'Home'], 50),
            'ad_spend': np.random.uniform(100, 10000, 50),
            'impressions': np.random.randint(1000, 100000, 50),
            'clicks': np.random.randint(50, 5000, 50),
            'conversions': np.random.randint(1, 500, 50),
            'revenue': np.random.uniform(100, 50000, 50),
            'installs': np.random.randint(100, 1000, 50),
            'signups': np.random.randint(50, 500, 50),
            'first_purchase': np.random.randint(10, 200, 50),
            'repeat_purchase': np.random.randint(0, 50, 50),
            'search_volume': np.random.randint(1000, 50000, 50),
            'average_position': np.random.uniform(1, 20, 50),
            'conversion_rate': np.random.uniform(0.01, 0.2, 50)
        })
    
    def test_llm_generator_initialization(self):
        """Test LLM insights generator initialization"""
        self.assertIsInstance(self.llm_generator, LLMInsightsGenerator)
        self.assertTrue(self.llm_generator.mock_mode)  # Should be in mock mode without API key
    
    def test_statistical_insights_calculation(self):
        """Test statistical insights calculation"""
        insights = self.llm_generator._calculate_statistical_insights(self.sample_app_data)
        
        # Check that insights structure is correct
        self.assertIn('category_performance', insights)
        self.assertIn('data_quality', insights)
        
        # Check category performance structure
        cat_perf = insights['category_performance']
        self.assertIn('stats', cat_perf)
        self.assertIn('confidence_scores', cat_perf)
        self.assertIn('top_categories_by_rating', cat_perf)
    
    def test_mock_insights_generation(self):
        """Test mock insights generation"""
        insights = self.llm_generator._generate_mock_insights()
        
        # Check structure of mock insights
        required_sections = ['market_trends', 'competitive_analysis', 'strategic_recommendations', 'consumer_insights']
        for section in required_sections:
            self.assertIn(section, insights)
        
        # Check that lists are populated
        self.assertGreater(len(insights['market_trends']['emerging_categories']), 0)
        self.assertGreater(len(insights['strategic_recommendations']['developer_opportunities']), 0)
    
    def test_d2c_analyzer_initialization(self):
        """Test D2C analyzer initialization"""
        self.assertIsInstance(self.d2c_analyzer, D2CAnalyzer)
    
    def test_d2c_metrics_calculation(self):
        """Test D2C metrics calculation"""
        insights = self.d2c_analyzer.analyze_funnel_metrics(self.sample_d2c_data)
        
        # Check business metrics
        self.assertIn('business_metrics', insights)
        metrics = insights['business_metrics']
        
        # Check that key metrics are calculated
        self.assertIn('average_roas', metrics)
        self.assertIn('average_cac', metrics)
        self.assertIn('total_revenue', metrics)
        
        # Check funnel analysis
        self.assertIn('funnel_analysis', insights)
        funnel = insights['funnel_analysis']
        self.assertIn('install_to_signup', funnel)
        self.assertIn('signup_to_purchase', funnel)
    
    def test_d2c_seo_analysis(self):
        """Test D2C SEO opportunity analysis"""
        seo_insights = self.d2c_analyzer._analyze_seo_opportunities(self.sample_d2c_data)
        
        self.assertIn('high_opportunity_categories', seo_insights)
        self.assertIn('seo_gap_analysis', seo_insights)
        
        gap_analysis = seo_insights['seo_gap_analysis']
        self.assertIn('estimated_traffic_gain', gap_analysis)
        self.assertIn('revenue_opportunity', gap_analysis)
    
    def test_d2c_creative_generation(self):
        """Test D2C creative recommendations generation"""
        creatives = self.d2c_analyzer._generate_fallback_creatives('Electronics')
        
        self.assertIn('ad_headline', creatives)
        self.assertIn('seo_meta_description', creatives)
        self.assertIn('pdp_text', creatives)
        
        # Check that creatives are strings and not empty
        self.assertIsInstance(creatives['ad_headline'], str)
        self.assertGreater(len(creatives['ad_headline']), 0)
        self.assertIsInstance(creatives['seo_meta_description'], str)
        self.assertGreater(len(creatives['seo_meta_description']), 0)

if __name__ == '__main__':
    unittest.main()