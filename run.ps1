Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  REPL - Langage d'expressions logiques" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Variables disponibles: A=true, B=false, C=true" -ForegroundColor Yellow
Write-Host "Tapez 'quit' pour quitter" -ForegroundColor Yellow
Write-Host ""
python -m src.repl A=true B=false C=true

