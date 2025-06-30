import numpy as np

def calculate_performance_metrics(df, risk_free_rate=0.01):
    """
    Calcule des métriques de performance (Sharpe, drawdown...) à partir d'un DataFrame avec les colonnes :
    'Strategy_Return' et 'Cumulative_Strategy'
    """
    metrics = {}

    # Rendement annualisé
    total_return = df["Cumulative_Strategy"].iloc[-1] - 1
    num_years = (df.index[-1] - df.index[0]).days / 365.25
    annual_return = (1 + total_return) ** (1 / num_years) - 1
    metrics["Rendement annualisé (%)"] = round(annual_return * 100, 2)

    # Volatilité annualisée
    annual_volatility = df["Strategy_Return"].std() * np.sqrt(252)
    metrics["Volatilité annualisée (%)"] = round(annual_volatility * 100, 2)

    # Sharpe Ratio
    sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility
    metrics["Sharpe Ratio"] = round(sharpe_ratio, 2)

    # Maximum Drawdown
    cum_return = df["Cumulative_Strategy"]
    peak = cum_return.cummax()
    drawdown = (cum_return - peak) / peak
    max_drawdown = drawdown.min()
    metrics["Max Drawdown (%)"] = round(max_drawdown * 100, 2)

    return metrics
