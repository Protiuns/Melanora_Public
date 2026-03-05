@echo off
chcp 65001 >nul
title MELANORA HUB v5.0 - PREMIUM ACCESS
setlocal enabledelayedexpansion

:: Detectar Caminho Raiz
set "BASE_DIR=%~dp0"
set "PY_EXE=%BASE_DIR%.venv\bin\python.exe"
set "DASH_DIR=%BASE_DIR%03_Cortex_Analitico\dashboard"

echo.
echo  💎 MELANORA PREMIUM HUB v5.0
echo  ----------------------------
echo  [INFRA] Verificando integridade neural...

:: Comando Central
if "%1"=="--stop" (
    "%PY_EXE%" "%BASE_DIR%melanora.py" stop
) else if "%1"=="--status" (
    "%PY_EXE%" "%BASE_DIR%melanora.py" status
) else (
    echo  [CORE] Inicializando Mente Fisica...
    "%PY_EXE%" "%BASE_DIR%melanora.py" start
)

echo.
echo  🌓 Sistema em Fluxo.
pause
