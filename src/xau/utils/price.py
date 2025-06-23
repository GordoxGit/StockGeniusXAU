"""Fonctions liées aux prix."""

import re


def clean_price(valeur: str) -> float:
    """Nettoie un prix en remplaçant les séparateurs européens."""
    nombre = valeur.replace("\xa0", " ")
    nombre = nombre.replace(" ", "")
    nombre = nombre.replace(",", ".")
    return float(nombre)
