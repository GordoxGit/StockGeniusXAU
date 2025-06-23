"""Exceptions spécifiques au module d'exécution."""


class ConnexionRefusee(Exception):
    """Échec de connexion à MetaTrader 5."""


class MarcheFerme(Exception):
    """Le marché est fermé ou l'ordre a été rejeté."""


class SlippageExcessif(Exception):
    """Le slippage dépasse la tolérance autorisée."""
