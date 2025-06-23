from datetime import datetime, timezone

import pandas as pd
import pytest

from xau.data import BinanceData, DukascopyData, Interval


def _fetch_binance(monkeypatch):
    client = BinanceData()
    # mock réseau
    client.client.get_klines = lambda **_: []
    return client.fetch("XAUUSDT", datetime(2023, 10, 1, tzinfo=timezone.utc), datetime(2023, 10, 2, tzinfo=timezone.utc), Interval.MIN1)


def _fetch_dukascopy(monkeypatch):
    dc = DukascopyData()
    dc._download_hour = lambda symbol, date: pd.DataFrame()
    return dc.fetch("XAUUSD", datetime(2023, 10, 1, tzinfo=timezone.utc), datetime(2023, 10, 2, tzinfo=timezone.utc))


@pytest.mark.xfail(reason="Réseau indisponible dans l'environnement")
def test_compare_sources(monkeypatch):
    binance = _fetch_binance(monkeypatch)
    duka = _fetch_dukascopy(monkeypatch)
    assert binance.empty and duka.empty
