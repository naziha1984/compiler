@echo off
REM Lance l'application GUI en masquant les warnings QSS
python -m src.gui 2>nul
if errorlevel 1 (
    echo Erreur lors du lancement de l'application
    pause
)

