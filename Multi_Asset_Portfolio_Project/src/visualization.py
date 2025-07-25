import numpy as np
import matplotlib.pyplot as plt


def plot_efficient_frontier(weights_list, returns_list, vol_list, optimal_point, save_path=None):
    """
    Plot the efficient frontier and mark the optimal portfolio.
    Args:
        weights_list (list): List of portfolio weights
        returns_list (list): List of expected returns for each portfolio
        vol_list (list): List of volatilities for each portfolio
        optimal_point (tuple): (volatility, return) of the optimal portfolio
        save_path (str): If provided, save the plot to this path
    """
    plt.figure(figsize=(10, 6))
    plt.plot(vol_list, returns_list, 'b--', label='Efficient Frontier')
    plt.scatter(*optimal_point, c='red', marker='*', s=200, label='Optimal Portfolio')
    plt.xlabel('Annualized Volatility')
    plt.ylabel('Annualized Return')
    plt.title('Efficient Frontier with Optimal Portfolio')
    plt.legend()
    plt.grid(True)
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()


def plot_asset_allocation_pie(weights, save_path=None):
    """
    Plot an asset allocation pie chart with percentage labels.
    Args:
        weights (dict or pd.Series): Asset weights
        save_path (str): If provided, save the plot to this path
    """
    import matplotlib.pyplot as plt
    labels = list(weights.keys())
    sizes = list(weights.values())
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, counterclock=False)
    plt.title('Asset Allocation')
    plt.axis('equal')
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()


def plot_correlation_heatmap(corr_matrix, save_path=None):
    """
    Plot a correlation heatmap of all asset classes.
    Args:
        corr_matrix (pd.DataFrame): Correlation matrix
        save_path (str): If provided, save the plot to this path
    """
    import seaborn as sns
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f', square=True)
    plt.title('Correlation Heatmap of Asset Classes')
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()


def plot_rolling_performance(portfolio_returns, benchmark_returns, window=12, save_path=None):
    """
    Plot rolling performance (returns) vs benchmarks over time.
    Args:
        portfolio_returns (pd.Series): Portfolio returns (monthly)
        benchmark_returns (dict): Dict of benchmark name to returns (monthly)
        window (int): Rolling window size in months
        save_path (str): If provided, save the plot to this path
    """
    import matplotlib.pyplot as plt
    roll_port = portfolio_returns.rolling(window).mean()
    plt.figure(figsize=(12, 6))
    plt.plot(roll_port, label='Portfolio')
    for name, bench in benchmark_returns.items():
        plt.plot(bench.rolling(window).mean(), label=name)
    plt.title(f'Rolling {window}-Month Performance')
    plt.xlabel('Date')
    plt.ylabel('Rolling Return')
    plt.legend()
    plt.grid(True)
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()


def plot_risk_contribution_bar(weights, cov_matrix, save_path=None):
    """
    Plot a risk contribution bar chart by asset class.
    Args:
        weights (dict or pd.Series): Portfolio weights
        cov_matrix (pd.DataFrame): Covariance matrix of asset returns
        save_path (str): If provided, save the plot to this path
    """
    import matplotlib.pyplot as plt
    import numpy as np
    w = np.array(list(weights.values()))
    assets = list(weights.keys())
    # Marginal contribution to risk
    port_vol = np.sqrt(np.dot(w, np.dot(cov_matrix, w)))
    mcr = np.dot(cov_matrix, w) / port_vol
    # Risk contribution
    rc = w * mcr
    plt.figure(figsize=(10, 6))
    plt.bar(assets, rc)
    plt.ylabel('Risk Contribution')
    plt.title('Risk Contribution by Asset Class')
    plt.xticks(rotation=45)
    plt.grid(True, axis='y')
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()


def plot_stress_test_results(stress_results, chart_type='bar', save_path=None):
    """
    Plot stress test results as a radar or bar chart.
    Args:
        stress_results (dict): Scenario name to result dict (e.g., max_drawdown, total_return)
        chart_type (str): 'bar' or 'radar'
        save_path (str): If provided, save the plot to this path
    """
    import matplotlib.pyplot as plt
    import numpy as np
    scenarios = list(stress_results.keys())
    values = [stress_results[s].get('max_drawdown', 0) for s in scenarios]
    if chart_type == 'bar':
        plt.figure(figsize=(10, 6))
        plt.bar(scenarios, values, color='orange')
        plt.ylabel('Max Drawdown')
        plt.title('Stress Test Results - Max Drawdown by Scenario')
        plt.xticks(rotation=30)
        plt.grid(True, axis='y')
    elif chart_type == 'radar':
        angles = np.linspace(0, 2 * np.pi, len(scenarios), endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        ax.plot(angles, values, 'o-', linewidth=2)
        ax.fill(angles, values, alpha=0.25)
        ax.set_thetagrids(np.degrees(angles[:-1]), scenarios)
        ax.set_title('Stress Test Results - Max Drawdown (Radar)')
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()


def plot_manager_comparison_scatter(manager_metrics, save_path=None):
    """
    Plot a manager comparison scatter plot (risk vs return).
    Args:
        manager_metrics (pd.DataFrame): DataFrame with columns 'Net_Return' and 'Sharpe' or 'Volatility'
        save_path (str): If provided, save the plot to this path
    """
    import matplotlib.pyplot as plt
    x = manager_metrics['Sharpe'] if 'Sharpe' in manager_metrics else manager_metrics['Volatility']
    y = manager_metrics['Net_Return']
    labels = manager_metrics['Manager'] if 'Manager' in manager_metrics else manager_metrics.index
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, c='blue', s=100)
    for i, label in enumerate(labels):
        plt.annotate(label, (x.iloc[i], y.iloc[i]), textcoords="offset points", xytext=(5,5), ha='left', fontsize=9)
    plt.xlabel('Sharpe Ratio' if 'Sharpe' in manager_metrics else 'Volatility')
    plt.ylabel('Net Return')
    plt.title('Manager Comparison: Risk vs Return')
    plt.grid(True)
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()


def plot_performance_attribution_waterfall(attribution_dict, save_path=None):
    """
    Plot a performance attribution waterfall chart.
    Args:
        attribution_dict (dict): Asset or factor to contribution value
        save_path (str): If provided, save the plot to this path
    """
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter
    labels = list(attribution_dict.keys())
    values = list(attribution_dict.values())
    cum_values = [0]
    for v in values[:-1]:
        cum_values.append(cum_values[-1] + v)
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(labels, values, color=['green' if v >= 0 else 'red' for v in values])
    ax.set_title('Performance Attribution Waterfall Chart')
    ax.set_ylabel('Contribution')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.2%}'))
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.annotate(f'{value:.2%}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)
    plt.grid(True, axis='y')
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close() 