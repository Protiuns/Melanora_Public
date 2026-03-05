---
name: Project Version Control & Backup Guard
description: Gerencia o sistema de versionamento local e backups automáticos do estúdio, garantindo a segurança dos dados através de snapshots zipados e logs de alteração.
---

# 💾 Project Version Control & Backup Guard (v1.0)

Esta skill é responsável por garantir que o progresso do estúdio nunca seja perdido. Ela gerencia a criação de "Pontos de Restauração" (Snapshots) do projeto inteiro, permitindo reverter erros catastróficos.

## 🎯 Quando usar:
- Antes de refatorações grandes ou arriscadas.
- Ao finalizar um marco importante (Milestone).
- Quando o usuário solicita "backup", "zipar projeto" ou "salvar versão".

---

## 📦 Estrutura de Backup

Os backups são armazenados localmente em:
`/_backups/` (na raiz do workspace)

### Formato de Arquivo
`Backup_v{Versao}_{Data}_{Hora}.zip`
Exemplo: `Backup_v1.0_2024-03-24_1530.zip`

### O que é ignorado (Exclusões):
Para economizar espaço, as seguintes pastas **NÃO** entram no backup:
- `.godot/` (Cache da engine, regenerável e pesado)
- `.import/` (Cache de assets)
- `tmp/` (Arquivos temporários)
- `_backups/` (Para evitar recursão infinita)

---

## 🛠️ Workflow de Backup (Manual ou Automático)

Para criar um novo backup, o Agente deve:

1.  **Ler o Histórico:** Verificar `/_backups/backup_log.md` para determinar a próxima versão.
2.  **Criar o Zip:** Usar script PowerShell para compactar todo o workspace (respeitando exclusões).
3.  **Registrar:** Adicionar uma entrada no `backup_log.md` com a descrição das mudanças.

### Script PowerShell Padrão (Flexível)
O script aceita um parâmetro de diretório alvo. Se não especificado, faz backup de tudo (`.`).

```powershell
$target = "." # Pode ser alterado para "projects/meu_jogo"
Compress-Archive -Path $target -DestinationPath $dest
```

---

## 📜 Log de Versões (`backup_log.md`)

Mantenha este arquivo na pasta `_backups/`.

```markdown
# Histórico de Backups

## v1.0 - 2024-03-24 15:30
- Estado inicial do sistema de backup.
- Projetos: puk_mam, tiroteando.
- Studio Library estável.

## v1.1 - ...
```

---

## ⚠️ Recuperação de Desastres

Se o usuário pedir para "restaurar" ou "voltar versão":
1.  **NUNCA delete o projeto atual imediatamente.**
2.  Renomeie a pasta atual para `_OLD_Current`.
3.  Descompacte o backup solicitado.
4.  Valide se está funcionando.
5.  Só então pergunte se pode remover a pasta `_OLD`.
