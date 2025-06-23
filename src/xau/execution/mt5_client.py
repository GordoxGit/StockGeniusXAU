"""Client bas-niveau pour interagir avec MetaTrader 5."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

import MetaTrader5 as mt5
from packaging import version

from .exceptions import ConnexionRefusee, MarcheFerme, SlippageExcessif


@dataclass
class MT5Client:
    """Wrapper simplifié autour de l'API MetaTrader 5."""

    slippage: int = 5

    def connect(self, login: int, password: str, server: str) -> bool:
        """Initialise la connexion au terminal MT5."""
        if version.parse(mt5.__version__) < version.parse("5.0.44"):
            raise RuntimeError("Version de MetaTrader5 trop ancienne")
        if not mt5.initialize(login=login, password=password, server=server):
            raise ConnexionRefusee(str(mt5.last_error()))
        return True

    def _check_result(self, request: Dict[str, Any], result: Any) -> Dict[str, Any]:
        if result is None:
            raise MarcheFerme("Aucun résultat retourné")
        res = result._asdict()
        # contrôle basique du slippage
        filled_price = res.get("price")
        if (
            filled_price
            and abs(filled_price - request.get("price", 0))
            > self.slippage * mt5.symbol_info(request["symbol"]).point
        ):
            raise SlippageExcessif()
        return res

    def market_buy(self, symbol: str, volume: float) -> Dict[str, Any]:
        """Envoie un ordre d'achat au marché."""
        price = mt5.symbol_info_tick(symbol).ask
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "slippage": self.slippage,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        return self._check_result(request, result)

    def market_sell(self, symbol: str, volume: float) -> Dict[str, Any]:
        """Envoie un ordre de vente au marché."""
        price = mt5.symbol_info_tick(symbol).bid
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,
            "slippage": self.slippage,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        return self._check_result(request, result)

    def close_order(self, ticket: int) -> Dict[str, Any]:
        """Ferme la position spécifiée."""
        pos = mt5.positions_get(ticket=ticket)
        if not pos:
            raise MarcheFerme("Position introuvable")
        position = pos[0]
        order_type = (
            mt5.ORDER_TYPE_SELL
            if position.type == mt5.ORDER_TYPE_BUY
            else mt5.ORDER_TYPE_BUY
        )
        price = (
            mt5.symbol_info_tick(position.symbol).bid
            if order_type == mt5.ORDER_TYPE_SELL
            else mt5.symbol_info_tick(position.symbol).ask
        )
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": position.symbol,
            "volume": position.volume,
            "type": order_type,
            "position": ticket,
            "price": price,
            "slippage": self.slippage,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        return self._check_result(request, result)

    def modify_order(self, ticket: int, price: float) -> Dict[str, Any]:
        """Modifie le prix d'un ordre en attente."""
        request = {
            "action": mt5.TRADE_ACTION_MODIFY,
            "order": ticket,
            "price": price,
        }
        result = mt5.order_send(request)
        return self._check_result(request, result)
