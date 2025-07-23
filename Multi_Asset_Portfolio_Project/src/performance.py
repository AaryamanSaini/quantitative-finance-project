import numpy as np
import pandas as pd
from scipy import stats


def evaluate_managers(manager_returns, benchmark_returns, fees=None, dd_scores=None):
    """
    Evaluate and rank third-party managers by risk-adjusted metrics and due diligence.
    Args:
        manager_returns (pd.DataFrame): Monthly returns for each manager
        benchmark_returns (pd.Series): Monthly benchmark returns
        fees (dict): Annual fee for each manager (in decimal, e.g., 0.01)
        dd_scores (dict): Due diligence scores (0-10) for each manager
    Returns:
        pd.DataFrame: Manager evaluation table with all metrics and ranking
    """
    results = []
    for mgr in manager_returns.columns:
        rets = manager_returns[mgr]
        fee = fees.get(mgr, 0.01) if fees else 0.01
        dd = dd_scores.get(mgr, 7) if dd_scores else 7
        ann_ret = (1 + rets).prod() ** (12 / len(rets)) - 1 - fee
        ann_vol = rets.std() * np.sqrt(12)
        sharpe = ann_ret / ann_vol if ann_vol > 0 else np.nan
        # Alpha/Beta
        slope, intercept, r, p, std_err = stats.linregress(benchmark_returns, rets)
        alpha = intercept * 12
        beta = slope
        # Max drawdown
        cum = (1 + rets).cumprod()
        max_dd = (cum.cummax() - cum).max() / cum.cummax().max()
        results.append({
            'Manager': mgr,
            'Sharpe': sharpe,
            'Alpha': alpha,
            'Beta': beta,
            'Max_Drawdown': max_dd,
            'Fee': fee,
            'Due_Diligence': dd,
            'Net_Return': ann_ret,
            'Score': sharpe + alpha - max_dd - fee + dd/10
        })
    df = pd.DataFrame(results)
    df['Rank'] = df['Score'].rank(ascending=False)
    return df.sort_values('Rank')


def performance_attribution(portfolio_returns, asset_returns, weights, benchmark_returns=None):
    """
    Attribute performance by asset and vs. benchmark.
    Args:
        portfolio_returns (pd.Series): Portfolio returns (monthly)
        asset_returns (pd.DataFrame): Asset returns (monthly)
        weights (dict): Portfolio weights
        benchmark_returns (pd.Series): Benchmark returns (monthly)
    Returns:
        dict: Attribution results (by asset, vs. benchmark)
    """
    # By asset
    contrib = {a: (asset_returns[a] * weights.get(a, 0)).sum() for a in asset_returns.columns}
    total = sum(contrib.values())
    by_asset = {a: v/total for a, v in contrib.items()}
    # Vs benchmark
    vs_bench = None
    if benchmark_returns is not None:
        vs_bench = (portfolio_returns - benchmark_returns).sum()
    return {'by_asset': by_asset, 'vs_benchmark': vs_bench}


def dynamic_rebalancing(current_weights, target_weights, liquidity=None, transaction_costs=0.001):
    """
    Calculate optimal rebalancing trades given transaction costs and liquidity constraints.
    Args:
        current_weights (dict): Current portfolio weights
        target_weights (dict): Target portfolio weights
        liquidity (dict): Max tradable % per asset (optional)
        transaction_costs (float): Per-trade cost
    Returns:
        dict: Trades to execute, total transaction cost
    """
    trades = {}
    total_cost = 0
    for asset in target_weights:
        curr = current_weights.get(asset, 0)
        tgt = target_weights[asset]
        trade = tgt - curr
        # Apply liquidity constraint
        if liquidity and asset in liquidity:
            trade = np.clip(trade, -liquidity[asset], liquidity[asset])
        trades[asset] = trade
        total_cost += abs(trade) * transaction_costs
    return {'trades': trades, 'total_cost': total_cost}

# Example test (to be removed in production)
if __name__ == "__main__":
    idx = pd.date_range('2020-01-31', periods=36, freq='M')
    np.random.seed(42)
    mgrs = pd.DataFrame(np.random.normal(0.01, 0.04, (36, 10)), index=idx, columns=[f'M{i}' for i in range(10)])
    bench = pd.Series(np.random.normal(0.008, 0.03, 36), index=idx)
    fees = {f'M{i}': 0.01 + 0.002*i for i in range(10)}
    dd = {f'M{i}': np.random.randint(6, 10) for i in range(10)}
    print(evaluate_managers(mgrs, bench, fees, dd))
    # Attribution
    weights = {f'M{i}': 0.1 for i in range(10)}
    print(performance_attribution(mgrs.sum(axis=1), mgrs, weights, bench)) 