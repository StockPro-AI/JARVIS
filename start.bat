@echo off
REM ============================================================
REM  JARVIS - AI Voice Assistant | START
REM  One-Click Start via Docker Compose
REM ============================================================

title JARVIS - Running
color 0A

echo.
echo  ==========================================
echo   JARVIS - AI Voice Assistant
echo   Starte Container...
echo  ==========================================
echo.

REM --- Voraussetzungen pruefen ---
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [FEHLER] Docker nicht gefunden!
    echo  Fuehre zuerst setup.bat aus.
    pause
    exit /b 1
)

if not exist ".env" (
    echo  [FEHLER] .env Datei nicht gefunden!
    echo  Fuehre zuerst setup.bat aus oder erstelle die .env Datei.
    pause
    exit /b 1
)

REM --- Docker Compose starten ---
echo  Starte JARVIS mit docker compose...
echo  (Zum Beenden: Ctrl+C oder stop.bat in einem anderen Fenster)
echo.
docker compose up

REM --- Nach dem Beenden ---
echo.
echo  JARVIS wurde gestoppt.
pause
