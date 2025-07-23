# 🎯 Multi-Asset Portfolio Optimization System

**Aaryaman Saini** | Quantitative Finance Portfolio Management Project

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.0+-purple.svg)](https://tailwindcss.com/)
[![Chart.js](https://img.shields.io/badge/Chart.js-3.0+-orange.svg)](https://www.chartjs.org/)

## 📊 Project Overview

This institutional-grade portfolio optimization system demonstrates advanced quantitative finance techniques including mean-variance optimization, ESG integration, risk analytics, and dynamic rebalancing. Built for professional portfolio management applications and quantitative investment research.

### 🎯 Key Features

- **Mean-Variance Optimization**: Markowitz framework implementation with constraints
- **ESG Integration**: Environmental, Social, and Governance scoring system
- **Risk Analytics**: VaR, stress testing, drawdown analysis, and factor modeling
- **Multi-Asset Class Support**: Stocks, bonds, alternatives, commodities, real estate
- **Dynamic Rebalancing**: Automated portfolio rebalancing with transaction costs
- **Professional Dashboard**: Interactive web interface with real-time analytics
- **Excel Export**: Comprehensive reporting for institutional clients
- **Educational Interface**: Detailed explanations and tooltips for learning

## 🏗️ Architecture

```
quantitative-finance-project/
├── backend_server.py          # Flask API server
├── data_collection.py         # Market data collection & preprocessing
├── optimization.py            # Portfolio optimization algorithms
├── excel_export.py           # Excel report generation
├── frontend/
│   ├── index.html            # Main dashboard interface
│   └── app.js               # Frontend JavaScript logic
└── README.md                # Project documentation
```

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.8+ required
python3 --version

# Install required packages
pip install yfinance pandas numpy scipy matplotlib seaborn plotly openpyxl xlsxwriter flask flask-cors
```

### Running the Application

1. **Start the Backend Server:**
   ```bash
   cd quantitative-finance-project
   python3 backend_server.py
   ```
   The Flask server will start on `http://localhost:5000`

2. **Start the Frontend:**
   ```bash
   # In a new terminal, from the project root
   python3 -m http.server 8080
   ```

3. **Access the Dashboard:**
   Open your browser and navigate to: `http://localhost:8080/frontend/index.html`

## 📈 Core Functionality

### Portfolio Optimization
- **Mean-Variance Framework**: Maximizes Sharpe ratio while respecting constraints
- **Asset Allocation**: Optimal weight distribution across multiple asset classes
- **Risk Management**: Comprehensive risk metrics and stress testing
- **ESG Integration**: Sustainable investing with minimum ESG score requirements

### Risk Analytics
- **Value at Risk (VaR)**: 95% and 99% confidence intervals
- **Maximum Drawdown**: Historical worst-case scenario analysis
- **Volatility Analysis**: Rolling volatility and correlation matrices
- **Stress Testing**: Scenario analysis for extreme market conditions

### Professional Features
- **Real-time Optimization**: Live portfolio rebalancing with user parameters
- **Interactive Charts**: Dynamic visualizations using Chart.js
- **Excel Reporting**: Institutional-grade reports with multiple sheets
- **Educational Interface**: Detailed explanations and learning resources

## 🎨 User Interface

### Dashboard Features
- **Black Theme**: Professional dark interface suitable for institutional use
- **Interactive Parameters**: Real-time adjustment of optimization constraints
- **Live Charts**: Asset allocation pie chart and risk metrics bar chart
- **Status Logging**: Real-time feedback on optimization processes
- **Educational Tooltips**: Hover explanations for all metrics and parameters

### Key Metrics Displayed
- **Sharpe Ratio**: Risk-adjusted return performance
- **Expected Return**: Annualized portfolio return projections
- **Volatility**: Portfolio risk measurement
- **ESG Score**: Sustainability rating (0-10 scale)

## 🔧 Technical Implementation

### Backend (Python/Flask)
```python
# Core optimization endpoint
POST /run_optimization
{
    "riskFreeRate": 0.02,
    "minAlternatives": 0.20,
    "maxSingle": 0.30,
    "minEsg": 7.0
}

# Excel export endpoint
POST /export_excel
# Returns comprehensive Excel report
```

### Frontend (HTML/JavaScript/Tailwind CSS)
- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Updates**: Live chart and metric updates
- **Error Handling**: Graceful fallback to simulation mode
- **Professional Styling**: Institutional-grade appearance

## 📊 Sample Results

### Optimized Portfolio Allocation
- **SPY (S&P 500)**: 25% - Core equity exposure
- **AGG (Bonds)**: 20% - Fixed income diversification
- **GLD (Gold)**: 15% - Commodity hedge
- **Hedge Fund**: 25% - Alternative strategies
- **Private Equity**: 15% - Illiquid alternatives

### Performance Metrics
- **Sharpe Ratio**: 2.33 (Excellent risk-adjusted returns)
- **Expected Return**: 18.1% (Annualized)
- **Volatility**: 6.9% (Low risk profile)
- **ESG Score**: 7.9/10 (Strong sustainability)

## 🎓 Educational Value

This project demonstrates:
- **Quantitative Finance**: Advanced portfolio theory implementation
- **Risk Management**: Institutional-grade risk analytics
- **ESG Investing**: Sustainable finance integration
- **Professional Development**: Full-stack financial application
- **Data Science**: Real-world financial data analysis

## 🏢 Institutional Applications

- **Portfolio Management**: Institutional asset allocation
- **Risk Management**: Comprehensive risk analytics and reporting
- **Client Services**: Professional client portfolio optimization
- **Research**: Quantitative investment research platform
- **Education**: Learning tool for finance professionals

## 🔮 Future Enhancements

- **Machine Learning**: ML-based portfolio optimization
- **Alternative Data**: ESG, sentiment, and alternative data integration
- **Real-time Data**: Live market data feeds
- **Mobile App**: Native mobile application
- **API Integration**: Third-party data and execution platforms

## 📝 License

This project is developed for educational and professional portfolio management purposes.

## 👨‍💻 Author

**Aaryaman Saini**
- Quantitative Finance Portfolio Optimization Project
- Institutional-grade portfolio management system
- Professional quantitative finance implementation

---

*This project showcases advanced quantitative finance techniques and institutional portfolio management capabilities suitable for professional applications in investment management and quantitative finance.*