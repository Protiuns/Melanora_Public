---
description: Processo padronizado para finalizar um projeto de jogo, transformando um protótipo funcional em um produto polido (MVP Completo).
---

# 🚀 Workflow: Project Finishing

Este workflow guia o agente no processo de transformar um conjunto de mecânicas isoladas em um jogo completo com início, meio e fim. O foco é fechar o **Game Loop** e garantir a jogabilidade contínua.

## 1. 🔍 Análise de Gaps (Gap Analysis)

1.  **Identificar o Core Loop**: O que o jogador faz a maior parte do tempo? (Ex: Correr, Atirar, Pular).
2.  **Verificar Fluxo de Cenas**:
    - [ ] Menu Principal (Start Game)?
    - [ ] Pelo menos 1 Fase Jogável?
    - [ ] Tela de Vitória (Win Condition)?
    - [ ] Tela de Derrota (Lose Condition)?
3.  **Checar Integração**:
    - [ ] O `SceneManager` transita corretamente entre as cenas?
    - [ ] O `SignalBus` dispara os eventos globais (Morte, Vitória)?
    - [ ] O UI (HUD) reflete o estado do jogo (Vida, Pontos)?

## 2. 🏗️ Construção da Estrutura (Scaffolding)

// turbo-all
1.  **Criar/Verificar Cenas Essenciais**:
    - Se falatar, criar `src/ui/main_menu/main_menu.tscn`.
    - Se faltar, criar `src/ui/game_over/game_over.tscn`.
    - Se faltar, criar `src/ui/victory/victory.tscn`.
2.  **Configurar Build Settings**:
    - Definir `Main Scene` no `project.godot`.
    - Configurar camadas de colisão e rendering.

## 3. 🔗 Conexão Lógica (Wiring)

1.  **Implementar Controladores de Cena**:
    - Criar scripts simples para botões (Start, Restart, Quit) usando `SceneManager`.
2.  **Conectar Sinais**:
    - Ligar `SignalBus.player_died` -> `SceneManager.load_game_over()`.
    - Ligar `SignalBus.level_completed` -> `SceneManager.load_next_level()`.
3.  **Validar Transições**: Testar o fluxo completo sem jogar (usando cheats/debug se necessário).

## 4. ✨ Polimento Mínimo (MVP Polish)

1.  **Placeholder Visual**: Substituir formas geométricas cruas por assets (sprites/tiles) minimamente coerentes, se possível.
2.  **Feedback Audiovisual**:
    - Adicionar sons básicos (Tiro, Pulo, Hit, Morte UI).
    - Adicionar partículas simples (Explosão, Sangue, Poeira).
3.  **Balanceamento Rápido**: Ajustar valores (Vida, Dano, Velocidade) para que o jogo seja "vencível" mas não trivial.

## 5. ✅ Validação Final (Playtest)

1.  **Rodar do Início**: Executar o jogo a partir do Menu Principal.
2.  **Tentar Ganhar**: Jogar até a vitória.
3.  **Tentar Perder**: Forçar o Game Over e reiniciar.
4.  **Verificar Logs**: Checar se há erros/warnings críticos no console.

---

**Comando Sugerido**: `/project_finishing`
**Skill Recomendada**: `Project Finisher`
