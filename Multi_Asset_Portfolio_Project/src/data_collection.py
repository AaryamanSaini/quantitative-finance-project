import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

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

START_DATE = (datetime.now() - pd.DateOffset(years=5)).strftime('%Y-%m-%d')
END_DATE = datetime.now().strftime('%Y-%m-%d')


def collect_market_data(tickers=ASSET_TICKERS, start=START_DATE, end=END_DATE, simulate_alternatives=True, seed=42):
    """
    Download historical price data for given tickers, calculate monthly returns, annualized metrics, and correlation matrix.
    Optionally add simulated alternative asset data (hedge funds, private equity).
    Returns:
        prices (pd.DataFrame): Cleaned monthly price data
        returns (pd.DataFrame): Monthly returns
        ann_metrics (dict): Annualized return, volatility, Sharpe
        corr (pd.DataFrame): Correlation matrix
    """
    np.random.seed(seed)
    # Download daily adjusted close prices
    data = yf.download(tickers, start=start, end=end, progress=False)
    
    # Handle different yfinance output formats
    if isinstance(data.columns, pd.MultiIndex):
        # Multi-level columns (newer yfinance version)
        if 'Adj Close' in data.columns.get_level_values(0):
            data = data['Adj Close']
        else:
            # Fallback to Close if Adj Close not available
            data = data['Close']
    else:
        # Single-level columns (older yfinance version)
        if 'Adj Close' in data.columns:
            data = data['Adj Close']
        else:
            # Fallback to Close
            data = data['Close']
    
    # Forward fill and drop rows with all NaNs
    data = data.ffill().dropna(how='all')
    # Resample to month-end prices
    monthly_prices = data.resample('M').last()
    # Calculate monthly returns
    monthly_returns = monthly_prices.pct_change().dropna(how='all')
    # Handle missing data: drop columns with >10% missing, fill others
    missing = monthly_returns.isnull().mean()
    monthly_returns = monthly_returns.loc[:, missing <= 0.1].fillna(0)
    # Simulate alternative assets if needed
    if simulate_alternatives:
        alt_assets = simulate_alternative_assets(monthly_returns.index)
        monthly_returns = pd.concat([monthly_returns, alt_assets], axis=1)
        monthly_prices = pd.concat([monthly_prices, (1+alt_assets).cumprod()], axis=1)
    # Annualized metrics
    ann_metrics = calculate_annualized_metrics(monthly_returns)
    # Correlation matrix
    corr = monthly_returns.corr()
    return monthly_prices, monthly_returns, ann_metrics, corr

def simulate_alternative_assets(index):
    """
    Simulate monthly returns for two alternative assets: hedge funds and private equity.
    Returns DataFrame with realistic mean/volatility.
    """
    n = len(index)
    # Hedge Funds: 10% annual return, 15% vol
    hf_mean = 0.10 / 12
    hf_vol = 0.15 / np.sqrt(12)
    # Private Equity: 12% annual return, 18% vol
    pe_mean = 0.12 / 12
    pe_vol = 0.18 / np.sqrt(12)
    hf = np.random.normal(hf_mean, hf_vol, n)
    pe = np.random.normal(pe_mean, pe_vol, n)
    return pd.DataFrame({'Hedge_Fund': hf, 'Private_Equity': pe}, index=index)

def calculate_annualized_metrics(returns):
    """
    Calculate annualized return, volatility, and Sharpe ratio for each asset.
    """
    ann_return = (1 + returns).prod() ** (12 / len(returns)) - 1
    ann_vol = returns.std() * np.sqrt(12)
    sharpe = ann_return / ann_vol.replace(0, np.nan)
    return {'annualized_return': ann_return, 'annualized_volatility': ann_vol, 'sharpe_ratio': sharpe}

if __name__ == "__main__":
    # Example usage and test
    prices, rets, metrics, corr = collect_market_data()
    print("Monthly Returns Sample:\n", rets.head())
    print("Annualized Metrics:\n", metrics)
    print("Correlation Matrix:\n", corr) 