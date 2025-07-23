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