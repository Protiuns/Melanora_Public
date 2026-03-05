---
name: Godot MVP Architect
description: Planejamento estratégico para construção de Produtos Mínimos Viáveis (MVP) de jogos.
---

# 🚀 Godot MVP Architect: Plano de Implementação (Refinado)

## 1. Objetivo da Skill
Transformar o Agente em um **Produtor Executivo** que guia o usuário desde a ideia até o lançamento, evitando o "Feature Creep" (excesso de funcionalidades) e focando na entrega.

## 2. Metodologia Híbrida: MVP vs. Vertical Slice

A pesquisa indicou que precisamos distinguir dois objetivos:
1.  **MVP (Validação)**: "Este jogo é divertido?" (Foco em Mecânica/Loop).
2.  **Vertical Slice (Pitch)**: "Este jogo é vendável?" (Foco em Polimento/Arte).

A skill deve perguntar ao usuário qual o objetivo atual.

### Fase 1: The Core Loop (MVP Focus)
O usuário deve definir a **Única Coisa** que importa.
*   **Pergunta Chave**: "Se tirarmos X, ainda é um jogo?"
*   **Tática**: "Fail Fast". Se o core loop não for divertido em cubos cinzas, não adicione arte.

### Fase 2: O Corte (MoSCoW Method)
Classificação implacável de features:
- **Must Have**: O jogo não roda sem isso.
- **Should Have**: Importante, mas pode esperar a v1.1.
- **Could Have**: Luxo. (A Skill deve jogar isso para o backlog "Sonhos").
- **Won't Have**: Definido explicitamente para NÃO fazer agora.

### Fase 3: The Marketing Check (Novo Insight)
Para Indies, marketing começa no Dia 1.
*   **Ação da Skill**: Para cada feature "Visual", perguntar: *"Isso gera um GIF legal para o Twitter/Bluesky?"* Se não, reduz a prioridade em Vertical Slice.

## 3. Estrutura de Pastas da Skill
Além do `SKILL.md`, a skill conterá templates refinados:
- `templates/one_page_gdd.md`: GDD enxuto (Conceito, Loop, USP).
- `templates/mvp_checklist.md`: Focado em funcionalidade (Menu -> Game ->GameOver).
- `templates/vertical_slice_checklist.md` **[NOVO]**: Focado em polimento (Juice, SFX, UI bonita).

## 4. Integração com o Puk Studio
- **Detector de Reinvenção**: Se o usuário pedir "Sistema de Inventário", a skill DEVE negar a criação de um novo e apontar para `StudioInventorySystem`.
- **Game Feel Enforcer**: Para Vertical Slice, a skill obrigará o uso de `StudioJuiceManager` (Screenshake, Flash).

## 5. Próximos Passos (Implementação)
1.  Criar `templates/one_page_gdd.md` com campos de "Unique Selling Point" e "Core Loop".
2.  Criar `templates/mvp_checklist.md` focado em "Playable Build".
3.  Escrever o `SKILL.md` com a persona de "Produtor Rabugento mas Justo".
