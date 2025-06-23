
import sys
import pytest

if sys.platform != "win32" or sys.version_info >= (3, 12):
    pytest.skip(
        "Tests MT5 ignorés hors Windows ou Python>=3.12",
        allow_module_level=True,
    )
