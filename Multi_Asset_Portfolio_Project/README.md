# Multi-Asset Portfolio Optimization Project

## 🎯 Project Overview

A comprehensive multi-asset portfolio optimization system designed for institutional-level portfolio management. This project demonstrates advanced quantitative analysis capabilities suitable for Morgan Stanley Portfolio Solutions Group internship applications.

## 🚀 Key Features

### Core Functionality
- **Data Collection**: Automated download of 5 years of historical data for 8 asset classes
- **Portfolio Optimization**: Mean-variance optimization with institutional constraints
- **Risk Management**: VaR calculations, stress testing, and factor analysis
- **Performance Attribution**: Manager evaluation and return decomposition
- **Dynamic Rebalancing**: Optimal rebalancing with transaction costs
- **Visualization**: Professional charts and graphs
- **Excel Dashboard**: Comprehensive reporting system

### Asset Classes
- **Traditional**: SPY (US Equity), EFA (International Equity), AGG (Bonds), TIP (TIPS)
- **Alternative**: VNQ (REITs), DJP (Commodities), GLD (Gold), HYG (High Yield)
- **Simulated**: Hedge Funds, Private Equity

## 📊 Target Metrics

- **Portfolio Sharpe Ratio**: >1.2 (vs benchmark ~0.8)
- **Maximum Drawdown**: <15% (vs benchmark ~20%)
- **95% VaR**: <3% monthly loss
- **Diversification Benefit**: >200bps annual return improvement
- **Transaction Cost Optimization**: <10bps annual drag

## 🛠️ Installation

### Prerequisites
```bash
Python 3.8+
pip install -r requirements.txt
```

### Setup
```bash
# Clone the repository
git clone https://github.com/AaryamanSaini/quantitative-finance-project.git
cd quantitative-finance-project/Multi_Asset_Portfolio_Project

# Install dependencies
pip install -r requirements.txt

# Create output directories
mkdir -p outputs/charts
```

## 🚀 Quick Start

### Run Complete Analysis
```bash
cd src
python main.py
```

### Individual Module Usage
```python
from data_collection import collect_market_data
from optimization import optimize_portfolio
from risk_analytics import calculate_var, stress_test_portfolio

# Collect data
prices, returns, metrics, corr = collect_market_data()

# Optimize portfolio
optimal = optimize_portfolio(expected_returns, cov_matrix)

# Risk analysis
var_results = calculate_var(portfolio_returns)
stress_results = stress_test_portfolio(returns)
```

## 📁 Project Structure

```
Multi_Asset_Portfolio_Project/
├── src/
│   ├── main.py              # Main execution script
│   ├── config.py            # Configuration parameters
│   ├── data_collection.py   # Data gathering and preprocessing
│   ├── optimization.py      # Portfolio optimization algorithms
│   ├── risk_analytics.py    # Risk calculations and stress testing
│   ├── performance.py       # Performance attribution and analytics
│   ├── visualization.py     # Charts and graphs
│   └── excel_export.py      # Excel dashboard creation
├── data/                    # Raw and processed data
├── outputs/                 # Generated outputs
│   ├── charts/             # Visualization images
│   └── Portfolio_Dashboard.xlsx
├── docs/                   # Documentation
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 📈 Key Functions

### Data Collection
- `collect_market_data()`: Download and clean asset data
- `calculate_annualized_metrics()`: Compute returns, volatility, Sharpe ratios
- `simulate_alternative_assets()`: Generate realistic alternative asset data

### Portfolio Optimization
- `optimize_portfolio()`: Mean-variance optimization with constraints
- Institutional constraints: Asset limits, alternatives minimum, ESG scoring
- Transaction cost modeling for rebalancing decisions

### Risk Analytics
- `calculate_var()`: Value at Risk calculations (95%, 99%)
- `stress_test_portfolio()`: Scenario analysis (2008, COVID-19, rate shocks)
- `factor_analysis()`: Risk factor exposures
- `dynamic_correlation()`: Rolling correlation tracking

### Performance & Attribution
- `evaluate_managers()`: Third-party manager scoring and ranking
- `performance_attribution()`: Return decomposition by asset
- `dynamic_rebalancing()`: Optimal rebalancing with costs

### Visualization
- Efficient frontier plots
- Asset allocation pie charts
- Correlation heatmaps
- Rolling performance charts
- Risk contribution bar charts
- Stress test results (radar/bar)
- Manager comparison scatter plots
- Performance attribution waterfall charts

## 📊 Output Files

### Excel Dashboard
- **Executive Summary**: Key metrics and portfolio overview
- **Asset Allocation**: Current weights and target allocations
- **Risk Metrics**: VaR, stress test results, factor exposures
- **Performance Attribution**: Return decomposition by asset
- **Manager Analysis**: Third-party fund evaluation
- **Historical Performance**: Monthly returns and attribution

### Charts
- High-quality PNG images for all visualizations
- Professional formatting suitable for presentations
- Embedded in Excel dashboard

## 🔧 Configuration

Key parameters in `config.py`:
- Asset tickers and data ranges
- Portfolio constraints (weights, ESG, alternatives)
- Risk management settings (VaR levels, stress scenarios)
- Transaction costs and rebalancing frequency
- Output file paths and formats

## 🧪 Testing

### Unit Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific module tests
python -m pytest tests/test_optimization.py
```

### Sample Data Testing
The system includes comprehensive sample data testing to validate all calculations and ensure reproducibility.

## 📚 Documentation

- **README.md**: Project overview and setup (this file)
- **Methodology.pdf**: Detailed explanation of optimization approach
- **Executive_Summary.pdf**: Key findings and recommendations
- Inline code comments explaining complex calculations
- Function docstrings with parameter descriptions

## 🎯 Success Criteria

This project demonstrates:
- ✅ Institutional-level portfolio management skills
- ✅ Advanced quantitative analysis capabilities
- ✅ Professional presentation quality
- ✅ Real-world applicability to Morgan Stanley PSG role
- ✅ Complete end-to-end portfolio construction process

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with comprehensive testing
4. Submit a pull request with detailed description

## 📄 License

This project is for educational and demonstration purposes.

## 👨‍💻 Author

**Aaryaman Saini**
- GitHub: [@AaryamanSaini](https://github.com/AaryamanSaini)
- Project: Multi-Asset Portfolio Optimization for Morgan Stanley PSG Application

---

*This project represents production-quality code suitable for institutional investment management applications.* 