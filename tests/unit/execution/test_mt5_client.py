from types import SimpleNamespace
import sys

import pytest

from xau.execution.mt5_client import MT5_AVAILABLE

if not MT5_AVAILABLE:
    pytest.skip("MetaTrader5 non disponible", allow_module_level=True)


class DummyMT5:
    __version__ = "5.0.50"

    def __init__(self) -> None:
        self.initialized = False

    def initialize(self, login: int, password: str, server: str) -> bool:
        if login == 0:
            return False
        self.initialized = True
        return True

    def last_error(self):  # noqa: D401 - interface MT5
        return (1, "error")

    def symbol_info_tick(self, _):
        return SimpleNamespace(ask=1900.0, bid=1899.0)

    def symbol_info(self, _):
        return SimpleNamespace(point=0.1)

    TRADE_ACTION_DEAL = 1
    ORDER_TYPE_BUY = 0
    ORDER_TYPE_SELL = 1
    ORDER_TIME_GTC = 0
    ORDER_FILLING_IOC = 1
    TRADE_ACTION_MODIFY = 2

    def order_send(self, request):
        return SimpleNamespace(
            _asdict=lambda: {"price": request["price"], "retcode": 10009}
        )

    def positions_get(self, ticket: int):
        return [SimpleNamespace(symbol="XAUUSD", volume=0.01, type=self.ORDER_TYPE_BUY)]


@pytest.fixture()
def client_cls(monkeypatch):
    monkeypatch.setitem(sys.modules, "MetaTrader5", DummyMT5())
    import importlib

    from xau import execution as exec_mod

    importlib.reload(exec_mod.mt5_client)
    MT5Client = exec_mod.MT5Client

    yield MT5Client
    sys.modules.pop("MetaTrader5", None)


def test_connect_success(client_cls):
    client = client_cls()
    assert client.connect(login=1, password="p", server="s") is True


def test_connect_failure(client_cls):
    client = client_cls()
    from xau.execution import ConnexionRefusee

    with pytest.raises(ConnexionRefusee):
        client.connect(login=0, password="p", server="s")
