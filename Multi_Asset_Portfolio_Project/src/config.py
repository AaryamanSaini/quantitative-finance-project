# Configuration parameters for Multi-Asset Portfolio Optimization Project

# Asset Configuration
ASSET_TICKERS = [
    'SPY',  # US Equity
    'EFA',  # International Equity
    'AGG',  # Bonds
    'TIP',  # TIPS
    'VNQ',  # REITs
    'DJP',  # Commodities
    'GLD',  # Gold
    'HYG'   # High Yield
]

# Data Configuration
START_DATE = '2019-01-01'
END_DATE = '2024-12-31'
DATA_FREQUENCY = 'M'  # Monthly

# Portfolio Constraints
MAX_ASSET_WEIGHT = 0.40  # 40% max per asset
MIN_ALTERNATIVES = 0.20  # 20% min to alternatives
MAX_SINGLE_ASSET = 0.30  # 30% max concentration
MIN_ESG_SCORE = 7.0      # Minimum average ESG score

# Risk Management
RISK_FREE_RATE = 0.02    # 2% annual risk-free rate
TRANSACTION_COSTS = 0.001 # 10 bps per trade
VAR_CONFIDENCE_LEVELS = [0.95, 0.99]

# ESG Scores (1-10 scale)
ESG_SCORES = {
    'SPY': 8.5,
    'EFA': 7.8,
    'AGG': 8.2,
    'TIP': 8.0,
    'VNQ': 6.5,
    'DJP': 5.5,
    'GLD': 7.0,
    'HYG': 6.8,
    'Hedge_Fund': 8.2,
    'Private_Equity': 8.0
}

# Stress Test Scenarios
STRESS_SCENARIOS = {
    '2008_Crisis': ('2007-10-01', '2009-03-01'),
    'COVID_Crash': ('2020-02-01', '2020-04-01'),
    'Rate_Shock': None,  # Custom scenario
    'Custom_Worst': None
}

# Performance Tracking
ROLLING_WINDOW = 12  # Months
REBALANCING_FREQUENCY = 'Q'  # Quarterly

# Output Configuration
OUTPUT_DIR = '../outputs/'
CHARTS_DIR = '../outputs/charts/'
EXCEL_FILENAME = 'Portfolio_Dashboard.xlsx' 