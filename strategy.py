def moving_average_crossover(df, short_window=20, long_window=50):
    """
    Ajoute des signaux d'achat/vente basés sur le croisement de moyennes mobiles.
    """
    df = df.copy()
    df["SMA_short"] = df["Close"].rolling(window=short_window).mean()
    df["SMA_long"] = df["Close"].rolling(window=long_window).mean()
    
    df["Signal"] = 0
    df["Signal"] = (df["SMA_short"] > df["SMA_long"]).astype(int)
    df["Position"] = df["Signal"].diff()
    
    return df

def sma_rsi_strategy(df, short_window=20, long_window=50, rsi_period=14):
    df = df.copy()
    
    # SMA
    df["SMA_short"] = df["Close"].rolling(window=short_window).mean()
    df["SMA_long"] = df["Close"].rolling(window=long_window).mean()
    
    # RSI
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=rsi_period).mean()
    avg_loss = loss.rolling(window=rsi_period).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # Signaux combinés
    df["Signal"] = 0
    df.loc[(df["SMA_short"] > df["SMA_long"]) & (df["RSI"] > 50), "Signal"] = 1
    df.loc[(df["SMA_short"] < df["SMA_long"]) | (df["RSI"] < 45), "Signal"] = 0
    df["Position"] = df["Signal"].diff()

    return df
