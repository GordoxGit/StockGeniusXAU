import pandas as pd

from xau.signals import generate_signal
from xau.signals.backtest import run_backtest


def test_run_backtest() -> None:
    close = [1, 2, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2]
    df = pd.DataFrame(
        {
            "close": close,
            "high": [c + 0.5 for c in close],
            "low": [c - 0.5 for c in close],
        }
    )
    signal = generate_signal(df, rsi_period=3, atr_period=3)
    pf = run_backtest(df, signal)
    assert pf.stats()["Total Return [%]"] is not None
