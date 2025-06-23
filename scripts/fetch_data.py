"""CLI pour télécharger les données de marché."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from xau.data import BinanceData, DukascopyData, Interval


def main() -> None:
    parser = argparse.ArgumentParser(description="Télécharge les données XAU/USD")
    parser.add_argument("--source", choices=["binance", "dukascopy"], required=True)
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--interval", default="1m")
    parser.add_argument("--out", required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    interval = Interval(args.interval)
    start = pd.to_datetime(args.start, utc=True)
    end = pd.to_datetime(args.end, utc=True)

    if args.source == "binance":
        client = BinanceData()
    else:
        client = DukascopyData()

    df = client.fetch(args.symbol, start, end, interval)
    client.save_parquet(df, Path(args.out), overwrite=args.overwrite)


if __name__ == "__main__":
    main()
