import numpy as np
import pandas as pd
from scipy.optimize import minimize

# Example ESG scores for all assets (simulate for alternatives)
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

TRANSACTION_COSTS = 0.001  # 10 bps per trade


def optimize_portfolio(
    expected_returns,
    cov_matrix,
    esg_scores=ESG_SCORES,
    min_alt=0.2,
    max_single=0.3,
    max_asset=0.4,
    min_esg=7.0,
    risk_free_rate=0.02,
    transaction_costs=TRANSACTION_COSTS,
    prev_weights=None
):
    """
    Mean-variance optimization with institutional constraints and ESG scoring.
    Args:
        expected_returns (pd.Series): Annualized expected returns
        cov_matrix (pd.DataFrame): Annualized covariance matrix
        esg_scores (dict): ESG scores for each asset
        min_alt (float): Minimum allocation to alternatives (Hedge_Fund + Private_Equity)
        max_single (float): Max concentration in any single asset class
        max_asset (float): Max allocation to any asset
        min_esg (float): Minimum average ESG score
        risk_free_rate (float): Risk-free rate for Sharpe ratio
        transaction_costs (float): Per-trade cost
        prev_weights (np.array): Previous weights for transaction cost modeling
    Returns:
        dict: Optimal weights, Sharpe ratio, expected return, volatility, ESG score
    """
    n = len(expected_returns)
    bounds = [(0, max_asset)] * n
    tickers = expected_returns.index.tolist()
    alt_idx = [i for i, t in enumerate(tickers) if t in ['Hedge_Fund', 'Private_Equity']]
    esg_arr = np.array([esg_scores.get(t, 7.0) for t in tickers])

    def portfolio_stats(weights):
        port_return = np.dot(weights, expected_returns)
        port_vol = np.sqrt(np.dot(weights, np.dot(cov_matrix, weights)))
        sharpe = (port_return - risk_free_rate) / port_vol if port_vol > 0 else 0
        return port_return, port_vol, sharpe

    def objective(weights):
        # Negative Sharpe (since we minimize)
        port_return, port_vol, sharpe = portfolio_stats(weights)
        tc = 0
        if prev_weights is not None:
            tc = transaction_costs * np.sum(np.abs(weights - prev_weights))
        return -sharpe + tc

    constraints = [
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},  # Fully invested
        {'type': 'ineq', 'fun': lambda w: np.sum(w[alt_idx]) - min_alt},  # Alternatives min
        {'type': 'ineq', 'fun': lambda w: min_esg - (np.dot(w, esg_arr) / np.sum(w))},  # ESG constraint
        {'type': 'ineq', 'fun': lambda w: max_single - np.max(w)},  # Max single asset class
    ]

    x0 = np.ones(n) / n
    result = minimize(objective, x0, bounds=bounds, constraints=constraints)
    if not result.success:
        raise ValueError(f"Optimization failed: {result.message}")
    opt_weights = result.x
    port_return, port_vol, sharpe = portfolio_stats(opt_weights)
    avg_esg = np.dot(opt_weights, esg_arr)
    return {
        'weights': dict(zip(tickers, opt_weights)),
        'sharpe_ratio': sharpe,
        'expected_return': port_return,
        'volatility': port_vol,
        'avg_esg': avg_esg
    }

# Example test (to be removed in production)
if __name__ == "__main__":
    # Simulate some data for testing
    tickers = list(ESG_SCORES.keys())
    np.random.seed(42)
    exp_rets = pd.Series(np.random.uniform(0.05, 0.12, len(tickers)), index=tickers)
    cov = np.diag(np.random.uniform(0.02, 0.05, len(tickers)))
    res = optimize_portfolio(exp_rets, cov)
    print("Optimal Portfolio:", res) 