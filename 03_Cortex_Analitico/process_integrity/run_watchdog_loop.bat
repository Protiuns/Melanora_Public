@echo off
set "PY_EXE=%~dp0..\..\01_Ambientes_Ferramentas\Python\bin\python.exe"
set "WATCHDOG_PY=%~dp0integrity_watchdog.py"

echo [WATCHDOG] Loop Ativo. Monitorando integridade neural...

:loop
"%PY_EXE%" "%WATCHDOG_PY%"
timeout /t 60 /nobreak >nul
goto loop
