#!/usr/bin/env python3
"""
Simple Flask backend server for portfolio optimization dashboard.
Handles API calls from the frontend and runs the optimization.
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys
import os
import json
import tempfile
import pandas as pd

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'Multi_Asset_Portfolio_Project', 'src'))

# Import our modules
try:
    from data_collection import collect_market_data
    from optimization import optimize_portfolio
    from risk_analytics import calculate_var, stress_test
    from performance import calculate_risk_metrics
    from excel_export import create_excel_dashboard
    print("✅ All modules imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all required modules are in the Multi_Asset_Portfolio_Project/src directory")

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/run_optimization', methods=['POST'])
def run_optimization():
    """Run portfolio optimization with given parameters."""
    try:
        # Get parameters from frontend
        params = request.json
        risk_free_rate = params.get('riskFreeRate', 0.02)
        min_alt = params.get('minAlternatives', 0.2)
        max_single = params.get('maxSingle', 0.3)
        min_esg = params.get('minEsg', 7.0)
        
        print(f"🔄 Running optimization with parameters: {params}")
        
        # Collect market data
        prices, returns, metrics, corr = collect_market_data()
        
        # Calculate expected returns and covariance
        expected_returns = metrics['annualized_return']
        cov_matrix = returns.cov() * 12  # Annualize covariance
        
        # Run optimization
        result = optimize_portfolio(
            expected_returns=expected_returns,
            cov_matrix=cov_matrix,
            risk_free_rate=risk_free_rate,
            min_alt=min_alt,
            max_single=max_single,
            min_esg=min_esg
        )
        
        # Calculate additional risk metrics
        portfolio_weights = list(result['weights'].values())
        portfolio_returns = returns.dot(portfolio_weights)
        
        risk_metrics = {
            'VaR_95': calculate_var(portfolio_returns, 0.95),
            'VaR_99': calculate_var(portfolio_returns, 0.99),
            'Max_Drawdown': calculate_risk_metrics(portfolio_returns)['max_drawdown']
        }
        
        # Prepare response
        response = {
            'sharpe_ratio': result['sharpe_ratio'],
            'expected_return': result['expected_return'],
            'volatility': result['volatility'],
            'avg_esg': result['avg_esg'],
            'weights': result['weights'],
            'risk_metrics': risk_metrics
        }
        
        print(f"✅ Optimization completed successfully")
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Optimization error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/export_excel', methods=['POST'])
def export_excel():
    """Export portfolio data to Excel."""
    try:
        data = request.json
        print(f"📊 Exporting Excel with data: {list(data.keys())}")
        
        # Create Excel file
        sheets_dict = {
            'Portfolio_Summary': {
                'Sharpe_Ratio': data['sharpeRatio'],
                'Expected_Return': f"{data['expectedReturn']*100:.1f}%",
                'Volatility': f"{data['volatility']*100:.1f}%",
                'ESG_Score': f"{data['esgScore']:.1f}/10"
            },
            'Asset_Allocation': pd.DataFrame([
                {'Asset': asset, 'Weight': f"{weight*100:.1f}%"}
                for asset, weight in data['portfolio'].items()
            ]),
            'Risk_Metrics': pd.DataFrame([
                {'Metric': '95% VaR', 'Value': f"{data['riskMetrics']['VaR_95']*100:.2f}%"},
                {'Metric': '99% VaR', 'Value': f"{data['riskMetrics']['VaR_99']*100:.2f}%"},
                {'Metric': 'Max Drawdown', 'Value': f"{data['riskMetrics']['Max_Drawdown']*100:.2f}%"}
            ])
        }
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            create_excel_dashboard(sheets_dict, tmp.name)
            print(f"✅ Excel file created: {tmp.name}")
            return send_file(tmp.name, as_attachment=True, download_name='portfolio_optimization.xlsx')
            
    except Exception as e:
        print(f"❌ Excel export error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'message': 'Portfolio optimization backend is running'})

if __name__ == '__main__':
    print("🚀 Starting Portfolio Optimization Backend Server...")
    print("📍 Server will be available at: http://localhost:5000")
    print("🌐 Frontend can connect to: http://localhost:8080/frontend/index.html")
    app.run(host='0.0.0.0', port=5000, debug=True) 