@echo off
echo ========================================
echo   Lancement de l'application GUI
echo ========================================
echo.
echo Installation de PyQt6 si necessaire...
pip install PyQt6
echo.
echo Lancement de l'application...
python -m src.gui
pause

