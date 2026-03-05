---
name: Skill Ecosystem Auditor
description: Avalia redundâncias, gaps e problemas no ecossistema de skills, gerando recomendações de melhoria.
---

# 🔍 Skill Ecosystem Auditor (v1.0)

Esta skill é responsável por **auditar o ecossistema** de skills e componentes, identificando problemas e oportunidades de melhoria.

## 🎯 Quando Executar Auditoria

- Após criar várias skills novas
- Quando há confusão sobre qual skill usar
- Periodicamente (a cada 10+ conversas)
- Quando solicitado pelo usuário

---

## 📋 Checklist de Auditoria

### 1. Análise de Triggers
```
Para cada skill no skill_registry.json:
  Para cada trigger da skill:
    Verificar se existe em outra skill
    Se sim → AUDIT: trigger_conflict
```

### 2. Análise de Dependências
```
Para cada skill:
  Para cada depends_on:
    Verificar se skill existe
    Se não → AUDIT: dead_dependency
  
  Verificar ciclos:
    Se A→B→A → AUDIT: circular_dependency
```

### 3. Análise de Cobertura Dimensional
```
Para cada skill com dimension="2d":
  Verificar se existe equivalente "3d"
  Se não → avaliar se é necessário
```

### 4. Análise de Escopo
```
Comparar outputs de todas as skills:
  Se dois outputs são muito similares → AUDIT: overlapping_scope
```

### 5. Análise de Gaps
```
Lista de áreas comuns de gamedev:
  - Movimentação ✓
  - Combate ✓
  - IA ✓
  - UI ✓
  - Áudio ✓
  - Save/Load ✗
  - Multiplayer ✗
  - Localização ✗
  
Para cada ✗ → avaliar necessidade
```

---

## 📊 Tipos de Problemas

| Tipo | Severidade | Ação |
|------|------------|------|
| `trigger_conflict` | 🔴 Alta | Diferenciar triggers |
| `dead_dependency` | 🔴 Crítica | Corrigir referência |
| `circular_dependency` | 🔴 Crítica | Quebrar ciclo |
| `overlapping_scope` | 🟡 Média | Consolidar ou clarificar fronteira |
| `missing_dimension_pair` | 🟡 Média | Criar par ou tornar universal |
| `missing_coverage` | 🟡 Média | Criar skill se necessário |
| `orphan_skill` | 🟢 Baixa | Revisar necessidade |

---

## 🛠️ Processo de Auditoria

### Passo 1: Carregar Registros
```
Ler: skill_registry.json
Ler: component_registry.json
Ler: audit_report.json (anterior)
```

### Passo 2: Executar Verificações
```
Para cada regra em audit_rules:
  Executar verificação
  Se problema encontrado:
    Adicionar a current_issues
```

### Passo 3: Calcular Estatísticas
```
Contar skills por categoria
Contar skills por dimensão
Contar issues por status
```

### Passo 4: Gerar Recomendações
```
Ordenar issues por severidade
Para cada issue aberta:
  Gerar ação recomendada
  Atribuir prioridade
```

### Passo 5: Atualizar Relatório
```
Salvar audit_report.json com:
  - Data da auditoria
  - Issues encontradas
  - Recomendações
  - Estatísticas
```

---

## 📈 Métricas de Saúde

### Índice de Saúde do Ecossistema
```
score = 100
score -= (critical_issues * 20)
score -= (high_issues * 10)
score -= (medium_issues * 5)
score -= (low_issues * 2)

>80 = 🟢 Saudável
60-80 = 🟡 Necessita Atenção
<60 = 🔴 Crítico
```

### Métricas Atuais (2026-02-09)
- Total de Skills: 37
- Issues Abertas: 4
- Issues Críticas: 0
- **Score: 80** 🟢

---

## 🔄 Ações Pendentes (Prioridade)

1. **[P2]** Clarificar fronteira `fx_architect` vs `feedback_architect` (RESOLVIDO via Evolution)
2. **[P3]** Atualizar triggers de `particle_forge` e `particle_3d_architect` (RESOLVIDO via Evolution)
3. **[P4]** Avaliar merge de skills procedurais

---

## 🗃️ Arquivo de Auditoria

O relatório completo está em:
`studio_library/_registry/audit_report.json`

Este arquivo contém:
- Regras de auditoria
- Issues atuais com status
- Análise de cobertura
- Ações recomendadas
- Estatísticas

---

## 🔗 Integração com Skill Forge

Ao criar nova skill via `skill_forge`:
1. Executar mini-auditoria de triggers
2. Verificar se não há overlap com existentes
3. Adicionar à coverage_analysis se nova área
