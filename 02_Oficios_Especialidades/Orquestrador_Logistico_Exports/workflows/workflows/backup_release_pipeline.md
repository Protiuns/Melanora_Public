# Workflow: Pipeline de Backup e Release

Garante que cada entrega seja segura e versionada.

## 🔄 Passos
1.  **Snapshot**: Criar um backup ZIP do estado atual usando a skill de `project_version_control`.
2.  **Log de Alterações**: Registrar o que foi mudado desde o último backup.
3.  **Build**: Executar `godot_export` para a plataforma alvo.
4.  **Delivery**: Mover o build para a pasta `_exports` e atualizar o log de delivery.

---
*Objetivo: Entrega segura e rastreável.*
