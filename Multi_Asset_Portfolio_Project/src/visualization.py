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