# Gestion des secrets CI

Les clés et tokens nécessaires (par ex. `CODECOV_TOKEN`, `BINANCE_API_KEY`)
se configurent dans GitHub :

1. Ouvrez le dépôt sur GitHub puis **Settings → Secrets and variables → Actions**.
2. Cliquez sur **New repository secret** et saisissez le nom du secret.
3. Collez la valeur fournie puis validez.

Aucun secret ne doit être ajouté dans le code source ou le dépôt git.
