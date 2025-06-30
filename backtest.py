def backtest_strategy(df):
    """
    Calcule le rendement cumulé de la stratégie par rapport au Buy & Hold.
    """
    df = df.copy()
    df["Daily_Return"] = df["Close"].pct_change()
    df["Strategy_Return"] = df["Daily_Return"] * df["Signal"].shift(1)

    df["Cumulative_BuyHold"] = (1 + df["Daily_Return"]).cumprod()
    df["Cumulative_Strategy"] = (1 + df["Strategy_Return"]).cumprod()
    
    return df

