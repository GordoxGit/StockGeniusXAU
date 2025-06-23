import pandas as pd

from xau.signals import atr, macd, moving_average, rsi


def test_rsi_reference() -> None:
    prices = [
        44.34,
        44.09,
        44.15,
        43.61,
        44.33,
        44.83,
        45.10,
        45.42,
        45.84,
        46.08,
        45.89,
        46.03,
        45.61,
        46.28,
        46.28,
        46.00,
        46.03,
        46.41,
        46.22,
        45.64,
        46.21,
    ]
    df = pd.DataFrame({"close": prices})
    out = rsi(df)
    assert round(out.iloc[14], 2) == 70.46
    assert round(out.iloc[15], 2) == 66.25


def test_macd_reference() -> None:
    data = {
        "close": [
            77.44539475,
            77.04557544,
            74.89697204,
            75.856461,
            75.09194679,
            76.20263178,
            75.2301837,
            73.84891755,
            75.0113527,
            77.14481412,
            77.33058367,
            76.85652616,
            75.39394758,
            76.7763823,
            76.64038513,
            77.20512022,
            76.66007339,
            70.90497216,
            70.23598702,
            71.817561,
            71.565308,
            72.495697,
            72.908951,
            72.699074,
            73.712648,
        ]
    }
    df = pd.DataFrame(data)
    out = macd(df)
    assert round(out["macd"].iloc[24], 3) == -1.097
    assert round(out["signal"].iloc[24], 3) == -0.987


def test_atr_reference() -> None:
    df = pd.DataFrame(
        {
            "high": [10, 12, 11, 13, 15],
            "low": [8, 9, 9, 10, 12],
            "close": [9, 11, 10, 12, 14],
        }
    )
    out = atr(df, period=3)
    assert round(out.iloc[4], 3) == 2.654


def test_moving_average() -> None:
    df = pd.DataFrame({"close": [1, 2, 3, 4, 5]})
    out = moving_average(df, 3)
    assert pd.isna(out.iloc[0]) and pd.isna(out.iloc[1])
    assert out.iloc[2] == 2.0
    assert out.iloc[3] == 3.0
    assert out.iloc[4] == 4.0
