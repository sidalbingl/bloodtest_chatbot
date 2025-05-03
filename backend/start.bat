@echo off
echo FastAPI sunucusu başlatılıyor...
uvicorn main:app --reload --port 8000
pause
