---
description: Gera um backup completo do workspace atual em formato ZIP, versionado e logado.
---

# 📦 Workflow: Criar Backup do Projeto

Este workflow cria um snapshot seguro do workspace `Puk 97`.

## 1. Preparação
Certifique-se que a pasta `_backups` existe.

// turbo
1. Criar diretório `_backups` se não existir.
```powershell
if (-not (Test-Path "_backups")) { New-Item -ItemType Directory -Path "_backups" }
if (-not (Test-Path "_backups/backup_log.md")) { New-Item -ItemType File -Path "_backups/backup_log.md" -Value "# Histórico de Backups`n`n" }
```

## 2. Definir Versão e Nome
O Agente deve ler o log para decidir a versão. Por padrão, incremente a última.
(Como este é um script automático, usaremos Timestamp como identificador principal se não houver input).

## 3. Executar Backup
Compacta as pastas críticas: `projects`, `studio_library`, `.agent`, `docs` e arquivos da raiz.

// turbo
2. Gerar arquivo ZIP
```powershell
# --- CONFIGURAÇÃO ---
# O usuário pode solicitar backup de uma subpasta específica. 
# Para mudar, altere o valor abaixo (Ex: "projects/puk_mam" ou "." para tudo)
$targetDir = "." 
# --------------------

$date = Get-Date -Format "yyyy-MM-dd_HH\.-mm"
$backupName = "Backup_Puk97_$date.zip"
$destPath = "_backups/$backupName"

Write-Host "Iniciando backup de: '$targetDir' para '$destPath'..."

# Define o que será incluído baseado no alvo
if ($targetDir -eq ".") {
    # Backup Completo (Root)
    $folders = @("projects", "studio_library", ".agent", "docs", "resources")
    $files = Get-ChildItem -Path . -File | ForEach-Object { $_.Name }
} else {
    # Backup Específico (Subpasta)
    if (-not (Test-Path $targetDir)) {
        Write-Error "A pasta '$targetDir' não existe!"
        exit 1
    }
    $folders = @($targetDir)
    $files = @()
}

# Verifica consistência
$validPaths = @()
foreach ($f in $folders) {
    if (Test-Path $f) { $validPaths += $f }
}
foreach ($f in $files) {
    if (Test-Path $f) { $validPaths += $f }
}

if ($validPaths.Count -eq 0) {
    Write-Error "Nenhum arquivo válido encontrado para backup em '$targetDir'."
    exit 1
}

Compress-Archive -Path $validPaths -DestinationPath $destPath -Update
Write-Host "Backup Concluído Com Sucesso!"
```

## 4. Atualizar Log
O usuário deve ser informado para atualizar o `backup_log.md` manualmente ou o Agente faz isso no próximo passo.

// turbo
3. Listar backups recentes
```powershell
Get-ChildItem "_backups" *.zip | Sort-Object LastWriteTime -Descending | Select-Object -First 5 Name, Length, LastWriteTime
```
