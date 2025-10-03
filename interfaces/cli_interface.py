import json
import pandas as pd
from typing import Dict, List
import os
import logging
from utils.config import Config
from utils.helpers import load_json

logger = logging.getLogger(__name__)

class CLIInterface:
    def __init__(self, insights_file: str = None, d2c_insights_file: str = None):
        if insights_file is None:
            insights_file = os.path.join(Config.DATA_OUTPUTS_PATH, "market_insights.json")
        if d2c_insights_file is None:
            d2c_insights_file = os.path.join(Config.DATA_OUTPUTS_PATH, "d2c_insights.json")
            
        self.insights_file = insights_file
        self.d2c_insights_file = d2c_insights_file
        self.insights = self._load_insights()
        self.d2c_insights = self._load_d2c_insights()
    
    def _load_insights(self) -> Dict:
        """Load market insights from JSON file"""
        insights = load_json(self.insights_file)
        if not insights:
            print("❌ Market insights file not found or empty. Please generate insights first.")
        return insights
    
    def _load_d2c_insights(self) -> Dict:
        """Load D2C insights from JSON file"""
        insights = load_json(self.d2c_insights_file)
        return insights
    
    def display_main_menu(self):
        """Display main menu options"""
        print("\n" + "="*60)
        print("🤖 AI-Powered Market Intelligence System")
        print("="*60)
        print("1.  Market Trends Analysis")
        print("2.  Competitive Insights") 
        print("3.  Strategic Recommendations")
        print("4.  Consumer Behavior Analysis")
        print("5.  Statistical Backing & Confidence Scores")
        print("6.  D2C eCommerce Insights")
        print("7.  D2C Funnel & SEO Analysis")
        print("8.  D2C Creative Recommendations")
        print("9.  Export Full Report")
        print("0.  Exit")
        print("="*60)
    
    def show_market_trends(self):
        """Display market trends insights"""
        if not self.insights:
            return
            
        trends = self.insights.get('insights', {}).get('market_trends', {})
        stats = self.insights.get('statistical_backing', {}).get('category_performance', {})
        
        print("\n📈 MARKET TRENDS ANALYSIS")
        print("-" * 50)
        
        print("\n🚀 Emerging Categories (High Growth Potential):")
        for i, category in enumerate(trends.get('emerging_categories', [])[:5], 1):
            confidence = stats.get('confidence_scores', {}).get(category, 'N/A')
            print(f"   {i}. {category} (Confidence: {confidence})")
        
        print(f"\n🎯 Saturation Analysis:")
        print(f"   {trends.get('saturation_analysis', 'N/A')}")
        
        print(f"\n💡 Growth Opportunities:")
        for i, opportunity in enumerate(trends.get('growth_opportunities', [])[:3], 1):
            print(f"   {i}. {opportunity}")
        
        print(f"\n📊 Market Maturity Assessment:")
        print(f"   {trends.get('market_maturity', 'N/A')}")
    
    def show_competitive_analysis(self):
        """Display competitive insights"""
        if not self.insights:
            return
            
        competitive = self.insights.get('insights', {}).get('competitive_analysis', {})
        
        print("\n🏆 COMPETITIVE ANALYSIS")
        print("-" * 50)
        
        print(f"\n📊 Top Performers Analysis:")
        print(f"   {competitive.get('top_performers_analysis', 'N/A')}")
        
        print(f"\n💰 Pricing Strategies:")
        for i, strategy in enumerate(competitive.get('pricing_strategies', [])[:3], 1):
            print(f"   {i}. {strategy}")
        
        print(f"\n⭐ Quality Indicators (Success Factors):")
        for i, indicator in enumerate(competitive.get('quality_indicators', [])[:3], 1):
            print(f"   {i}. {indicator}")
        
        print(f"\n⚡ Competitive Intensity:")
        print(f"   {competitive.get('competitive_intensity', 'N/A')}")
    
    def show_recommendations(self):
        """Display strategic recommendations"""
        if not self.insights:
            return
            
        recommendations = self.insights.get('insights', {}).get('strategic_recommendations', {})
        priority = self.insights.get('recommendation_priority', {})
        
        print("\n🎯 STRATEGIC RECOMMENDATIONS")
        print("-" * 50)
        
        print(f"\n💻 HIGH PRIORITY - Developer Opportunities:")
        for i, opportunity in enumerate(priority.get('high_priority', [])[:3], 1):
            print(f"   {i}. {opportunity}")
        
        print(f"\n📈 MEDIUM PRIORITY - Investment Priorities:")
        for i, priority_item in enumerate(priority.get('medium_priority', [])[:3], 1):
            print(f"   {i}. {priority_item}")
        
        print(f"\n⚠️  RISK FACTORS & CONSIDERATIONS:")
        for i, risk in enumerate(priority.get('considerations', [])[:3], 1):
            print(f"   {i}. {risk}")
        
        print(f"\n⏰ Timing Recommendations:")
        print(f"   {recommendations.get('timing_recommendations', 'N/A')}")
    
    def show_consumer_insights(self):
        """Display consumer behavior insights"""
        if not self.insights:
            return
            
        consumer = self.insights.get('insights', {}).get('consumer_insights', {})
        
        print("\n👥 CONSUMER INSIGHTS")
        print("-" * 50)
        
        print(f"\n❤️  User Preference Patterns:")
        for i, pattern in enumerate(consumer.get('preference_patterns', [])[:3], 1):
            print(f"   {i}. {pattern}")
        
        print(f"\n⭐ Rating & Review Behavior:")
        print(f"   {consumer.get('rating_behavior', 'N/A')}")
        
        print(f"\n📱 App Adoption Drivers:")
        for i, factor in enumerate(consumer.get('adoption_factors', [])[:3], 1):
            print(f"   {i}. {factor}")
        
        print(f"\n🔗 User Retention Drivers:")
        for i, driver in enumerate(consumer.get('retention_drivers', [])[:3], 1):
            print(f"   {i}. {driver}")
    
    def show_statistical_backing(self):
        """Display statistical analysis and confidence scores"""
        if not self.insights:
            return
            
        stats = self.insights.get('statistical_backing', {})
        confidence = self.insights.get('confidence_metrics', {})
        
        print("\n📊 STATISTICAL BACKING & CONFIDENCE SCORES")
        print("-" * 55)
        
        print(f"\n🎯 Overall Confidence Metrics:")
        for metric, score in confidence.items():
            print(f"   • {metric.replace('_', ' ').title()}: {score}")
        
        if 'category_performance' in stats:
            print(f"\n📈 Top Categories by Confidence Score:")
            cat_stats = stats['category_performance'].get('confidence_scores', {})
            for category, score in sorted(cat_stats.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"   • {category}: {score}")
        
        if 'data_quality' in stats:
            data_quality = stats['data_quality']
            print(f"\n📋 Data Quality Assessment:")
            print(f"   • Total Records: {data_quality.get('total_records', 0):,}")
            print(f"   • Data Completeness Score: {data_quality.get('completeness_score', 0)}")
            print(f"   • Missing Ratings: {data_quality.get('missing_ratings', 0)}")
    
    def show_d2c_insights(self):
        """Display D2C eCommerce insights"""
        if not self.d2c_insights:
            print("❌ D2C insights not found. Please run D2C analysis first.")
            return
            
        metrics = self.d2c_insights.get('business_metrics', {})
        
        print("\n🛍️ D2C eCOMMERCE INSIGHTS")
        print("-" * 50)
        
        print(f"\n💰 Key Business Metrics:")
        print(f"   • Average ROAS: {metrics.get('average_roas', 0):.2f}")
        print(f"   • Average CAC: ${metrics.get('average_cac', 0):.2f}")
        print(f"   • Average CTR: {metrics.get('average_ctr', 0):.4f}")
        print(f"   • Total Revenue: ${metrics.get('total_revenue', 0):,.2f}")
        print(f"   • Total Conversions: {metrics.get('total_conversions', 0):,}")
        
        funnel = self.d2c_insights.get('funnel_analysis', {})
        print(f"\n📊 Funnel Performance:")
        print(f"   • Install → Signup: {funnel.get('install_to_signup', 0):.2%}")
        print(f"   • Signup → Purchase: {funnel.get('signup_to_purchase', 0):.2%}")
        print(f"   • Customer Retention: {funnel.get('retention_rate', 0):.2%}")
        print(f"   • Overall Conversion: {funnel.get('overall_conversion_rate', 0):.2%}")
    
    def show_d2c_funnel_seo(self):
        """Display D2C funnel and SEO analysis"""
        if not self.d2c_insights:
            return
            
        funnel = self.d2c_insights.get('funnel_analysis', {})
        seo = self.d2c_insights.get('seo_opportunities', {})
        
        print("\n🎯 D2C FUNNEL & SEO ANALYSIS")
        print("-" * 50)
        
        print(f"\n🔍 Funnel Leakage Analysis:")
        leakage = funnel.get('funnel_leakage_analysis', {})
        if 'biggest_leakage_points' in leakage:
            print("   Biggest Conversion Drop-offs:")
            for point, rate in leakage['biggest_leakage_points']:
                print(f"   • {point.replace('_', ' ').title()}: {rate:.2%}")
        
        print(f"\n🚀 SEO Growth Opportunities:")
        seo_gap = seo.get('seo_gap_analysis', {})
        print(f"   • Estimated Traffic Gain: {seo_gap.get('estimated_traffic_gain', 0):,} visits")
        print(f"   • Revenue Opportunity: ${seo_gap.get('revenue_opportunity', 0):,.2f}")
        
        print(f"\n🎯 Optimization Priorities:")
        priorities = funnel.get('funnel_leakage_analysis', {}).get('optimization_priority', [])
        for i, priority in enumerate(priorities[:3], 1):
            print(f"   {i}. {priority.replace('_', ' ').title()}")
    
    def show_d2c_creatives(self):
        """Display D2C creative recommendations"""
        if not self.d2c_insights:
            return
            
        creatives = self.d2c_insights.get('creative_recommendations', {})
        
        print("\n🎨 D2C AI-GENERATED CREATIVE RECOMMENDATIONS")
        print("-" * 55)
        
        print(f"\n📢 HIGH-CONVERTING AD HEADLINE:")
        print(f"   '{creatives.get('ad_headline', 'N/A')}'")
        
        print(f"\n🔍 SEO-OPTIMIZED META DESCRIPTION:")
        print(f"   '{creatives.get('seo_meta_description', 'N/A')}'")
        
        print(f"\n📝 PERSUASIVE PRODUCT DESCRIPTION:")
        print(f"   {creatives.get('pdp_text', 'N/A')}")
        
        if 'cta_optimization' in creatives:
            print(f"\n💡 CTA OPTIMIZATION TIPS:")
            for tip in creatives['cta_optimization'][:3]:
                print(f"   • {tip}")
    
    def export_report(self):
        """Export insights to various formats"""
        from reports.report_generator import ReportGenerator
        
        generator = ReportGenerator()
        
        # Generate market intelligence report
        if self.insights:
            report_path = generator.generate_report(self.insights, "market_intelligence")
            print(f"📄 Market Intelligence Report: {report_path}")
        else:
            print("❌ No market insights available to export")
        
        # Generate D2C report
        if self.d2c_insights:
            d2c_report_path = generator.generate_d2c_report(self.d2c_insights)
            print(f"📊 D2C Insights Report: {d2c_report_path}")
        else:
            print("❌ No D2C insights available to export")
    
    def run(self):
        """Main CLI loop"""
        while True:
            self.display_main_menu()
            choice = input("\nEnter your choice (0-9): ").strip()
            
            if choice == '1':
                self.show_market_trends()
            elif choice == '2':
                self.show_competitive_analysis()
            elif choice == '3':
                self.show_recommendations()
            elif choice == '4':
                self.show_consumer_insights()
            elif choice == '5':
                self.show_statistical_backing()
            elif choice == '6':
                self.show_d2c_insights()
            elif choice == '7':
                self.show_d2c_funnel_seo()
            elif choice == '8':
                self.show_d2c_creatives()
            elif choice == '9':
                self.export_report()
            elif choice == '0':
                print("\nThank you for using the AI Market Intelligence System! 👋")
                break
            else:
                print("❌ Invalid choice. Please try again.")
            
            if choice != '0':
                input("\nPress Enter to continue...")