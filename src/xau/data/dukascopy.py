"""Téléchargement des données depuis Dukascopy."""

from __future__ import annotations

import lzma
import struct
import time
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import requests

from .schema import Interval

_BASE = "https://datafeed.dukascopy.com/datafeed/{symbol}/{year}/{month:02d}/{day:02d}/{hour:02d}h_ticks.bi5"


def _parse_bi5(content: bytes, base_time: datetime) -> pd.DataFrame:
    """Décompresse et parse un fichier bi5."""
    raw = lzma.decompress(content)
    records = []
    for i in range(0, len(raw), 20):
        ms, bid, ask, bid_vol, ask_vol = struct.unpack(
            ">Iffff", raw[i : i + 20]
        )
        ts = base_time + timedelta(milliseconds=ms)
        records.append((ts, bid, ask, bid_vol, ask_vol))
    df = pd.DataFrame(records, columns=["timestamp", "bid", "ask", "bid_volume", "ask_volume"])
    df.set_index("timestamp", inplace=True)
    return df


class DukascopyData:
    """Client simplifié pour Dukascopy."""

    def __init__(self, rate_limit: float = 0.2, threads: int = 5) -> None:
        self.rate_limit = rate_limit
        self.threads = threads

    def _download_hour(self, symbol: str, date: datetime) -> pd.DataFrame:
        url = _BASE.format(
            symbol=symbol,
            year=date.year,
            month=date.month - 1,
            day=date.day,
            hour=date.hour,
        )
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        ticks = _parse_bi5(resp.content, date)
        time.sleep(self.rate_limit)
        return ticks

    def fetch(self, symbol: str, start: datetime, end: datetime, interval: Interval = Interval.MIN1) -> pd.DataFrame:
        """Télécharge les données de ticks et agrège en chandeliers."""
        cursor = start.replace(minute=0, second=0, microsecond=0)
        all_ticks = []
        while cursor <= end:
            try:
                ticks = self._download_hour(symbol, cursor)
                all_ticks.append(ticks)
            except requests.HTTPError:
                pass
            cursor += timedelta(hours=1)
        if not all_ticks:
            return pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])
        df = pd.concat(all_ticks).sort_index()
        price = (df["bid"] + df["ask"]) / 2
        ohlc = price.resample(interval.value).ohlc()
        vol = df["bid_volume"].resample(interval.value).sum()
        result = pd.concat([ohlc, vol.rename("volume")], axis=1).reset_index()
        result.rename(columns={"index": "timestamp"}, inplace=True)
        return result

    def save_parquet(self, df: pd.DataFrame, out: Path, overwrite: bool = False) -> None:
        """Sauvegarde en Parquet partitionné par date."""
        df = df.copy()
        df["date"] = pd.to_datetime(df["timestamp"], utc=True).dt.date.astype(str)
        out.mkdir(parents=True, exist_ok=True)
        df.to_parquet(out, partition_cols=["date"], compression="zstd", engine="pyarrow", overwrite=overwrite)
