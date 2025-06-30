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
