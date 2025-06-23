# StockGenius XAU

![CI](https://img.shields.io/github/actions/workflow/status/your‑org/StockGenius‑XAU/ci.yml?branch=main)
![Licence](https://img.shields.io/github/license/your‑org/StockGenius‑XAU)

> **Assistant IA personnel pour la prise de décision sur le **gold spot** (XAU/USD)**

StockGenius XAU est un projet open‑source de trading algorithmique non‑automatisé qui combine :

* Collecte de données granulaires (tick ➜ D1) ;
* Machine Learning (CatBoost GPU) et NLP pour l’analyse de sentiment ;
* Moteur d’auto‑apprentissage continu sur MetaTrader 5 ;
* Contrôles de risque alignés MiFID II / AMF ;
* Tableau de bord FastAPI + Grafana.

Le code est intégralement commenté en français et la conformité réglementaire est au cœur de l’architecture.fileciteturn3file0

---

## 1. Arborescence recommandée

```text
StockGenius‑XAU/
├── src/                  # Code métier (Python 3.11)
│   ├── data/            # Ingestion & nettoyage
│   ├── features/        # Feature engineering CatBoost
│   ├── models/         # Entraînement & inférence
│   ├── execution/      # Wrapper MT5
│   ├── risk/           # Limites, Kelly fractionnel...
│   └── utils/
├── tests/               # Unit, integration, functional
├── notebooks/           # Recherches ponctuelles
├── docs/                # Rapports PDF, specs & RFC
└── .github/workflows/   # CI (pytest + coverage)
```

Cette structure suit les principes de maintenabilité, testabilité et reproductibilité détaillés dans le rapport d’architecture optimale.fileciteturn3file0

---

## 2. Mise en route rapide

```bash
conda create -n xau python=3.11
conda activate xau
pip install -r requirements.txt
# Variables d’environnement sensibles
cp .env.example .env  # puis renseigner vos clés API/identifiants MT5
pytest                # exécute tous les tests
```

Une action GitHub CI (Ubuntu latest, Python 3.11/3.12) refuse tout merge si les tests ou la couverture (<85 %) échouent.fileciteturn3file7

---

## 3. Sources de données

| Provider                  | Granularité          | Coût     | Usage                    |
| ------------------------- | -------------------- | -------- | ------------------------ |
| **Dukascopy**             | Tick / M1            | Gratuit  | Backtesting primaire     |
| **MetaTrader 5 (FBS)**    | Tick temps‑réel      | Spread   | Flux live / Trading demo |
| **Alpha Vantage**         | Intraday M1 (limité) | Freemium | Redondance API           |
| **Refinitiv / Bloomberg** | Tick                 | \$\$     | Recherche avancée        |
| **Chainlink Oracles**     | Blockchain feeds     | Gas      | Veille DeFi              |

Chaque source est comparée (latence, profondeur historique, limitations) dans "XAU/USD Data Source Analysis".fileciteturn4file2

---

## 4. Ingénierie des caractéristiques & ML

* **Feature set cœur** : taux réels, DXY, ATR/Yang‑Zhang, SuperTrend, sentiment FinBERT.fileciteturn4file16
* **Labelling** : méthode *Triple‑Barrier* dynamique (barrières ATR).
* **Déséquilibre classes** : pondération ou *Focal Loss* dans CatBoost.
* **Validation** : *walk‑forward* + *TimeSeriesSplit*.

---

## 5. Backtesting & Validation

Vectorbt (JIT Numba) pour la recherche rapide, Backtrader pour le *walk‑forward* événementiel, Zipline‑Reloaded pour la comparaison factorielle. Recommandations mémoire (M1 data), benchmarks GPU vs CPU et gestion de la latence décrits dans le rapport dédié.fileciteturn3file7

---

## 6. Gestion des risques

Cadre avancé : Kelly fractionnel, *fixed‑fractional* 0 ,1 %, limite de perte journalière, contrôle de la courbe d’équité et *news blackout* sur NFP/FOMC. Pseudo‑code et exemples inclus dans "Risk Management Guide".fileciteturn3file9

---

## 7. Sécurité, conformité & déploiement

Checklist exhaustive MiFID II / ESMA 2024 + guides VPS hardening, kill‑switch IA, logging chiffré GDPR. Implémenter les contrôles avant toute mise en production.fileciteturn3file2

---

## 8. Moteur d’auto‑apprentissage MT5

Design cyclique :

1. Signal → 2. Exécution demo MT5 → 3. Logging SQLite/CSV → 4. Détection de drift → 5. *Incremental retrain* CatBoost (*init\_model*) → 6. Déploiement modèle → 7. Boucle feedback.fileciteturn3file4

Points clés : modularité, concept drift, rollback, orchestration *Windows Task Scheduler*.fileciteturn3file17

---

## 9. Optimisation matériel & énergie

Guide complet pour une station **Ryzen 5 5600X + RTX 3060** et un VPS Debian 12 :

* BIOS : PBO + Curve Optimizer.
* CUDA 12/cuDNN + undervolt GPU.
* ROI énergie vs temps de calcul, estimation tarif EDF 2025.fileciteturn4file1

---

## 10. Prompt engineering & contributions IA

Le guide explique comment rédiger des tickets GitHub/Jira optimisés pour Claude 4 (Sonnet/Opus) et Codex : sections context, DoD, critères, exemples few‑shot, exigence de commentaires français.fileciteturn4file9

---

## 11. Tests

```bash
pytest -m unit           # fonctions isolées
pytest -m integration    # pipeline Data→Signal→Order
pytest -m functional     # end‑to‑end MT5 demo
pytest-benchmark         # stress
```

Les mocks MT5 utilisent `pytest‑mock`; la couverture est publiée sur Codecov. Les résultats de validation sont archivés pour MiFID II RTS 6.fileciteturn3file2

---

## 12. Roadmap

* [x] Architecture v1 & CI
* [x] Pipeline d’ingestion Dukascopy
* [x] Backtester vectorbt + Backtrader
* [ ] Implémentation Risk Engine complet
* [ ] Boucle auto‑learning MT5 live demo
* [ ] Dashboard Grafana temps‑réel
* [ ] Déploiement VPS + kill‑switch réglementaire

---

## 13. Licence

MIT — voir `LICENSE`.

---

## 14. Références PDF internes

Tous les rapports PDF se trouvent dans `docs/` :

1. Architecture optimale (arch.pdf)fileciteturn3file0
2. Risk Management Guide (risk.pdf)fileciteturn3file9
3. Checklist Sécurité/Compliance (checklist.pdf)fileciteturn3file2
4. Backtesting Libraries (backtesting.pdf)fileciteturn3file7
5. Auto‑Learning MT5 (autolearn.pdf)fileciteturn3file4
6. Data Source Analysis (datasource.pdf)fileciteturn4file2
7. Feature Engineering (features.pdf)fileciteturn4file16
8. Hardware & Énergie (hw\_energy.pdf)fileciteturn4file1
9. Prompt Engineering (prompts.pdf)fileciteturn4file9
10. Dossier de Recherche (research.pdf)fileciteturn4file8

---

> *« Un algorithme n’est qu’un soldat ; sa stratégie réside dans votre rigueur. »*

## Roadmap

> *Calendrier indicatif avant mise en production (v1.0) — révisé le 23 juin 2025*

| Phase                                 | Période cible  | Livrables principaux                                                                                                                            | État        |
| ------------------------------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| **0 — Bootstrapping**                 | Semaine 1 (T0) | • Dépôt GitHub initial<br>• Arborescence `src/` & `tests/`<br>• CI GitHub Actions (`pytest`, `ruff`, `mypy`)<br>• Badge couverture Codecov      | ✅ Terminé   |
| **1 — Pipeline Données**              | Sem. 2 → 6     | • Collecte tick → D1 (Binance & Dukascopy)<br>• Stockage Parquet + DuckDB<br>• Normalisation fuseau horaire UTC<br>• Scripts QA « data sanity » | 🔄 En cours |
| **2 — Moteur de Signaux**             | Sem. 6 → 10    | • RSI, MACD, MM 20/50/200<br>• Entropie & ATR volatilité<br>• NLP sentiment news (FinBERT)                                                      | ⏳ Planifié  |
| **3 — Backtesting & Risque**          | Sem. 8 → 12    | • Backtesting vectorbt multi-timeframe<br>• Analyse drawdown & Sharpe<br>• Limites MiFID « fat-finger », taille max trade                       | ⏳ Planifié  |
| **4 — Exécution & Paper Trading**     | Sem. 12 → 16   | • Wrapper MT5 / MetaQuotes Gateway<br>• Gestion ordres IOC/GTC<br>• Journaux horodatés (Article 25)                                             | ⏳ Planifié  |
| **5 — Dashboard & Monitoring**        | Sem. 14 → 18   | • API FastAPI sécurisée (OAuth2)<br>• Grafana PnL & risques<br>• Alerting Telegram / Email                                                      | ⏳ Planifié  |
| **6 — Conformité & Audit**            | Sem. 16 → 20   | • Dossier RTS 6 auto-généré<br>• Archivage logs & trades (WORM)<br>• Rapports stress-tests ESMA                                                 | ⏳ Planifié  |
| **7 — Optimisation Hyper-paramètres** | Sem. 20 → 24   | • Grid & Bayesian search CatBoost<br>• Early stopping, k-fold OOS<br>• Tracking essais MLflow                                                   | ⏳ Planifié  |
| **8 — Go-Live contrôlé**              | Sem. 24 → 26   | • Passage live micro-lot<br>• Guardrails latence / risk-on-chain<br>• Revue code externe                                                        | ⏳ Planifié  |
| **9 — Post-lancement**                | Sem. 26 → +∞   | • Amélioration continue<br>• Ajout EUR/USD, GBP/USD, WTI, Silver<br>• Migration micro-services Kubernetes                                       | ⏳ Planifié  |
 

| Phase                                  | Période cible       | Livrables principaux                                                                                                                                    | État        |
| -------------------------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| **0 — Bootstrapping**                  | Semaine 1 (T0)      | – Dépôt GitHub initial<br>– Structure `src/` & `tests/`<br>– CI GitHub Actions (`pytest`, `ruff`, `mypy`)<br>– Badge couverture                         | ✅ Terminé   |
| **1 — Pipeline Données**               | Sem. 2 → 6          | – Collecte tick ↔ D1 Binance & Dukascopy<br>– Normalisation OHLCV Parquet + DuckDB<br>– Tests unitaires + fixtures<br>– Documentation « Data Contract » | 🔄 En cours |
| **2 — Moteur de Signaux (rule‑based)** | Sem. 6 → 10         | – Implémentation RSI, SMA, MACD<br>– Génération de signaux JSON (`BUY` / `SELL`) avec TP/SL<br>– Tests d’intégration pipeline **Data → Signal**         | ⏳ Planifié  |
| **3 — Backtesting & Metrics**          | Sem. 8 → 12         | – Vectorbt + Backtrader<br>– Walk‑forward & OOS split<br>– Tableaux de métriques (Sharpe, DD, Win %)                                                    | ⏳ Planifié  |
| **4 — Gestion du Risque & Compliance** | Sem. 10 → 14        | – Limites taille / valeur d’ordre<br>– Fat‑finger guard, kill switch<br>– Logs MiFID II (RTS 6)                                                         | ⏳ Planifié  |
| **5 — Paper Trading MT5**              | Sem. 12 → 16        | – Wrapper `MetaTrader5` Python<br>– Journalisation ordres demo<br>– Tests E2E & stress réseau                                                           | ⏳ Planifié  |
| **6 — Dashboard & Monitoring**         | Sem. 14 → 18        | – API FastAPI v1<br>– Dashboard Grafana (Equity Curve, PnL live)<br>– Alerting Prometheus + Discord Webhook                                             | ⏳ Planifié  |
| **7 — Amélioration ML (CatBoost GPU)** | Sem. 18 → 24        | – Feature engineering avancée (`lag`, `seasonality`, sentiment NLP)<br>– Hyperparameter tuning Optuna<br>– Validation k‑fold & OOS                      | ⏳ Planifié  |
| **8 — Beta fermée (live small size)**  | Sem. 25 → 28        | – Exécution live sur VPS<br>– Journal d’incidents<br>– KPI hebdo partagés                                                                               | ⏳ Planifié  |
| **9 — Release Production v1.0**        | À partir de Sem. 30 | – Audit sécurité & code review externe<br>– Documentation complète (`docs/` MkDocs)<br>– Licence OSS Finalisée<br>– Go‑live public                      | ⏳ Planifié  |

### Objectifs transverses

* **Qualité** : Maintenir ≥ 85 % de couverture tests, `ruff` sans erreur, typage `mypy` strict.
* **Sécurité** : Scan Dependabot hebdo, SCA, politique clés/API chiffrées.
* **Durabilité** : Suivi consommation GPU/énergie (< 1 kWh/jour en phase ML) d’après le rapport *Optimisation IA Trading — Hardware & Énergie*.
* **Documentation** : Mise à jour continue du Wiki et diagrammes d’architecture (PlantUML).
