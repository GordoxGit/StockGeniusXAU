"""Indicateurs techniques basés sur Pandas."""

from __future__ import annotations

import numpy as np
import pandas as pd


def rsi(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Calcule le Relative Strength Index.

    Args:
        df: Données contenant une colonne ``close``.
        period: Période utilisée pour le calcul.

    Returns:
        Série du RSI.
    """
    close = df["close"]
    delta = close.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    avg_gain = up.rolling(window=period, min_periods=period).mean()
    avg_loss = down.rolling(window=period, min_periods=period).mean()
    rsi = pd.Series(np.nan, index=df.index)
    if len(df) >= period:
        rs = avg_gain.iloc[period] / avg_loss.iloc[period]
        rsi.iloc[period] = 100 - 100 / (1 + rs)
        prev_gain = avg_gain.iloc[period]
        prev_loss = avg_loss.iloc[period]
        for i in range(period + 1, len(df)):
            prev_gain = (prev_gain * (period - 1) + up.iloc[i]) / period
            prev_loss = (prev_loss * (period - 1) + down.iloc[i]) / period
            rsi.iloc[i] = 100 - 100 / (1 + prev_gain / prev_loss)
    return rsi


def macd(
    df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9
) -> pd.DataFrame:
    """Calcule la MACD (Moving Average Convergence Divergence).

    Args:
        df: Données avec une colonne ``close``.
        fast: Période de l'EMA rapide.
        slow: Période de l'EMA lente.
        signal: Période de la ligne signal.

    Returns:
        DataFrame avec colonnes ``macd``, ``signal`` et ``hist``.
    """
    close = df["close"]
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    hist = macd_line - signal_line
    return pd.DataFrame({"macd": macd_line, "signal": signal_line, "hist": hist})


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Calcule l'Average True Range.

    Args:
        df: Données contenant ``high``, ``low`` et ``close``.
        period: Période dissage.

    Returns:
        Série de l'ATR.
    """
    high = df["high"]
    low = df["low"]
    close = df["close"]
    tr = pd.concat(
        [
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs(),
        ],
        axis=1,
    ).max(axis=1)
    atr_series = tr.ewm(alpha=1 / period, adjust=False).mean()
    atr_series.iloc[:period] = np.nan
    return atr_series


def moving_average(df: pd.DataFrame, period: int) -> pd.Series:
    """Calcule la moyenne mobile simple.

    Args:
        df: Données avec une colonne ``close``.
        period: Fenêtre de lissage.

    Returns:
        Série de la SMA.
    """
    return df["close"].rolling(window=period).mean()
