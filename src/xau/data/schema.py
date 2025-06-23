"""Schémas de données pour l'ingestion."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Interval(str, Enum):
    """Intervalle de temps utilisé pour les chandeliers."""

    MIN1 = "1m"
    MIN5 = "5m"
    HOUR1 = "1h"
    DAY1 = "1d"


@dataclass
class Candle:
    """Représente un chandelier OHLCV."""

    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
