@echo off
REM ============================================================
REM  JARVIS - AI Voice Assistant | SETUP (Ersteinrichtung)
REM  Fuehre dieses Skript EINMALIG aus, bevor du start.bat
  verwendest.
REM ============================================================

title JARVIS - Setup
color 0A

echo.
echo  ==========================================
echo   JARVIS Setup - Ersteinrichtung
echo  ==========================================
echo.

REM --- Schritt 1: Docker pruefen ---
echo [1/4] Pruefe Docker Installation...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [FEHLER] Docker ist nicht installiert oder nicht im PATH!
    echo  Bitte installiere Docker Desktop: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo  Docker gefunden.
echo.

REM --- Schritt 2: .env erstellen ---
echo [2/4] Konfiguration...
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo  .env Datei wurde aus .env.example erstellt.
        echo.
        echo  WICHTIG: Trage jetzt deine API-Keys in die .env Datei ein!
        echo  Datei: %CD%\.env
        echo.
        echo  Benoetigt:
        echo    GEMINI_API_KEY  - https://aistudio.google.com/app/apikey
        echo    NEWS_API_KEY    - https://newsapi.org/register
        echo.
        notepad.exe ".env"
        echo  Druecke eine Taste, nachdem du die .env gespeichert hast...
        pause >nul
    ) else (
        echo  [WARNUNG] .env.example nicht gefunden. Erstelle leere .env...
        echo GEMINI_API_KEY=dein_api_key_hier> .env
        echo NEWS_API_KEY=dein_api_key_hier>> .env
        notepad.exe ".env"
        pause >nul
    )
) else (
    echo  .env Datei existiert bereits - wird nicht ueberschrieben.
)
echo.

REM --- Schritt 3: Docker Image bauen ---
echo [3/4] Baue Docker Image (kann einige Minuten dauern)...
echo.
docker compose build --no-cache
if %errorlevel% neq 0 (
    echo  [FEHLER] Docker Build fehlgeschlagen!
    pause
    exit /b 1
)
echo.
echo  Docker Image erfolgreich gebaut!
echo.

REM --- Schritt 4: Abschluss ---
echo [4/4] Setup abgeschlossen!
echo.
echo  ==========================================
echo   Setup erfolgreich!
echo   Starte JARVIS mit: start.bat
echo  ==========================================
echo.
pause
