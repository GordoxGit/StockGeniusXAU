from datetime import datetime, timezone
import lzma
import struct

import pandas as pd

from xau.data.dukascopy import DukascopyData, _parse_bi5
from xau.data.schema import Interval


def test_parse_bi5() -> None:
    base = datetime(2023, 10, 1, tzinfo=timezone.utc)
    # un tick à 0ms et un à 60000ms
    raw = struct.pack(
        ">IffffIffff",
        0,
        1900.0,
        1900.1,
        1.0,
        1.0,
        60000,
        1900.5,
        1900.6,
        2.0,
        2.0,
    )
    compressed = lzma.compress(raw)
    df = _parse_bi5(compressed, base)
    assert len(df) == 2
    assert df.index[0] == base
    assert df.index[1] == base + pd.Timedelta(milliseconds=60000)

def test_fetch_aggregate(monkeypatch):
    base = datetime(2023, 10, 1, tzinfo=timezone.utc)
    # ticks each 30 seconds for 2 minutes
    raw = struct.pack(
        ">IffffIffffIffffIffff",
        0, 1900.0, 1900.1, 1.0, 1.0,
        30000, 1900.2, 1900.3, 1.0, 1.0,
        60000, 1900.4, 1900.5, 1.0, 1.0,
        90000, 1900.6, 1900.7, 1.0, 1.0,
    )
    comp = lzma.compress(raw)
    monkeypatch.setattr("xau.data.dukascopy.requests.get", lambda *a, **k: type("R", (), {"content": comp, "raise_for_status": lambda self: None})())
    dc = DukascopyData()
    df = dc.fetch("XAUUSD", base, base + pd.Timedelta(minutes=1), Interval.MIN1)
    assert len(df) == 1
