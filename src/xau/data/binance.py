"""Téléchargement des données Binance."""

from __future__ import annotations

import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from binance.client import Client  # type: ignore

from .schema import Interval


class BinanceData:
    """Client simplifié pour l'historique Binance."""

    def __init__(self, api_key: str | None = None, secret_key: str | None = None, rate_limit: float = 0.2) -> None:
        self.client = Client(api_key, secret_key, ping=False)
        self.rate_limit = rate_limit
        self.listing_dates: dict[str, datetime] = {"XAUUSDT": datetime(2019, 1, 1, tzinfo=timezone.utc)}

    def fetch(self, symbol: str, start: datetime, end: datetime, interval: Interval) -> pd.DataFrame:
        """Télécharge les chandeliers entre deux dates."""
        listing = self.listing_dates.get(symbol)
        if listing and start < listing:
            start = listing
        limit = 1000
        start_ts = pd.Timestamp(start)
        if start_ts.tzinfo is None:
            start_ts = start_ts.tz_localize("UTC")
        else:
            start_ts = start_ts.tz_convert("UTC")
        end_ts = pd.Timestamp(end)
        if end_ts.tzinfo is None:
            end_ts = end_ts.tz_localize("UTC")
        else:
            end_ts = end_ts.tz_convert("UTC")
        start_ms = int(start_ts.timestamp() * 1000)
        end_ms = int(end_ts.timestamp() * 1000)
        all_klines: list[list[str | float]] = []
        while True:
            klines = self.client.get_klines(
                symbol=symbol,
                interval=interval.value,
                limit=limit,
                startTime=start_ms,
                endTime=end_ms,
            )
            if not klines:
                break
            all_klines.extend(klines)
            last_open = klines[-1][0]
            if last_open >= end_ms:
                break
            start_ms = last_open + 1
            time.sleep(self.rate_limit)
        df = pd.DataFrame(
            all_klines,
            columns=[
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "quote_asset_volume",
                "number_of_trades",
                "taker_buy_base",
                "taker_buy_quote",
                "ignore",
            ],
        )
        df = df[["timestamp", "open", "high", "low", "close", "volume"]]
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
        df = df.astype({"open": float, "high": float, "low": float, "close": float, "volume": float})
        return df

    def save_parquet(self, df: pd.DataFrame, out: Path, overwrite: bool = False) -> None:
        """Sauvegarde les données en Parquet partitionné par date."""
        df = df.copy()
        df["date"] = df["timestamp"].dt.date.astype(str)
        if overwrite and out.exists():
            for item in out.glob("*"):
                if item.is_file():
                    item.unlink()
                else:
                    for sub in item.rglob("*"):
                        if sub.is_file():
                            sub.unlink()
                    subdir = item
                    if subdir.is_dir():
                        subdir.rmdir()
        out.mkdir(parents=True, exist_ok=True)
        df.to_parquet(out, partition_cols=["date"], compression="zstd", engine="pyarrow")
