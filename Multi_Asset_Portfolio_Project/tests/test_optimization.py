import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from optimization import optimize_portfolio, ESG_SCORES


class TestOptimization(unittest.TestCase):
    """Test cases for portfolio optimization module"""
    
    def setUp(self):
        """Set up test data"""
        np.random.seed(42)
        self.test_assets = ['SPY', 'AGG', 'GLD', 'Hedge_Fund']
        self.expected_returns = pd.Series(
            [0.10, 0.05, 0.08, 0.12],
            index=self.test_assets
        )
        self.cov_matrix = pd.DataFrame(
            np.random.uniform(0.01, 0.05, (4, 4)),
            index=self.test_assets,
            columns=self.test_assets
        )
        # Make covariance matrix symmetric and positive definite
        self.cov_matrix = (self.cov_matrix + self.cov_matrix.T) / 2
        self.cov_matrix += np.eye(4) * 0.01
        
    def test_optimize_portfolio_basic(self):
        """Test basic portfolio optimization"""
        result = optimize_portfolio(
            expected_returns=self.expected_returns,
            cov_matrix=self.cov_matrix
        )
        
        # Check result structure
        required_keys = ['weights', 'sharpe_ratio', 'expected_return', 'volatility', 'avg_esg']
        for key in required_keys:
            self.assertIn(key, result)
            
        # Check weights sum to 1
        weights_sum = sum(result['weights'].values())
        self.assertAlmostEqual(weights_sum, 1.0, places=6)
        
        # Check all weights are positive
        for weight in result['weights'].values():
            self.assertGreaterEqual(weight, 0)
            
    def test_optimization_constraints(self):
        """Test optimization with constraints"""
        result = optimize_portfolio(
            expected_returns=self.expected_returns,
            cov_matrix=self.cov_matrix,
            max_asset=0.4,
            min_alt=0.2,
            max_single=0.3
        )
        
        # Check max asset constraint
        for weight in result['weights'].values():
            self.assertLessEqual(weight, 0.4)
            
        # Check alternatives minimum (Hedge_Fund should be >= 0.2)
        alt_weight = result['weights'].get('Hedge_Fund', 0)
        self.assertGreaterEqual(alt_weight, 0.2)
        
        # Check max single asset constraint
        max_weight = max(result['weights'].values())
        self.assertLessEqual(max_weight, 0.3)
        
    def test_esg_constraint(self):
        """Test ESG scoring constraint"""
        result = optimize_portfolio(
            expected_returns=self.expected_returns,
            cov_matrix=self.cov_matrix,
            min_esg=7.0
        )
        
        # Check ESG score is above minimum
        self.assertGreaterEqual(result['avg_esg'], 7.0)
        
    def test_transaction_costs(self):
        """Test transaction cost modeling"""
        # First optimization
        result1 = optimize_portfolio(
            expected_returns=self.expected_returns,
            cov_matrix=self.cov_matrix
        )
        
        # Second optimization with previous weights
        prev_weights = np.array(list(result1['weights'].values()))
        result2 = optimize_portfolio(
            expected_returns=self.expected_returns,
            cov_matrix=self.cov_matrix,
            prev_weights=prev_weights,
            transaction_costs=0.001
        )
        
        # Should have similar but not identical results
        self.assertNotEqual(result1['weights'], result2['weights'])
        
    def test_optimization_failure_handling(self):
        """Test handling of optimization failures"""
        # Create invalid covariance matrix
        invalid_cov = pd.DataFrame(
            [[1, 1], [1, 1]],  # Not positive definite
            index=['A', 'B'],
            columns=['A', 'B']
        )
        invalid_returns = pd.Series([0.1, 0.1], index=['A', 'B'])
        
        with self.assertRaises(ValueError):
            optimize_portfolio(
                expected_returns=invalid_returns,
                cov_matrix=invalid_cov
            )


if __name__ == '__main__':
    unittest.main() 