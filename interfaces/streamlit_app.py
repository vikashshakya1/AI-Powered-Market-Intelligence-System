import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import os
from utils.config import Config
from utils.helpers import load_json

class StreamlitApp:
    def __init__(self):
        self.insights_file = os.path.join(Config.DATA_OUTPUTS_PATH, "market_insights.json")
        self.d2c_insights_file = os.path.join(Config.DATA_OUTPUTS_PATH, "d2c_insights.json")
        self.insights = load_json(self.insights_file)
        self.d2c_insights = load_json(self.d2c_insights_file)
        
    def run(self):
        """Run the Streamlit application"""
        st.set_page_config(
            page_title="AI Market Intelligence",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS
        st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .section-header {
            font-size: 1.5rem;
            color: #2e86ab;
            border-bottom: 2px solid #2e86ab;
            padding-bottom: 0.5rem;
            margin-top: 2rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #2e86ab;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Header
        st.markdown('<h1 class="main-header">🤖 AI-Powered Market Intelligence</h1>', unsafe_allow_html=True)
        
        # Sidebar
        st.sidebar.title("Navigation")
        app_mode = st.sidebar.selectbox(
            "Choose Analysis Mode",
            ["Market Intelligence", "D2C eCommerce Insights", "Executive Summary"]
        )
        
        if app_mode == "Market Intelligence":
            self.render_market_intelligence()
        elif app_mode == "D2C eCommerce Insights":
            self.render_d2c_insights()
        else:
            self.render_executive_summary()
    
    def render_market_intelligence(self):
        """Render market intelligence insights"""
        if not self.insights:
            st.error("❌ No market insights found. Please generate insights first.")
            return
        
        # Overview Metrics
        st.markdown('<h2 class="section-header">📊 Market Overview</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            confidence = self.insights.get('confidence_metrics', {}).get('overall_confidence', 0)
            st.metric("Overall Confidence", f"{confidence:.1%}")
        
        with col2:
            total_apps = self.insights.get('summary', {}).get('total_apps_analyzed', 0)
            st.metric("Apps Analyzed", f"{total_apps:,}")
        
        with col3:
            data_quality = self.insights.get('confidence_metrics', {}).get('data_quality_score', 0)
            st.metric("Data Quality Score", f"{data_quality:.1%}")
        
        with col4:
            findings_count = self.insights.get('summary', {}).get('key_findings_count', 0)
            st.metric("Key Findings", f"{findings_count}")
        
        # Market Trends
        st.markdown('<h2 class="section-header">📈 Market Trends</h2>', unsafe_allow_html=True)
        
        trends = self.insights.get('insights', {}).get('market_trends', {})
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🚀 Emerging Categories")
            emerging_cats = trends.get('emerging_categories', [])
            for i, cat in enumerate(emerging_cats[:5], 1):
                st.write(f"{i}. {cat}")
        
        with col2:
            st.subheader("💡 Growth Opportunities")
            opportunities = trends.get('growth_opportunities', [])
            for i, opp in enumerate(opportunities[:3], 1):
                st.write(f"{i}. {opp}")
        
        # Competitive Analysis
        st.markdown('<h2 class="section-header">🏆 Competitive Analysis</h2>', unsafe_allow_html=True)
        
        competitive = self.insights.get('insights', {}).get('competitive_analysis', {})
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("💰 Pricing Strategies")
            strategies = competitive.get('pricing_strategies', [])
            for strategy in strategies[:3]:
                st.write(f"• {strategy}")
        
        with col2:
            st.subheader("⭐ Quality Indicators")
            indicators = competitive.get('quality_indicators', [])
            for indicator in indicators[:3]:
                st.write(f"• {indicator}")
        
        # Strategic Recommendations
        st.markdown('<h2 class="section-header">🎯 Strategic Recommendations</h2>', unsafe_allow_html=True)
        
        recommendations = self.insights.get('recommendation_priority', {})
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🚀 High Priority")
            high_priority = recommendations.get('high_priority', [])
            for item in high_priority[:2]:
                st.write(f"• {item}")
        
        with col2:
            st.subheader("📈 Medium Priority")
            medium_priority = recommendations.get('medium_priority', [])
            for item in medium_priority[:2]:
                st.write(f"• {item}")
        
        with col3:
            st.subheader("⚠️ Risk Factors")
            risks = recommendations.get('considerations', [])
            for risk in risks[:2]:
                st.write(f"• {risk}")
    
    def render_d2c_insights(self):
        """Render D2C eCommerce insights"""
        if not self.d2c_insights:
            st.error("❌ No D2C insights found. Please run D2C analysis first.")
            return
        
        # Key Metrics
        st.markdown('<h2 class="section-header">🛍️ D2C eCommerce Performance</h2>', unsafe_allow_html=True)
        
        metrics = self.d2c_insights.get('business_metrics', {})
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Average ROAS", f"{metrics.get('average_roas', 0):.2f}")
        
        with col2:
            st.metric("Average CAC", f"${metrics.get('average_cac', 0):.2f}")
        
        with col3:
            st.metric("Total Revenue", f"${metrics.get('total_revenue', 0):,.0f}")
        
        with col4:
            st.metric("Total Conversions", f"{metrics.get('total_conversions', 0):,}")
        
        # Funnel Analysis
        st.markdown('<h2 class="section-header">📊 Funnel Performance</h2>', unsafe_allow_html=True)
        
        funnel = self.d2c_insights.get('funnel_analysis', {})
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Install → Signup", f"{funnel.get('install_to_signup', 0):.2%}")
        
        with col2:
            st.metric("Signup → Purchase", f"{funnel.get('signup_to_purchase', 0):.2%}")
        
        with col3:
            st.metric("Retention Rate", f"{funnel.get('retention_rate', 0):.2%}")
        
        with col4:
            st.metric("Overall Conversion", f"{funnel.get('overall_conversion_rate', 0):.2%}")
        
        # Creative Recommendations
        st.markdown('<h2 class="section-header">🎨 AI-Generated Creatives</h2>', unsafe_allow_html=True)
        
        creatives = self.d2c_insights.get('creative_recommendations', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📢 Ad Headline")
            st.info(creatives.get('ad_headline', 'N/A'))
            
            st.subheader("🔍 Meta Description")
            st.info(creatives.get('seo_meta_description', 'N/A'))
        
        with col2:
            st.subheader("📝 Product Description")
            st.text_area("PDP Text", creatives.get('pdp_text', 'N/A'), height=150)
        
        # SEO Opportunities
        st.markdown('<h2 class="section-header">🚀 SEO Opportunities</h2>', unsafe_allow_html=True)
        
        seo = self.d2c_insights.get('seo_opportunities', {})
        seo_gap = seo.get('seo_gap_analysis', {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Estimated Traffic Gain", f"{seo_gap.get('estimated_traffic_gain', 0):,}")
        
        with col2:
            st.metric("Revenue Opportunity", f"${seo_gap.get('revenue_opportunity', 0):,.0f}")
    
    def render_executive_summary(self):
        """Render executive summary dashboard"""
        st.markdown('<h2 class="section-header">📋 Executive Summary</h2>', unsafe_allow_html=True)
        
        # Market Intelligence Summary
        if self.insights:
            st.subheader("📱 Mobile App Market Intelligence")
            
            insights_data = self.insights.get('insights', {})
            trends = insights_data.get('market_trends', {})
            recommendations = insights_data.get('strategic_recommendations', {})
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Key Market Trends:**")
                emerging_cats = trends.get('emerging_categories', [])
                for cat in emerging_cats[:3]:
                    st.write(f"• {cat}")
                
                st.write("**Growth Opportunities:**")
                opportunities = trends.get('growth_opportunities', [])
                for opp in opportunities[:2]:
                    st.write(f"• {opp}")
            
            with col2:
                st.write("**Strategic Recommendations:**")
                dev_opps = recommendations.get('developer_opportunities', [])
                for opp in dev_opps[:2]:
                    st.write(f"• {opp}")
                
                st.write("**Investment Priorities:**")
                investments = recommendations.get('investment_priorities', [])
                for inv in investments[:2]:
                    st.write(f"• {inv}")
        
        # D2C Summary
        if self.d2c_insights:
            st.subheader("🛍️ D2C eCommerce Performance")
            
            metrics = self.d2c_insights.get('business_metrics', {})
            strategic_recs = self.d2c_insights.get('strategic_recommendations', {})
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Performance Metrics:**")
                st.write(f"• Average ROAS: {metrics.get('average_roas', 0):.2f}")
                st.write(f"• Average CAC: ${metrics.get('average_cac', 0):.2f}")
                st.write(f"• Total Revenue: ${metrics.get('total_revenue', 0):,.0f}")
            
            with col2:
                st.write("**Optimization Priorities:**")
                budget_recs = strategic_recs.get('budget_reallocation', {})
                increase_cats = budget_recs.get('increase_spend_categories', [])
                for cat in increase_cats[:2]:
                    st.write(f"• Increase spend in {cat}")
                
                immediate_actions = strategic_recs.get('optimization_priorities', {}).get('immediate_actions', [])
                for action in immediate_actions[:1]:
                    st.write(f"• {action}")
        
        # Confidence Scores
        st.markdown('<h2 class="section-header">🎯 Confidence Assessment</h2>', unsafe_allow_html=True)
        
        if self.insights:
            confidence = self.insights.get('confidence_metrics', {})
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                score = confidence.get('overall_confidence', 0)
                st.metric("Overall Confidence", f"{score:.1%}")
                st.progress(score)
            
            with col2:
                score = confidence.get('data_quality_score', 0)
                st.metric("Data Quality", f"{score:.1%}")
                st.progress(score)
            
            with col3:
                score = confidence.get('statistical_significance', 0)
                st.metric("Statistical Significance", f"{score:.1%}")
                st.progress(score)

def main():
    app = StreamlitApp()
    app.run()

if __name__ == "__main__":
    main()