@echo off
title Ollama Local Manager
setlocal enabledelayedexpansion

set "OLLAMA_DIR=%~dp0bin"
set "OLLAMA_EXE=%OLLAMA_DIR%\ollama.exe"
set "OLLAMA_MODELS=%~dp0models"
set "OLLAMA_HOST=127.0.0.1:11434"

if not exist "%OLLAMA_EXE%" (
    echo [ERROR] Ollama not found. Run setup_ollama.ps1 first.
    pause
    exit /b 1
)

echo Starting Ollama Locally...
echo Host: %OLLAMA_HOST%
echo Models stored in: %OLLAMA_MODELS%
"%OLLAMA_EXE%" serve
