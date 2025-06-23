"""Wrapper haut-niveau pour l'exécution des ordres."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from xau.signals import LONG, SHORT

from .mt5_client import MT5Client


@dataclass
class TradeResult:
    """Résultat d'une exécution."""

    status: str
    details: Optional[Dict] = None


class Broker:
    """Gestionnaire d'envoi d'ordres et de journalisation."""

    def __init__(
        self, client: MT5Client, journal_dir: Path | str = "logs/trades"
    ) -> None:
        self.client = client
        self.dry_run = os.getenv("XAU_ENV") == "paper"
        self.journal_dir = Path(journal_dir)
        self.journal_dir.mkdir(parents=True, exist_ok=True)

    def _log(self, entry: Dict) -> None:
        file = self.journal_dir / f"{datetime.utcnow():%Y-%m-%d}.jsonl"
        with file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def send_order(
        self, signal: str, price: float | None = None, volume: float = 0.01
    ) -> TradeResult:
        """Envoie un ordre selon le signal fourni."""
        timestamp = datetime.utcnow().isoformat()
        if signal not in (LONG, SHORT):
            result = TradeResult(status="IGNORED")
            self._log(
                {"timestamp": timestamp, "signal": signal, "status": result.status}
            )
            return result

        if self.dry_run:
            result = TradeResult(
                status="FILLED", details={"price": price, "mode": "paper"}
            )
        else:
            if signal == LONG:
                details = self.client.market_buy("XAUUSD", volume)
            else:
                details = self.client.market_sell("XAUUSD", volume)
            result = TradeResult(status="FILLED", details=details)
        self._log(
            {
                "timestamp": timestamp,
                "signal": signal,
                "status": result.status,
                "details": result.details,
            }
        )
        return result
