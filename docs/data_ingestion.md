# Ingestion des données

Ce module fournit une interface unifiée pour télécharger les prix XAU/USD.

- **BinanceData** utilise l'API de Binance pour récupérer les chandeliers.
- **DukascopyData** télécharge les ticks puis les agrège en chandeliers.

Les données sont stockées au format **Parquet** compressé (zstd) et peuvent
ensuite être chargées facilement dans DuckDB pour les analyses.
