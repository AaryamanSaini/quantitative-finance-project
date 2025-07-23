#!/usr/bin/env python3
"""
Sample Data Testing Script
Validates all modules work together with realistic data
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from config import *
from data_collection import collect_market_data
from optimization import optimize_portfolio
from risk_analytics import calculate_var, stress_test_portfolio
from performance import evaluate_managers, performance_attribution
from visualization import plot_asset_allocation_pie, plot_correlation_heatmap
from excel_export import create_excel_dashboard


def test_complete_workflow():
    """Test the complete portfolio optimization workflow with sample data"""
    print("🧪 Testing Complete Portfolio Optimization Workflow")
    print("=" * 60)
    
    try:
        # Step 1: Data Collection Test
        print("\n1️⃣ Testing Data Collection...")
        prices, returns, metrics, corr = collect_market_data(
            tickers=['SPY', 'AGG', 'GLD'],  # Reduced set for testing
            start='2023-01-01',
            end='2023-12-31',
            simulate_alternatives=True
        )
        print(f"✅ Data collected: {len(returns.columns)} assets, {len(returns)} periods")
        print(f"   Sample returns: {returns.iloc[0].to_dict()}")
        
        # Step 2: Portfolio Optimization Test
        print("\n2️⃣ Testing Portfolio Optimization...")
        expected_returns = pd.Series(metrics['annualized_return'])
        annualized_cov = returns.cov() * 12
        
        optimal = optimize_portfolio(
            expected_returns=expected_returns,
            cov_matrix=annualized_cov,
            esg_scores=ESG_SCORES,
            min_alt=0.2,
            max_single=0.3,
            max_asset=0.4,
            min_esg=7.0
        )
        print(f"✅ Optimization completed:")
        print(f"   Sharpe Ratio: {optimal['sharpe_ratio']:.3f}")
        print(f"   Expected Return: {optimal['expected_return']:.3f}")
        print(f"   Volatility: {optimal['volatility']:.3f}")
        print(f"   ESG Score: {optimal['avg_esg']:.2f}")
        
        # Step 3: Risk Analytics Test
        print("\n3️⃣ Testing Risk Analytics...")
        portfolio_returns = returns.dot(pd.Series(optimal['weights']))
        
        var_results = calculate_var(portfolio_returns, [0.95, 0.99])
        print(f"✅ VaR calculated:")
        print(f"   95% VaR: {var_results['VaR_95']:.3f}")
        print(f"   99% VaR: {var_results['VaR_99']:.3f}")
        
        stress_results = stress_test_portfolio(returns)
        print(f"✅ Stress testing completed for {len(stress_results)} scenarios")
        
        # Step 4: Performance Attribution Test
        print("\n4️⃣ Testing Performance Attribution...")
        attribution = performance_attribution(
            portfolio_returns=portfolio_returns,
            asset_returns=returns,
            weights=optimal['weights']
        )
        print(f"✅ Attribution calculated for {len(attribution['by_asset'])} assets")
        
        # Step 5: Visualization Test
        print("\n5️⃣ Testing Visualizations...")
        os.makedirs('outputs/charts', exist_ok=True)
        
        # Test pie chart
        plot_asset_allocation_pie(
            weights=optimal['weights'],
            save_path='outputs/charts/test_allocation.png'
        )
        print("✅ Asset allocation pie chart created")
        
        # Test correlation heatmap
        plot_correlation_heatmap(
            corr_matrix=corr,
            save_path='outputs/charts/test_correlation.png'
        )
        print("✅ Correlation heatmap created")
        
        # Step 6: Excel Export Test
        print("\n6️⃣ Testing Excel Export...")
        dashboard_data = {
            'Test_Summary': {
                'Sharpe_Ratio': optimal['sharpe_ratio'],
                'Expected_Return': optimal['expected_return'],
                'Volatility': optimal['volatility'],
                'ESG_Score': optimal['avg_esg']
            },
            'Test_Allocation': pd.DataFrame(
                list(optimal['weights'].items()),
                columns=['Asset', 'Weight']
            ),
            'Test_Risk_Metrics': pd.DataFrame([var_results])
        }
        
        create_excel_dashboard(
            sheets_dict=dashboard_data,
            file_path='outputs/test_dashboard.xlsx'
        )
        print("✅ Excel dashboard created")
        
        # Step 7: Validation Checks
        print("\n7️⃣ Running Validation Checks...")
        
        # Check Sharpe ratio is reasonable
        assert optimal['sharpe_ratio'] > 0, "Sharpe ratio should be positive"
        print("✅ Sharpe ratio validation passed")
        
        # Check weights sum to 1
        weights_sum = sum(optimal['weights'].values())
        assert abs(weights_sum - 1.0) < 0.001, "Weights should sum to 1"
        print("✅ Portfolio weights validation passed")
        
        # Check ESG score meets minimum
        assert optimal['avg_esg'] >= 7.0, "ESG score should meet minimum requirement"
        print("✅ ESG score validation passed")
        
        # Check VaR is reasonable
        assert var_results['VaR_95'] > 0, "VaR should be positive"
        print("✅ VaR validation passed")
        
        print("\n🎉 ALL TESTS PASSED! Sample data workflow completed successfully.")
        print("\n📊 Sample Results Summary:")
        print(f"   Portfolio Sharpe Ratio: {optimal['sharpe_ratio']:.3f}")
        print(f"   Expected Annual Return: {optimal['expected_return']:.1%}")
        print(f"   Annual Volatility: {optimal['volatility']:.1%}")
        print(f"   Maximum Drawdown (95% VaR): {var_results['VaR_95']:.1%}")
        print(f"   ESG Score: {optimal['avg_esg']:.1f}/10")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_complete_workflow()
    sys.exit(0 if success else 1) 