#!/usr/bin/env python3
"""
Main execution script for Multi-Asset Portfolio Optimization Project
Integrates all modules and runs complete portfolio optimization workflow
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import *
from data_collection import collect_market_data, calculate_annualized_metrics
from optimization import optimize_portfolio
from risk_analytics import calculate_var, stress_test_portfolio, factor_analysis, dynamic_correlation
from performance import evaluate_managers, performance_attribution, dynamic_rebalancing
from visualization import (
    plot_efficient_frontier, plot_asset_allocation_pie, plot_correlation_heatmap,
    plot_rolling_performance, plot_risk_contribution_bar, plot_stress_test_results,
    plot_manager_comparison_scatter, plot_performance_attribution_waterfall
)
from excel_export import create_excel_dashboard, format_excel_sheet, embed_chart_in_excel


def main():
    """Main execution function for portfolio optimization workflow"""
    print("🚀 Starting Multi-Asset Portfolio Optimization Project...")
    
    try:
        # Step 1: Data Collection
        print("📊 Collecting market data...")
        prices, returns, metrics, corr_matrix = collect_market_data(
            tickers=ASSET_TICKERS,
            start=START_DATE,
            end=END_DATE,
            simulate_alternatives=True
        )
        print(f"✅ Collected data for {len(returns.columns)} assets over {len(returns)} periods")
        
        # Step 2: Portfolio Optimization
        print("⚡ Running portfolio optimization...")
        expected_returns = pd.Series(metrics['annualized_return'])
        annualized_cov = returns.cov() * 12
        
        optimal_portfolio = optimize_portfolio(
            expected_returns=expected_returns,
            cov_matrix=annualized_cov,
            esg_scores=ESG_SCORES,
            min_alt=MIN_ALTERNATIVES,
            max_single=MAX_SINGLE_ASSET,
            max_asset=MAX_ASSET_WEIGHT,
            min_esg=MIN_ESG_SCORE,
            risk_free_rate=RISK_FREE_RATE,
            transaction_costs=TRANSACTION_COSTS
        )
        print(f"✅ Optimal portfolio Sharpe ratio: {optimal_portfolio['sharpe_ratio']:.3f}")
        
        # Step 3: Risk Analytics
        print("🛡️ Running risk analytics...")
        portfolio_returns = returns.dot(pd.Series(optimal_portfolio['weights']))
        
        # VaR calculation
        var_results = calculate_var(portfolio_returns, VAR_CONFIDENCE_LEVELS)
        print(f"✅ 95% VaR: {var_results['VaR_95']:.3f}")
        
        # Stress testing
        stress_results = stress_test_portfolio(returns, STRESS_SCENARIOS)
        print(f"✅ Stress testing completed for {len(stress_results)} scenarios")
        
        # Step 4: Performance Attribution
        print("📈 Running performance attribution...")
        attribution = performance_attribution(
            portfolio_returns=portfolio_returns,
            asset_returns=returns,
            weights=optimal_portfolio['weights']
        )
        
        # Step 5: Generate Visualizations
        print("📊 Generating visualizations...")
        os.makedirs(CHARTS_DIR, exist_ok=True)
        
        # Efficient frontier (simplified)
        vol_range = np.linspace(0.05, 0.25, 50)
        ret_range = [optimal_portfolio['expected_return']] * 50
        plot_efficient_frontier(
            weights_list=[optimal_portfolio['weights']],
            returns_list=ret_range,
            vol_list=vol_range,
            optimal_point=(optimal_portfolio['volatility'], optimal_portfolio['expected_return']),
            save_path=f"{CHARTS_DIR}efficient_frontier.png"
        )
        
        # Asset allocation pie chart
        plot_asset_allocation_pie(
            weights=optimal_portfolio['weights'],
            save_path=f"{CHARTS_DIR}asset_allocation.png"
        )
        
        # Correlation heatmap
        plot_correlation_heatmap(
            corr_matrix=corr_matrix,
            save_path=f"{CHARTS_DIR}correlation_heatmap.png"
        )
        
        # Risk contribution
        plot_risk_contribution_bar(
            weights=optimal_portfolio['weights'],
            cov_matrix=annualized_cov,
            save_path=f"{CHARTS_DIR}risk_contribution.png"
        )
        
        # Stress test results
        plot_stress_test_results(
            stress_results=stress_results,
            chart_type='bar',
            save_path=f"{CHARTS_DIR}stress_test_results.png"
        )
        
        # Step 6: Create Excel Dashboard
        print("📋 Creating Excel dashboard...")
        dashboard_data = {
            'Executive_Summary': {
                'Portfolio_Sharpe': optimal_portfolio['sharpe_ratio'],
                'Expected_Return': optimal_portfolio['expected_return'],
                'Volatility': optimal_portfolio['volatility'],
                'ESG_Score': optimal_portfolio['avg_esg'],
                'VaR_95': var_results['VaR_95'],
                'VaR_99': var_results['VaR_99']
            },
            'Asset_Allocation': pd.DataFrame(list(optimal_portfolio['weights'].items()), 
                                           columns=['Asset', 'Weight']),
            'Risk_Metrics': pd.DataFrame([var_results]),
            'Stress_Test_Results': pd.DataFrame(stress_results).T,
            'Performance_Attribution': pd.DataFrame(list(attribution['by_asset'].items()),
                                                  columns=['Asset', 'Contribution'])
        }
        
        create_excel_dashboard(
            sheets_dict=dashboard_data,
            file_path=f"{OUTPUT_DIR}{EXCEL_FILENAME}"
        )
        
        print("🎉 Portfolio optimization completed successfully!")
        print(f"📁 Results saved to: {OUTPUT_DIR}")
        print(f"📊 Charts saved to: {CHARTS_DIR}")
        print(f"📋 Excel dashboard: {OUTPUT_DIR}{EXCEL_FILENAME}")
        
        return {
            'optimal_portfolio': optimal_portfolio,
            'risk_metrics': var_results,
            'stress_results': stress_results,
            'attribution': attribution
        }
        
    except Exception as e:
        print(f"❌ Error in main execution: {str(e)}")
        raise


if __name__ == "__main__":
    results = main() 