import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_collection import collect_market_data, calculate_annualized_metrics, simulate_alternative_assets


class TestDataCollection(unittest.TestCase):
    """Test cases for data collection module"""
    
    def setUp(self):
        """Set up test data"""
        self.test_tickers = ['SPY', 'AGG']
        self.test_start = '2023-01-01'
        self.test_end = '2023-12-31'
        
    def test_collect_market_data_basic(self):
        """Test basic market data collection"""
        prices, returns, metrics, corr = collect_market_data(
            tickers=self.test_tickers,
            start=self.test_start,
            end=self.test_end,
            simulate_alternatives=False
        )
        
        # Check data types
        self.assertIsInstance(prices, pd.DataFrame)
        self.assertIsInstance(returns, pd.DataFrame)
        self.assertIsInstance(metrics, dict)
        self.assertIsInstance(corr, pd.DataFrame)
        
        # Check dimensions
        self.assertEqual(len(returns.columns), len(self.test_tickers))
        self.assertTrue(len(returns) > 0)
        
    def test_calculate_annualized_metrics(self):
        """Test annualized metrics calculation"""
        # Create sample returns
        np.random.seed(42)
        sample_returns = pd.DataFrame(
            np.random.normal(0.01, 0.04, (24, 2)),
            columns=['Asset1', 'Asset2']
        )
        
        metrics = calculate_annualized_metrics(sample_returns)
        
        # Check required keys
        required_keys = ['annualized_return', 'annualized_volatility', 'sharpe_ratio']
        for key in required_keys:
            self.assertIn(key, metrics)
            
        # Check metrics are Series
        self.assertIsInstance(metrics['annualized_return'], pd.Series)
        self.assertIsInstance(metrics['annualized_volatility'], pd.Series)
        
    def test_simulate_alternative_assets(self):
        """Test alternative asset simulation"""
        index = pd.date_range('2023-01-31', periods=12, freq='M')
        alt_assets = simulate_alternative_assets(index)
        
        # Check output
        self.assertIsInstance(alt_assets, pd.DataFrame)
        self.assertEqual(len(alt_assets), 12)
        self.assertIn('Hedge_Fund', alt_assets.columns)
        self.assertIn('Private_Equity', alt_assets.columns)
        
        # Check realistic values
        self.assertTrue(alt_assets['Hedge_Fund'].mean() > 0)
        self.assertTrue(alt_assets['Private_Equity'].mean() > 0)
        
    def test_data_quality_checks(self):
        """Test data quality and missing data handling"""
        prices, returns, metrics, corr = collect_market_data(
            tickers=self.test_tickers,
            start=self.test_start,
            end=self.test_end,
            simulate_alternatives=False
        )
        
        # Check no excessive missing data
        missing_pct = returns.isnull().sum() / len(returns)
        self.assertTrue(all(missing_pct <= 0.1))  # Max 10% missing
        
        # Check correlation matrix is valid
        self.assertTrue(corr.notna().all().all())
        self.assertTrue((corr >= -1).all().all() and (corr <= 1).all().all())


if __name__ == '__main__':
    unittest.main() 