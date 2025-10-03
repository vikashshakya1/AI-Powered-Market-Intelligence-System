import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any
from utils.helpers import safe_divide, save_json
from utils.config import Config

logger = logging.getLogger(__name__)

class D2CAnalyzer:
    def __init__(self, llm_generator=None):
        self.llm_generator = llm_generator
    
    def load_d2c_data(self, file_path: str) -> pd.DataFrame:
        """Load D2C eCommerce dataset from Excel"""
        try:
            df = pd.read_excel(file_path)
            logger.info(f"Loaded D2C dataset with {len(df)} records and {len(df.columns)} columns")
            logger.info(f"Columns: {list(df.columns)}")
            return df
        except Exception as e:
            logger.error(f"Error loading D2C data: {str(e)}")
            # Return sample data for demonstration
            return self._create_sample_d2c_data()
    
    def _create_sample_d2c_data(self) -> pd.DataFrame:
        """Create sample D2C data for testing"""
        import faker
        fake = faker.Faker()
        
        categories = ['Electronics', 'Fashion', 'Home & Garden', 'Beauty', 'Sports', 'Books']
        campaigns = [f'Campaign_{i}' for i in range(1, 21)]
        
        data = []
        for i in range(500):
            campaign = fake.random_element(campaigns)
            category = fake.random_element(categories)
            spend = fake.random_int(min=100, max=10000)
            impressions = fake.random_int(min=1000, max=100000)
            clicks = fake.random_int(min=50, max=5000)
            conversions = fake.random_int(min=1, max=500)
            revenue = conversions * fake.random_int(min=20, max=200)
            
            data.append({
                'campaign_id': campaign,
                'category': category,
                'ad_spend': spend,
                'impressions': impressions,
                'clicks': clicks,
                'conversions': conversions,
                'revenue': revenue,
                'installs': fake.random_int(min=conversions, max=conversions * 2),
                'signups': fake.random_int(min=conversions, max=conversions),
                'first_purchase': conversions,
                'repeat_purchase': fake.random_int(min=0, max=conversions // 2),
                'search_volume': fake.random_int(min=1000, max=100000),
                'average_position': fake.random_int(min=1, max=20),
                'conversion_rate': fake.random_int(min=1, max=20) / 100
            })
        
        return pd.DataFrame(data)
    
    def analyze_funnel_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze D2C funnel metrics and calculate key business metrics"""
        logger.info("Analyzing D2C funnel metrics")
        
        insights = {}
        
        try:
            # Calculate key metrics
            df['cac'] = df.apply(lambda x: safe_divide(x['ad_spend'], x['conversions']), axis=1)
            df['roas'] = df.apply(lambda x: safe_divide(x['revenue'], x['ad_spend']), axis=1)
            df['ctr'] = df.apply(lambda x: safe_divide(x['clicks'], x['impressions']), axis=1)
            df['cpc'] = df.apply(lambda x: safe_divide(x['ad_spend'], x['clicks']), axis=1)
            
            # Funnel conversion rates
            df['install_to_signup_rate'] = df.apply(lambda x: safe_divide(x['signups'], x['installs']), axis=1)
            df['signup_to_purchase_rate'] = df.apply(lambda x: safe_divide(x['first_purchase'], x['signups']), axis=1)
            df['retention_rate'] = df.apply(lambda x: safe_divide(x['repeat_purchase'], x['first_purchase']), axis=1)
            df['overall_conversion_rate'] = df.apply(lambda x: safe_divide(x['conversions'], x['clicks']), axis=1)
            
            # Category performance analysis
            category_insights = df.groupby('category').agg({
                'cac': 'mean',
                'roas': 'mean',
                'revenue': 'sum',
                'conversions': 'sum',
                'ad_spend': 'sum',
                'ctr': 'mean',
                'overall_conversion_rate': 'mean'
            }).round(3)
            
            # Campaign performance analysis
            campaign_insights = df.groupby('campaign_id').agg({
                'roas': 'mean',
                'revenue': 'sum',
                'conversions': 'sum',
                'cac': 'mean'
            }).round(3)
            
            # SEO opportunity analysis
            seo_opportunities = self._analyze_seo_opportunities(df)
            
            # Generate creative recommendations
            creative_recommendations = self._generate_creative_recommendations(df)
            
            insights = {
                'business_metrics': {
                    'average_cac': round(df['cac'].mean(), 2),
                    'average_roas': round(df['roas'].mean(), 2),
                    'average_ctr': round(df['ctr'].mean(), 4),
                    'average_cpc': round(df['cpc'].mean(), 2),
                    'total_revenue': df['revenue'].sum(),
                    'total_conversions': df['conversions'].sum(),
                    'total_ad_spend': df['ad_spend'].sum()
                },
                'funnel_analysis': {
                    'install_to_signup': round(df['install_to_signup_rate'].mean(), 4),
                    'signup_to_purchase': round(df['signup_to_purchase_rate'].mean(), 4),
                    'retention_rate': round(df['retention_rate'].mean(), 4),
                    'overall_conversion_rate': round(df['overall_conversion_rate'].mean(), 4),
                    'funnel_leakage_analysis': self._analyze_funnel_leakage(df)
                },
                'category_performance': {
                    'top_categories_by_roas': category_insights.nlargest(3, 'roas')[['roas', 'revenue']].to_dict(),
                    'top_categories_by_revenue': category_insights.nlargest(3, 'revenue')[['revenue', 'roas']].to_dict(),
                    'most_efficient_categories': category_insights.nlargest(3, 'overall_conversion_rate')[['overall_conversion_rate', 'cac']].to_dict(),
                    'category_benchmarks': category_insights.agg({
                        'roas': ['mean', 'std'],
                        'cac': ['mean', 'std'],
                        'ctr': ['mean', 'std']
                    }).to_dict()
                },
                'campaign_insights': {
                    'top_performing_campaigns': campaign_insights.nlargest(5, 'roas').to_dict(),
                    'campaign_efficiency_analysis': self._analyze_campaign_efficiency(df)
                },
                'seo_opportunities': seo_opportunities,
                'creative_recommendations': creative_recommendations,
                'strategic_recommendations': self._generate_strategic_recommendations(df, category_insights)
            }
            
            logger.info("D2C analysis completed successfully")
            
        except Exception as e:
            logger.error(f"Error in D2C analysis: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
        
        return insights
    
    def _analyze_seo_opportunities(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Identify SEO growth opportunities"""
        
        # Calculate SEO efficiency score
        df['seo_efficiency'] = (df['search_volume'] * df['conversion_rate']) / (df['average_position'] + 1)
        
        # Identify high-opportunity categories (high search volume but poor positioning)
        opportunity_analysis = df.groupby('category').agg({
            'seo_efficiency': 'mean',
            'search_volume': 'mean',
            'conversion_rate': 'mean',
            'average_position': 'mean',
            'revenue': 'sum'
        }).round(3)
        
        # High opportunity: good search volume but poor average position
        high_opportunity = opportunity_analysis[
            (opportunity_analysis['search_volume'] > opportunity_analysis['search_volume'].median()) &
            (opportunity_analysis['average_position'] > 5) &
            (opportunity_analysis['conversion_rate'] > opportunity_analysis['conversion_rate'].median())
        ]
        
        # Quick wins: good position but low conversion rate optimization
        quick_wins = opportunity_analysis[
            (opportunity_analysis['average_position'] <= 5) &
            (opportunity_analysis['conversion_rate'] < opportunity_analysis['conversion_rate'].median())
        ]
        
        return {
            'high_opportunity_categories': high_opportunity.to_dict(),
            'quick_win_opportunities': quick_wins.to_dict(),
            'top_seo_performers': opportunity_analysis.nlargest(3, 'seo_efficiency').to_dict(),
            'seo_gap_analysis': {
                'estimated_traffic_gain': round(high_opportunity['search_volume'].sum() * 0.3),  # 30% improvement estimate
                'revenue_opportunity': round(high_opportunity['revenue'].sum() * 0.25)  # 25% revenue lift estimate
            }
        }
    
    def _analyze_funnel_leakage(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze where the funnel has the biggest drop-offs"""
        avg_rates = {
            'impression_to_click': df['ctr'].mean(),
            'click_to_conversion': df['overall_conversion_rate'].mean(),
            'install_to_signup': df['install_to_signup_rate'].mean(),
            'signup_to_purchase': df['signup_to_purchase_rate'].mean(),
            'first_to_repeat_purchase': df['retention_rate'].mean()
        }
        
        # Identify biggest drop-off points
        leakage_points = sorted(avg_rates.items(), key=lambda x: x[1])
        
        return {
            'conversion_rates': avg_rates,
            'biggest_leakage_points': leakage_points[:2],  # Two worst conversion points
            'optimization_priority': [point[0] for point in leakage_points[:3]]
        }
    
    def _analyze_campaign_efficiency(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Analyze campaign performance and efficiency"""
        campaign_stats = df.groupby('campaign_id').agg({
            'roas': ['mean', 'std'],
            'cac': 'mean',
            'revenue': 'sum',
            'conversions': 'sum'
        }).round(3)
        
        # Flatten column names
        campaign_stats.columns = ['_'.join(col).strip() for col in campaign_stats.columns.values]
        
        # Classify campaigns
        high_performers = campaign_stats[campaign_stats['roas_mean'] > campaign_stats['roas_mean'].quantile(0.75)]
        low_performers = campaign_stats[campaign_stats['roas_mean'] < campaign_stats['roas_mean'].quantile(0.25)]
        
        return {
            'campaign_count': len(campaign_stats),
            'high_performer_count': len(high_performers),
            'low_performer_count': len(low_performers),
            'performance_gap_analysis': {
                'roas_gap': high_performers['roas_mean'].mean() - low_performers['roas_mean'].mean(),
                'revenue_gap': high_performers['revenue_sum'].mean() - low_performers['revenue_sum'].mean()
            }
        }
    
    def _generate_creative_recommendations(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate AI-powered creative recommendations"""
        
        # Get top performing category for creative generation
        top_category = df.groupby('category')['roas'].mean().idxmax()
        top_category_data = df[df['category'] == top_category].iloc[0]
        
        creative_prompt = f"""
        Based on D2C eCommerce performance data for the {top_category} category:
        - Average ROAS: {top_category_data.get('roas', 'N/A'):.2f}
        - Conversion Rate: {top_category_data.get('conversion_rate', 'N/A'):.2%}
        - Customer Acquisition Cost: ${top_category_data.get('cac', 'N/A'):.2f}
        - Target Audience: D2C consumers interested in {top_category}
        
        Generate 3 creative outputs optimized for conversion:
        
        1. AD_HEADLINE: An engaging, click-worthy ad headline (max 60 characters)
        2. SEO_META_DESCRIPTION: Compelling meta description for SEO (max 160 characters)
        3. PDP_TEXT: Persuasive product description page text (2-3 sentences)
        
        Focus on:
        - Emotional benefits over features
        - Urgency and social proof
        - Clear value proposition
        - Mobile-first optimization
        """
        
        try:
            if self.llm_generator and not self.llm_generator.mock_mode:
                creative_outputs = self.llm_generator._call_llm_for_creatives(creative_prompt)
            else:
                creative_outputs = self._generate_fallback_creatives(top_category)
        except:
            creative_outputs = self._generate_fallback_creatives(top_category)
        
        return creative_outputs
    
    def _generate_fallback_creatives(self, category: str) -> Dict[str, Any]:
        """Generate fallback creative content when LLM is unavailable"""
        return {
            "ad_headline": f"Premium {category} - Limited Time Offer!",
            "seo_meta_description": f"Shop the best {category} with free shipping. Premium quality guaranteed. 4.8★ rated. Shop now!",
            "pdp_text": f"Experience exceptional quality with our premium {category} collection. Designed for modern lifestyles using sustainable materials and expert craftsmanship. Join 10,000+ satisfied customers with our 30-day satisfaction guarantee.",
            "cta_optimization": [
                "Add urgency: 'Limited Stock'",
                "Social proof: '10,000+ Sold'",
                "Risk reversal: '30-Day Guarantee'"
            ]
        }
    
    def _generate_strategic_recommendations(self, df: pd.DataFrame, category_insights: pd.DataFrame) -> Dict[str, Any]:
        """Generate strategic recommendations based on data analysis"""
        
        # Identify optimization opportunities
        high_cac_categories = category_insights[category_insights['cac'] > category_insights['cac'].mean()]
        high_roas_categories = category_insights[category_insights['roas'] > category_insights['roas'].mean()]
        
        return {
            'budget_reallocation': {
                'increase_spend_categories': high_roas_categories.nlargest(2, 'roas').index.tolist(),
                'decrease_spend_categories': high_cac_categories.nlargest(2, 'cac').index.tolist(),
                'testing_budget_categories': category_insights[
                    category_insights['roas'].between(
                        category_insights['roas'].quantile(0.4),
                        category_insights['roas'].quantile(0.6)
                    )
                ].index.tolist()
            },
            'optimization_priorities': {
                'immediate_actions': [
                    "Optimize landing pages for lowest conversion funnel stages",
                    "Increase bids on top-performing campaigns by 15-20%",
                    "Pause bottom 10% performing campaigns"
                ],
                'short_term_goals': [
                    "Implement A/B testing for ad creatives",
                    "Develop category-specific SEO content",
                    "Optimize mobile user experience"
                ],
                'long_term_strategies': [
                    "Build email marketing automation",
                    "Develop loyalty program",
                    "Expand to complementary product categories"
                ]
            },
            'kpi_targets': {
                'next_quarter_roas_target': round(category_insights['roas'].mean() * 1.15, 2),  # 15% improvement
                'cac_reduction_target': round(category_insights['cac'].mean() * 0.9, 2),  # 10% reduction
                'conversion_rate_target': round(category_insights['overall_conversion_rate'].mean() * 1.2, 4)  # 20% improvement
            }
        }
    
    def save_d2c_insights(self, insights: Dict[str, Any], filename: str = "d2c_insights.json"):
        """Save D2C insights to JSON file"""
        os.makedirs(Config.DATA_OUTPUTS_PATH, exist_ok=True)
        filepath = os.path.join(Config.DATA_OUTPUTS_PATH, filename)
        
        if save_json(insights, filepath):
            logger.info(f"D2C insights saved to {filepath}")
            return filepath
        else:
            logger.error(f"Failed to save D2C insights to {filepath}")
            return None