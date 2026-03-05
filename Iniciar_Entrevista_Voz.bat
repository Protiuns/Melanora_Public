@echo off
title Melanora - Entrevista por Voz
color 0B

echo ============================================================
echo.
echo   🎙️  Melanora Voice Interview v1.0
echo   Iniciando sistema de conversacao...
echo.
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/2] Verificando ambiente virtual de Python...
if not exist ".\01_Ambientes_Ferramentas\Python\bin\python.exe" (
    echo [ERRO] Python nao encontrado na pasta 01_Ambientes_Ferramentas!
    pause
    exit /b
)

echo [2/2] Iniciando interface de voz...
echo.
"01_Ambientes_Ferramentas\Python\bin\python.exe" "03_Cortex_Analitico\voice_interview.py"

echo.
echo Entrevista encerrada.
pause
