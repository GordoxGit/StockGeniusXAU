"""Backtest léger en mémoire avec vectorbt."""

from __future__ import annotations

import pandas as pd
import vectorbt as vbt

from .strategy import FLAT, LONG, SHORT


def run_backtest(
    df: pd.DataFrame,
    signal: pd.Series,
    on: str = "close",
    cash: float = 1000.0,
    fees: float = 0.0,
) -> vbt.Portfolio:
    """Exécute un backtest simple.

    Args:
        df: Données de marché.
        signal: Série générée par :func:`generate_signal`.
        on: Colonne du prix de référence.
        cash: Capital initial.
        fees: Frais de transaction proportionnels.

    Returns:
        Objet ``Portfolio`` vectorbt.
    """
    price = df[on]
    entries = signal == LONG
    exits = signal.shift().eq(LONG) & (signal != LONG)
    short_entries = signal == SHORT
    short_exits = signal.shift().eq(SHORT) & (signal != SHORT)
    pf = vbt.Portfolio.from_signals(
        price,
        entries=entries,
        exits=exits,
        short_entries=short_entries,
        short_exits=short_exits,
        init_cash=cash,
        fees=fees,
        freq="D",
    )
    return pf
