# 🤖 AI-Powered Market Intelligence System

A comprehensive market intelligence platform that ingests data from multiple sources, generates AI-powered insights, and provides actionable recommendations for decision-making in the mobile app ecosystem and D2C eCommerce space.

## 🚀 Features

### Core Capabilities
- **Multi-Source Data Integration**: Google Play Store + Apple App Store
- **AI-Powered Insights**: LLM-generated market intelligence using OpenAI/Gemini
- **D2C eCommerce Analysis**: Funnel metrics, SEO opportunities, creative generation
- **Confidence Scoring**: Statistical validation of insights
- **Multiple Interfaces**: CLI and Streamlit web dashboard
- **Automated Reporting**: Markdown reports with actionable recommendations
- **Real-time Data**: App Store API integration via RapidAPI

### Data Sources
1. **Google Play Store Apps** (Kaggle dataset or synthetic data)
2. **Apple App Store** (RapidAPI integration)
3. **D2C eCommerce Data** (Synthetic performance data)

## 📋 Prerequisites

- Python 3.8+
- API keys for:
  - [RapidAPI](https://rapidapi.com/) (App Store data)
  - [OpenAI](https://platform.openai.com/) or [Google Gemini](https://ai.google.dev/) (LLM insights)

## 🛠️ Installation

### 1. Clone and Setup
```bash
git clone <repository-url>
cd market_intelligence
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
# API Keys
RAPIDAPI_KEY=your_rapidapi_key_here
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Configuration
DEFAULT_LLM_PROVIDER=openai
SAMPLE_SIZE=1000
MAX_APPS_FETCH=50
```

### 5. Directory Structure Setup
```bash
# Create necessary directories
mkdir -p data/raw data/processed data/outputs
```

## 🎯 Quick Start

### Option 1: Full Analysis with Real APIs
```bash
python main.py
```

### Option 2: Mock Data Mode (No APIs Required)
```bash
python main.py --skip-llm
```

### Option 3: D2C Analysis Only
```bash
python main.py --d2c-file path/to/d2c_data.xlsx --skip-llm
```

### Option 4: Streamlit Dashboard
```bash
streamlit run run_streamlit.py
```

## 📊 Data Preparation

### Google Play Store Data
1. Download from [Kaggle](https://www.kaggle.com/datasets/lava18/google-play-store-apps)
2. Place file at: `data/raw/googleplaystore.csv`

### D2C eCommerce Data (Optional)
- Place Excel file at: `data/raw/d2c_data.xlsx`
- Required columns: campaign_id, category, ad_spend, impressions, clicks, conversions, revenue, installs, signups, first_purchase, repeat_purchase, search_volume, average_position, conversion_rate

## 🏗️ Project Structure

```
market_intelligence/
├── data/
│   ├── raw/              # Raw input data
│   ├── processed/        # Cleaned datasets
│   └── outputs/          # Generated insights & reports
├── pipelines/
│   ├── data_ingestion.py # Data loading & API integration
│   ├── data_cleaning.py  # Data preprocessing & normalization
│   ├── llm_insights.py   # AI insights generation
│   └── d2c_analyzer.py   # D2C eCommerce analysis
├── interfaces/
│   ├── cli_interface.py  # Command-line interface
│   └── streamlit_app.py  # Web dashboard
├── reports/
│   └── report_generator.py # Automated reporting
├── utils/
│   ├── config.py         # Configuration management
│   └── helpers.py        # Utility functions
├── tests/                # Unit tests
├── main.py              # Main entry point
└── requirements.txt     # Dependencies
```

## 🔧 Configuration

### Command Line Arguments
- `--llm-api-key`: LLM provider API key
- `--rapidapi-key`: RapidAPI key for App Store data
- `--d2c-file`: Path to D2C Excel file
- `--playstore-file`: Path to Play Store CSV file
- `--sample-size`: Records to analyze (default: 1000)
- `--interface`: cli or streamlit (default: cli)
- `--skip-llm`: Skip LLM insights generation
- `--skip-d2c`: Skip D2C analysis

### Environment Variables
- `RAPIDAPI_KEY`: App Store data access
- `OPENAI_API_KEY` / `GEMINI_API_KEY`: LLM provider keys
- `DEFAULT_LLM_PROVIDER`: openai or gemini

## 📈 Outputs

### Generated Files
1. **Cleaned Dataset**: `data/processed/combined_apps_data.csv`
2. **Market Insights**: `data/outputs/market_insights.json`
3. **D2C Insights**: `data/outputs/d2c_insights.json`
4. **Reports**: Timestamped Markdown reports

### Insights Structure
```json
{
  "summary": {
    "total_apps_analyzed": 1000,
    "analysis_scope": "Comprehensive market intelligence",
    "key_findings_count": 15
  },
  "insights": {
    "market_trends": {
      "emerging_categories": ["Health & Fitness", "Education Technology"],
      "saturation_analysis": "Market analysis...",
      "growth_opportunities": ["AI features", "Subscription models"]
    },
    "competitive_analysis": {...},
    "strategic_recommendations": {...},
    "consumer_insights": {...}
  },
  "statistical_backing": {...},
  "confidence_metrics": {
    "overall_confidence": 0.85,
    "data_quality_score": 0.78,
    "statistical_significance": 0.82
  }
}
```

## 🎨 Features in Detail

### Market Intelligence
- **Emerging Categories**: Identify high-growth app categories
- **Competitive Analysis**: Pricing strategies and quality indicators
- **Consumer Insights**: User preference patterns and adoption factors
- **Confidence Scoring**: Statistical validation of all insights

### D2C eCommerce Analysis
- **Funnel Metrics**: CAC, ROAS, conversion rates, retention
- **SEO Opportunities**: High-potential categories and traffic estimates
- **Creative Generation**: AI-powered ad copy and product descriptions
- **Budget Optimization**: Data-driven spend recommendations

### Interactive Interfaces
- **CLI**: Menu-driven exploration of insights
- **Streamlit**: Visual dashboard with charts and metrics

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

Run specific test files:
```bash
python -m unittest tests/test_data_pipeline.py
python -m unittest tests/test_insights.py
```

## 🚀 Usage Examples

### Complete Market Analysis
```bash
python main.py --llm-api-key sk-... --rapidapi-key your-key
```

### Quick Demo with Sample Data
```bash
python main.py --skip-llm --sample-size 500
```

### Generate D2C Report Only
```bash
python main.py --d2c-file data/raw/d2c_data.xlsx --skip-llm --interface cli
```

### Web Dashboard
```bash
streamlit run run_streamlit.py
```

## 🔍 Troubleshooting

### Common Issues

**API Connection Problems**
```bash
# Test RapidAPI connection
python -c "
import requests
headers = {
    'X-RapidAPI-Key': 'your-key',
    'X-RapidAPI-Host': 'appstore-scrapper-api.p.rapidapi.com'
}
response = requests.get('https://appstore-scrapper-api.p.rapidapi.com/app/details', 
                       headers=headers, 
                       params={'id': '284882215', 'country': 'us'})
print(f'Status: {response.status_code}')
"
```

**Missing Data Files**
- System automatically generates realistic sample data
- Download actual datasets for production analysis

**Memory Issues**
- Use `--sample-size` parameter to limit analysis
- System processes data in chunks for large datasets

### Logs
- Check `market_intelligence.log` for detailed execution logs
- All operations are logged with timestamps and error details

## 📚 API Reference

### Key Classes

#### DataIngestion
- `load_playstore_data()`: Load and validate Play Store data
- `fetch_appstore_data()`: Real-time App Store data via API
- `create_unified_schema()`: Combine datasets into consistent format

#### LLMInsightsGenerator
- `generate_insights()`: AI-powered market intelligence
- `_calculate_statistical_insights()`: Confidence scoring and validation

#### D2CAnalyzer
- `analyze_funnel_metrics()`: CAC, ROAS, conversion analysis
- `_analyze_seo_opportunities()`: Growth potential identification

#### CLIInterface
- Interactive command-line exploration
- Export capabilities for all insights

#### StreamlitApp
- Visual dashboard with metrics and charts
- Real-time insight exploration

## 🔄 Extending the System

### Adding New Data Sources
1. Extend `DataIngestion` class
2. Implement data loading and schema mapping
3. Update unified schema creation

### Custom LLM Prompts
Modify templates in:
- `pipelines/llm_insights.py` (market intelligence)
- `pipelines/d2c_analyzer.py` (creative generation)

### New Report Formats
Extend `ReportGenerator` class in `reports/report_generator.py`

## 📄 License

This project is developed as part of an AI engineering assignment demonstration.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request

## 🆘 Support

- Check generated log files for error details
- Verify API keys and network connectivity
- Use sample data mode for quick testing
- Run tests to validate installation

---

**Ready to generate powerful market insights!** 🚀

Run `python main.py` to start your analysis or `streamlit run run_streamlit.py` for the visual dashboard.
