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

# Génère un graphique sur AAPL uniquement
if "AAPL" in tickers:
    df_aapl = yf.download("AAPL", start=start_date, end=end_date)
    df_aapl = moving_average_crossover(df_aapl, short_window=20, long_window=50)
    df_aapl = backtest_strategy(df_aapl)

    import matplotlib.pyplot as plt

    plt.figure(figsize=(12, 6))
    plt.plot(df_aapl["Cumulative_BuyHold"], label="Buy & Hold", linestyle="--")
    plt.plot(df_aapl["Cumulative_Strategy"], label="Stratégie SMA", linewidth=2)
    plt.title("Apple (AAPL) — Rendement Cumulé")
    plt.xlabel("Date")
    plt.ylabel("Capital (base 1.0)")
    plt.grid()
    plt.legend()

    # 🔽 Sauvegarde dans le dossier /figures
    plt.savefig("figures/aapl_backtest.png")
    plt.close()

# Création du tableau récapitulatif
df_results = pd.DataFrame(results)
df_results = df_results[["Ticker", "Rendement annualisé (%)", "Volatilité annualisée (%)", "Sharpe Ratio", "Max Drawdown (%)"]]
df_results = df_results.sort_values("Sharpe Ratio", ascending=False)

# Affichage du tableau
print("\n=== COMPARAISON DES ACTIFS ===")
print(df_results.to_string(index=False))
