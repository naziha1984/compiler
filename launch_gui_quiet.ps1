# Lance l'application GUI en masquant les warnings QSS
$ErrorActionPreference = 'SilentlyContinue'
python -m src.gui *>$null

