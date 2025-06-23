"""Sous-package gérant l'ingestion des données de marché."""

from .binance import BinanceData
from .dukascopy import DukascopyData
from .schema import Candle, Interval

__all__ = ["BinanceData", "DukascopyData", "Candle", "Interval"]
