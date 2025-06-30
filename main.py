import yfinance as yf
from strategy import moving_average_crossover
from backtest import backtest_strategy
from metrics import calculate_performance_metrics
import pandas as pd

# Liste des tickers à tester
tickers = ["AAPL", "TSLA", "SPY", "MSFT", "AMZN"]

# Résultats stockés ici
results = []

# Paramètres
start_date = "2020-01-01"
end_date = "2024-12-31"

for ticker in tickers:
    print(f"\nTraitement de {ticker}...")

    # Téléchargement des données
    df = yf.download(ticker, start=start_date, end=end_date)
    if df.empty:
        print(f"⚠️ Pas de données pour {ticker}")
        continue

    # Application de la stratégie
    df = moving_average_crossover(df, short_window=20, long_window=50)
    df = backtest_strategy(df)

    # Calcul des métriques
    metrics = calculate_performance_metrics(df)
    metrics["Ticker"] = ticker
    results.append(metrics)

# Création du tableau récapitulatif
df_results = pd.DataFrame(results)
df_results = df_results[["Ticker", "Rendement annualisé (%)", "Volatilité annualisée (%)", "Sharpe Ratio", "Max Drawdown (%)"]]
df_results = df_results.sort_values("Sharpe Ratio", ascending=False)

# Affichage du tableau
print("\n=== COMPARAISON DES ACTIFS ===")
print(df_results.to_string(index=False))
