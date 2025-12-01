Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Lancement de l'application GUI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Installation de PyQt6 si necessaire..." -ForegroundColor Yellow
pip install PyQt6
Write-Host ""
Write-Host "Lancement de l'application..." -ForegroundColor Green
python -m src.gui

