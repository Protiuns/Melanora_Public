---
name: Godot Integrity & Bug Analyst
description: Especialista em detectar, analisar e mitigar bugs em tempo real no Godot 4. Gerencia o sistema de auditoria e auditoria do estúdio.
---

# 🐞 Godot Integrity & Bug Analyst (v1.0)

Esta skill define os padrões para o sistema de monitoramento de saúde do Studio Puk 97. O objetivo é capturar falhas silenciosas (null references, performance drops, world escapes) antes que elas cheguem ao usuário final.

## 📦 Componentes Vinculados (Registry)
- `bug_analyst`: Central de logs e emissão de sinais globais.
- `integrity_guard`: Sentinela modular para monitoramento de nós específicos.
- `debug_overlay`: Interface visual (HUD) para monitoramento em runtime (Teclado: F12).

---

## 🏗️ Fluxo de Diagnóstico

### 1. Detecção Passiva
O `StudioBugAnalyst` deve estar configurado como um **Autoload** em todos os projetos. Ele escuta erros do sistema e relatórios dos Guards.

### 2. Monitoramento Ativo (`StudioIntegrityGuard`)
Adicione este componente a nós críticos (Player, Chefes, Gerenciadores de Inventário).

**Configurações Recomendadas:**
- **Check Null References**: Essencial durante a fase de desenvolvimento para garantir que todos os `@export` foram arrastados no editor.
- **Check World Bounds**: Útil para projéteis ou inimigos físicos que podem "atravessar o chão" e cair no infinito.
- **Monitor Performance**: Identifica picos de lag associados a um nó específico.

---

## 📝 Protocolo de Análise de Erros

Ao encontrar um bug através do sistema:

1. **Consultar o Log**: Verifique a pasta `user://` por arquivos `bug_report_*.json`.
2. **Análise de Contexto**: O relatório inclui o `source_path` do nó. Use isso para localizar a cena exata.
3. **Reprodução**: Se o erro for de performance, use o Profiller do Godot focado no nó identificado pelo Analyst.

---

## 🛠️ Exemplo de Implementação em Script

Se você precisar reportar um erro customizado dentro de uma lógica de gameplay:

```gdscript
func use_item(item_id: String):
    if not inventory.has(item_id):
        # Reportar para o Analyst central
        if has_node("/root/StudioBugAnalyst"):
            get_node("/root/StudioBugAnalyst").report(self, "Tentativa de usar item inexistente: " + item_id, StudioBugAnalyst.Severity.ERROR)
```

---

## 🔄 Integração com Outras Skills
- **Studio Library Master**: Garante que o registry esteja atualizado com novas ferramentas de debug.
- **Project Structure Guard**: Mantém os logs organizados e as ferramentas nos caminhos corretos.
- **Godot Scene Builder**: Instala Guards em cenas críticas durante a montagem.
