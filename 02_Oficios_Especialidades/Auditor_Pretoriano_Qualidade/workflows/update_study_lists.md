---
description: Atualiza automaticamente as listas de estudo (GBA/Patterns) com base no status atual da Studio Library.
---

# 🔄 Workflow: Atualizar Status de Estudo (v1.0)

Este workflow permite que o Agente reavalie a viabilidade dos modelos de jogo listados em `docs/` com base nos componentes atualmente disponíveis em `studio_library/registry.json`.

## 📋 Passo a Passo

### 1. Ler o Registro de Componentes
O Agente deve ler `studio_library/registry.json` para obter a lista de `id`s de componentes instalados (ex: `grid_manager`, `inventory_component`).

### 2. Analisar Dependências nas Listas
O Agente deve ler `docs/gba_study_list.md` (e futuramente `docs/game_design_patterns.md`).
Para cada jogo listado:
1.  Identifique a seção "Módulos Necessários".
2.  Verifique se os módulos listados como "Necessários" já existem no `registry.json`.
    *   *Nota*: A comparação pode ser por nome aproximado ou ID inferido.

### 3. Calcular Novo Status
Com base na verificação:
*   🟢 **Ready**: Todos os módulos críticos existem.
*   🟡 **Partial**: Alguns módulos existem, mas outros (menos críticos ou específicos) faltam.
*   🔴 **Blocked**: Módulos core (Physics, Turn Manager) estão ausentes.

### 4. Atualizar o Documento
Use `multi_replace_file_content` para atualizar a linha `> **Status:** ...` de cada jogo com a nova avaliação e uma breve justificativa.

## 🤖 Exemplo de Raciocínio (Chain of Thought)
1.  *Jogo*: "Golden Sun"
2.  *Requer*: `StudioTurnBasedBattle`, `StudioPartyManager`.
3.  *Registro*: Contém `inventory`, `grid`, `save`.
4.  *Balanço*: Falta `TurnBattle`.
5.  *Resultado*: 🔴 Blocked (Missing Turn-Based Battle).

## 🚀 Execução
Sempre que uma nova Skill ou Componente for criado (ex: "Acabei de criar o TurnManager"), execute este workflow para refletir o impacto desbloqueado.
