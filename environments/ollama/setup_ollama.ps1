$OllamaUrl = "https://ollama.com/download/ollama-windows-amd64.zip"
$OllamaDir = "$PSScriptRoot\bin"
$ModelsDir = "$PSScriptRoot\models"
$ZipPath = "$PSScriptRoot\ollama.zip"

if (!(Test-Path -Path $OllamaDir)) {
    New-Item -ItemType Directory -Path $OllamaDir | Out-Null
}

if (!(Test-Path -Path $ModelsDir)) {
    New-Item -ItemType Directory -Path $ModelsDir | Out-Null
}

if (!(Test-Path -Path "$OllamaDir\ollama.exe")) {
    Write-Host "Downloading Ollama standalone package..."
    Invoke-WebRequest -Uri $OllamaUrl -OutFile $ZipPath
    
    Write-Host "Extracting Ollama..."
    Expand-Archive -Path $ZipPath -DestinationPath $OllamaDir -Force
    
    Write-Host "Cleaning up temporary files..."
    Remove-Item -Path $ZipPath -Force
    Write-Host "Ollama installed successfully in $OllamaDir"
}
else {
    Write-Host "Ollama is already installed in $OllamaDir"
}
