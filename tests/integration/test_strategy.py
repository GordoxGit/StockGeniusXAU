import pandas as pd

from xau.signals import FLAT, LONG, SHORT, generate_signal


def test_generate_signal() -> None:
    close = list(range(10)) + [5, 4]
    df = pd.DataFrame(
        {
            "close": close,
            "high": [c + 0.5 for c in close],
            "low": [c - 0.5 for c in close],
        }
    )
    out = generate_signal(df, confirmation=False, rsi_period=3, atr_period=3)
    assert out.iloc[3] == SHORT
    assert out.iloc[10] == FLAT
    assert out.iloc[11] == LONG

    out_conf = generate_signal(df, confirmation=True, rsi_period=3, atr_period=3)
    assert out_conf.iloc[8] == SHORT
    assert out_conf.iloc[11] == LONG
