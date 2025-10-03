#!/usr/bin/env python3
"""
AI-Powered Market Intelligence System
Main execution script for data pipeline and insights generation
"""

import os
import argparse
import logging
from utils.helpers import setup_logging
from utils.config import Config
from pipelines.data_ingestion import DataIngestion
from pipelines.data_cleaning import DataCleaner
from pipelines.llm_insights import LLMInsightsGenerator
from pipelines.d2c_analyzer import D2CAnalyzer
from interfaces.cli_interface import CLIInterface
from reports.report_generator import ReportGenerator

def _find_d2c_file():
    """Helper to find D2C file in common locations"""
    possible_locations = [
        "d2c_data.xlsx",
        "data/raw/d2c_data.xlsx",
        "d2c_ecommerce_data.xlsx",
        "data/d2c_data.xlsx"
    ]
    
    for location in possible_locations:
        if os.path.exists(location):
            return location
    return None

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="AI-Powered Market Intelligence System")
    parser.add_argument('--rapidapi-key', help='RapidAPI key for App Store data')
    parser.add_argument('--llm-api-key', help='LLM API key (OpenAI/Gemini)')
    parser.add_argument('--llm-provider', choices=['openai', 'gemini'], default='openai')
    parser.add_argument('--d2c-file', help='Path to D2C Excel file')
    parser.add_argument('--playstore-file', help='Path to Play Store CSV file')
    parser.add_argument('--sample-size', type=int, default=1000, help='Sample size for analysis')
    parser.add_argument('--interface', choices=['cli', 'streamlit'], default='cli', help='Interface to use')
    parser.add_argument('--skip-llm', action='store_true', help='Skip LLM insights generation')
    parser.add_argument('--skip-d2c', action='store_true', help='Skip D2C analysis')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Create data directories
    os.makedirs(Config.DATA_RAW_PATH, exist_ok=True)
    os.makedirs(Config.DATA_PROCESSED_PATH, exist_ok=True)
    os.makedirs(Config.DATA_OUTPUTS_PATH, exist_ok=True)
    
    print("🚀 Starting AI-Powered Market Intelligence System...")
    logger.info("System initialization started")
    
    # Validate configuration
    Config.validate_config()
    
    try:
        # Phase 1: Data Pipeline
        print("\n📊 Phase 1: Data Ingestion & Cleaning")
        logger.info("Starting data ingestion phase")
        
        ingestion = DataIngestion(rapidapi_key=args.rapidapi_key)
        cleaner = DataCleaner()
        
        # Load and clean Play Store data
        playstore_file = args.playstore_file or os.path.join(Config.DATA_RAW_PATH, "googleplaystore.csv")
        playstore_df = ingestion.load_playstore_data(playstore_file)
        
        if playstore_df.empty:
            logger.warning("Using sample Play Store data for demonstration")
            print("⚠️  Using sample data - for full analysis, download the Google Play Store dataset")
        
        clean_playstore = cleaner.clean_playstore_data(playstore_df)
        cleaning_report = cleaner.get_cleaning_report()
        logger.info(f"Data cleaning completed: {cleaning_report}")
        
        # Fetch App Store data (if API key provided)
        appstore_df = ingestion.fetch_appstore_data()
        
        # Create unified dataset
        combined_df = ingestion.create_unified_schema(clean_playstore, appstore_df)
        data_file = ingestion.save_clean_data(combined_df)
        
        if data_file:
            print(f"✅ Clean data saved to: {data_file}")
        else:
            print("❌ Failed to save clean data")
            return
        
        insights = None
        d2c_insights = None
        
        # Phase 2: LLM Insights Generation
        if not args.skip_llm and (args.llm_api_key or Config.OPENAI_API_KEY or Config.GEMINI_API_KEY):
            print("\n🤖 Phase 2: Generating AI Insights")
            logger.info("Starting LLM insights generation")
            
            llm_generator = LLMInsightsGenerator(
                api_key=args.llm_api_key,
                provider=args.llm_provider
            )
            
            insights = llm_generator.generate_insights(combined_df, sample_size=args.sample_size)
            insights_file = llm_generator.save_insights(insights)
            
            if insights_file:
                print(f"✅ Insights saved to: {insights_file}")
                
                # Generate report
                report_generator = ReportGenerator()
                report_file = report_generator.generate_report(insights)
                print(f"✅ Report generated: {report_file}")
            else:
                print("❌ Failed to save insights")
        else:
            print("⚠️  Skipping LLM insights generation (no API key provided or --skip-llm flag used)")
            # Generate mock insights for demonstration
            llm_generator = LLMInsightsGenerator()
            insights = llm_generator.generate_insights(combined_df, sample_size=args.sample_size)
            insights_file = llm_generator.save_insights(insights)
            if insights_file:
                print(f"✅ Mock insights saved to: {insights_file}")
        
        # Phase 3: D2C Analysis (Bonus)
        if not args.skip_d2c:
            print("\n🛍️ Phase 3: D2C eCommerce Analysis")
            logger.info("Starting D2C analysis")
            
            d2c_analyzer = D2CAnalyzer()
            
            # Load D2C data
            d2c_file = args.d2c_file or _find_d2c_file()
            if d2c_file and os.path.exists(d2c_file):
                d2c_df = d2c_analyzer.load_d2c_data(d2c_file)
                d2c_insights = d2c_analyzer.analyze_funnel_metrics(d2c_df)
                d2c_file = d2c_analyzer.save_d2c_insights(d2c_insights)
                
                if d2c_file:
                    print(f"✅ D2C insights saved to: {d2c_file}")
                    
                    # Generate D2C report
                    report_generator = ReportGenerator()
                    d2c_report_file = report_generator.generate_d2c_report(d2c_insights)
                    print(f"✅ D2C report generated: {d2c_report_file}")
                else:
                    print("❌ Failed to save D2C insights")
            else:
                print("⚠️  D2C file not found. Using sample data for demonstration.")
                d2c_df = d2c_analyzer.load_d2c_data(None)  # This will create sample data
                d2c_insights = d2c_analyzer.analyze_funnel_metrics(d2c_df)
                d2c_analyzer.save_d2c_insights(d2c_insights)
                print("✅ D2C analysis completed with sample data")
        
        # Phase 4: Start Interface
        print("\n💬 Phase 4: Starting User Interface")
        logger.info("Starting user interface")
        
        if args.interface == 'cli':
            cli = CLIInterface()
            cli.run()
        else:
            print("📊 Starting Streamlit interface...")
            print("Run: streamlit run run_streamlit.py")
            # The Streamlit app will be started separately
        
        logger.info("System execution completed successfully")
        
    except Exception as e:
        logger.error(f"System execution failed: {str(e)}")
        print(f"❌ Error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()