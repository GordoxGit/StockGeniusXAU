# Module `xau.signals`

Ce module regroupe plusieurs indicateurs techniques classiques calculés en mémoire avec **pandas** :

- **RSI** – formule originale de J. W. Wilder (1978) avec exemples issus d'AskPython.
- **MACD** – convergence/divergence de moyennes mobiles exposée par Alpharithms.
- **ATR** – mesure de volatilité décrite sur Investopedia.
- **Moyennes mobiles** – simples (SMA) via `pandas.Series.rolling`.

```python
from xau.signals import rsi, macd, atr, moving_average
```

Un exemple de backtest léger peut être réalisé avec [vectorbt](https://vectorbt.dev/):

```python
from xau.signals import generate_signal
signal = generate_signal(df)
```
