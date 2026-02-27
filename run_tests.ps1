Write-Host "Tests Unitaires" -ForegroundColor Cyan
pytest tests/unit/ -v

Write-Host "'nTests RobotFramework" -ForegroundColor Cyan
robot --pythonpath . --pythonpath src --outputdir logs tests/robot/

Write-Host "'nRapport Disponible : logs/report/html" -ForegroundColor Green