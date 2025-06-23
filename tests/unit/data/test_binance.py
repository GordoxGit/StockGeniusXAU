from datetime import datetime, timezone

import pandas as pd

from xau.data.binance import BinanceData, Interval


def test_start_before_listing() -> None:
    client = BinanceData()
    start = datetime(2010, 1, 1, tzinfo=timezone.utc)
    end = datetime(2010, 1, 2, tzinfo=timezone.utc)
    # on monkeypatch la méthode d'appel réseau pour éviter la requête
    calls = {
        "n": 0
    }
    def mock_get_klines(**_):
        if calls["n"] == 0:
            calls["n"] += 1
            return [[0, "1", "1", "1", "1", "1", 0, 0, 0, 0, 0, 0]]
        return []

    client.client.get_klines = mock_get_klines
    df = client.fetch("XAUUSDT", start, end, Interval.DAY1)
    assert len(df) == 1

def test_save_parquet(tmp_path) -> None:
    client = BinanceData()
    data = {
        "timestamp": pd.to_datetime(["2023-10-01T00:00:00Z", "2023-10-01T01:00:00Z"]),
        "open": [1, 2],
        "high": [1, 2],
        "low": [1, 2],
        "close": [1, 2],
        "volume": [1, 1],
    }
    df = pd.DataFrame(data)
    client.save_parquet(df, tmp_path)
    assert any(tmp_path.iterdir())
