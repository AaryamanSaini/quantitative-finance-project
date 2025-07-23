import numpy as np
import pandas as pd


def calculate_var(returns, confidence_levels=[0.95, 0.99]):
    """
    Calculate Value at Risk (VaR) at specified confidence levels using historical simulation.
    Args:
        returns (pd.Series or pd.DataFrame): Portfolio or asset returns
        confidence_levels (list): List of confidence levels (e.g., [0.95, 0.99])
    Returns:
        dict: VaR values for each confidence level
    """
    if isinstance(returns, pd.DataFrame):
        returns = returns.sum(axis=1)
    var_results = {}
    for cl in confidence_levels:
        var = -np.percentile(returns.dropna(), 100 * (1 - cl))
        var_results[f"VaR_{int(cl*100)}"] = var
    return var_results


def stress_test_portfolio(returns, scenarios=None):
    """
    Perform scenario analysis for specified stress events.
    Args:
        returns (pd.DataFrame): Asset or portfolio returns (monthly)
        scenarios (dict): Dict of scenario_name: (start_date, end_date)
    Returns:
        dict: Scenario results (drawdown, return, volatility)
    """
    if scenarios is None:
        scenarios = {
            '2008_Crisis': ('2007-10-01', '2009-03-01'),
            'COVID_Crash': ('2020-02-01', '2020-04-01'),
            'Rate_Shock': None,  # Custom: -2% to all bonds in one month
            'Custom_Worst': None
        }
    results = {}
    for name, period in scenarios.items():
        if period:
            start, end = period
            mask = (returns.index >= start) & (returns.index <= end)
            sub = returns.loc[mask]
            port_ret = sub.sum(axis=1) if isinstance(sub, pd.DataFrame) else sub
            drawdown = (port_ret.cummin() - port_ret.cummax()).min()
            results[name] = {
                'total_return': port_ret.sum(),
                'volatility': port_ret.std() * np.sqrt(12),
                'max_drawdown': drawdown
            }
        elif name == 'Rate_Shock':
            # Apply -2% shock to bond assets
            shock = returns.copy()
            for col in shock.columns:
                if col in ['AGG', 'TIP', 'HYG']:
                    shock.iloc[-1][col] -= 0.02
            port_ret = shock.sum(axis=1)
            results[name] = {
                'total_return': port_ret.sum(),
                'volatility': port_ret.std() * np.sqrt(12),
                'max_drawdown': (port_ret.cummin() - port_ret.cummax()).min()
            }
        elif name == 'Custom_Worst':
            # Worst single month in history
            port_ret = returns.sum(axis=1)
            min_month = port_ret.idxmin()
            results[name] = {
                'worst_month': min_month,
                'return': port_ret.loc[min_month]
            }
    return results


def factor_analysis(returns, factors):
    """
    Calculate exposures to major risk factors using linear regression.
    Args:
        returns (pd.DataFrame): Asset or portfolio returns
        factors (pd.DataFrame): Factor returns (same index)
    Returns:
        pd.Series: Factor loadings (betas)
    """
    from sklearn.linear_model import LinearRegression
    X = factors.values
    y = returns.values
    reg = LinearRegression().fit(X, y)
    return pd.Series(reg.coef_, index=factors.columns)


def dynamic_correlation(returns, window=12):
    """
    Calculate rolling correlation matrices for the given window size (months).
    Args:
        returns (pd.DataFrame): Asset returns
        window (int): Rolling window size in months
    Returns:
        dict: {end_date: correlation matrix}
    """
    corrs = {}
    for i in range(window, len(returns)+1):
        end = returns.index[i-1]
        sub = returns.iloc[i-window:i]
        corrs[end] = sub.corr()
    return corrs

# Example test (to be removed in production)
if __name__ == "__main__":
    # Simulate returns for testing
    idx = pd.date_range('2018-01-31', periods=60, freq='M')
    np.random.seed(42)
    rets = pd.DataFrame(np.random.normal(0.01, 0.04, (60, 5)), index=idx, columns=[f'A{i}' for i in range(5)])
    print("VaR:", calculate_var(rets))
    print("Stress Test:", stress_test_portfolio(rets))
    # Simulate factors
    factors = pd.DataFrame(np.random.normal(0, 0.03, (60, 3)), index=idx, columns=['MKT', 'RFR', 'TERM'])
    print("Factor Analysis:", factor_analysis(rets.iloc[:,0], factors))
    print("Dynamic Correlation (last):", list(dynamic_correlation(rets, 12).values())[-1]) 