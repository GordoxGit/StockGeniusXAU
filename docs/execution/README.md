# Module `xau.execution`

Ce composant gère l'envoi des ordres vers MetaTrader 5 ou en mode papier.

## Pré-requis

- Terminal MetaTrader 5 ouvert avec le compte démo configuré ;
- Bibliothèque Python `MetaTrader5` installée (version ≥ 5.0.44) ;
- Variables d'environnement `LOGIN`, `PASSWORD`, `SERVER` renseignées ou
  fournies au moment de la connexion ;
- Définir `XAU_ENV=paper` pour activer le mode *dry-run* sans envoi réel.

## Journalisation

Chaque ordre est enregistré dans `logs/trades/YYYY-MM-DD.jsonl`. Ces
fichiers sont horodatés pour répondre aux exigences MiFID II / RTS 6.

## Exemple rapide

```python
from xau.execution import Broker, MT5Client
from xau.signals import LONG

client = MT5Client()
client.connect(login=123456, password="demo", server="MetaQuotes-Demo")  # pragma: allowlist secret

broker = Broker(client)
result = broker.send_order(LONG, price=1900.0)
print(result)
```
