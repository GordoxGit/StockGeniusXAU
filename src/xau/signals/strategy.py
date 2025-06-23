"""Génération de signaux simples basés sur le RSI."""

from __future__ import annotations

import pandas as pd

from .indicators import atr, rsi


LONG = "LONG"
SHORT = "SHORT"
FLAT = "FLAT"


def generate_signal(
    df: pd.DataFrame,
    on: str = "close",
    confirmation: bool = False,
    rsi_period: int = 14,
    atr_period: int = 14,
) -> pd.Series:
    """Génère un signal directionnel.

    Args:
        df: Données de marché contenant ``high``, ``low`` et ``close``.
        on: Colonne utilisée pour le prix de clôture.
        confirmation: Active un filtre ATR si ``True``.

    Returns:
        Série de signaux ``LONG``, ``SHORT`` ou ``FLAT``.
    """
    data = df.rename(columns={on: "close"})
    signal = pd.Series(FLAT, index=data.index)
    data["rsi"] = rsi(data, period=rsi_period)
    signal[data["rsi"] > 70] = SHORT
    signal[data["rsi"] < 30] = LONG
    if confirmation:
        data["atr"] = atr(data, period=atr_period)
        threshold = data["atr"].median()
        signal[data["atr"] <= threshold] = FLAT
    return signal
