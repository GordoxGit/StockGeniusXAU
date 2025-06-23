"""Tests de fumée pour l'initialisation du projet."""

from xau import clean_price


def test_import() -> None:
    """Vérifie que le paquet s'importe correctement."""
    assert clean_price


def test_clean_price() -> None:
    """Vérifie le nettoyage du prix."""
    assert clean_price("1 234,56") == 1234.56
