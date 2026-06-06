Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m uvicorn backend.main:app --reload --port 8000"
Start-Sleep -Seconds 2
Start-Process "http://localhost:8000"
