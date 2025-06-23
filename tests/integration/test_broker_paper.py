import sys
from types import SimpleNamespace

import pytest
from xau.signals import LONG


class DummyMT5:
    __version__ = "5.0.50"

    def initialize(self, *_, **__):
        return True

    def last_error(self):  # noqa: D401
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

    def positions_get(self, _):
        return [SimpleNamespace(symbol="XAUUSD", volume=0.01, type=self.ORDER_TYPE_BUY)]


@pytest.fixture(autouse=True)
def patch_mt5(monkeypatch):
    monkeypatch.setitem(sys.modules, "MetaTrader5", DummyMT5())
    import importlib
    from xau import execution as exec_mod

    importlib.reload(exec_mod.mt5_client)
    yield
    sys.modules.pop("MetaTrader5", None)


def test_paper_broker_log(tmp_path, monkeypatch):
    monkeypatch.setenv("XAU_ENV", "paper")
    from xau.execution import Broker, MT5Client

    class DummyClient(MT5Client):
        def market_buy(self, symbol: str, volume: float):  # noqa: D401
            return {"price": 1900.0, "retcode": 10009}

    broker = Broker(DummyClient(), journal_dir=tmp_path)
    broker.send_order(LONG, price=1900.0)
    log_file = next(tmp_path.iterdir())
    assert log_file.stat().st_size < 5 * 1024
