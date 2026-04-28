@echo off
REM ============================================================
REM  JARVIS - AI Voice Assistant | STOP
REM  Stoppt und entfernt den laufenden JARVIS Container
REM ============================================================

title JARVIS - Stop
color 0C

echo.
echo  ==========================================
echo   JARVIS - Stoppe Container...
echo  ==========================================
echo.

docker compose down

if %errorlevel% neq 0 (
    echo  [HINWEIS] Kein laufender Container gefunden oder Fehler beim Stoppen.
) else (
    echo.
    echo  JARVIS wurde erfolgreich gestoppt.
)

echo.
pause
