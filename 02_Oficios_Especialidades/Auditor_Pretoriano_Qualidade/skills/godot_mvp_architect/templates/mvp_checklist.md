# ✅ Checklist MVP (Playable Build)

O objetivo desta checklist é ter um jogo COMPLETO que roda e fecha (Win/Lose). A Arte é secundária.

## ⚪ Fase 1: Greybox & Core Loop
*Fase de Blocos Cinzas. Foco total em "Feels Good to Play".*

- [ ] Criar Cena `Game.tscn` com blocos básicos (Chão, Paredes).
- [ ] Implementar Personagem (Player) com Movimento Básico.
    - *Recomendação*: Use `StudioPlatformerDriver2D` ou `StudioTopDownDriver2D`.
- [ ] Implementar a única mecânica principal (Pular, Atirar, Construir).
- [ ] Criar o Inimigo/Obstáculo Básico (cubo vermelho).
- [ ] Implementar Colisão e Feedback de Hit (Partículas simples).
    - *Recomendação*: Use `StudioJuiceManager`.

## 🟢 Fase 2: Game Flow (Início, Meio, Fim)
*O jogo precisa ter um "Ciclo de Vida".*

- [ ] Criar Cena `MainMenu.tscn` com botão "Jogar" e "Sair".
- [ ] Implementar Condição de Vitória (Chegar no fim, Matar Boss).
    - *Ação*: Mostrar tela "You Win" -> Botão "Reiniciar".
- [ ] Implementar Condição de Derrota (Vida = 0).
    - *Ação*: Mostrar tela "Game Over" -> Botão "Tentar Novamente".
- [ ] Implementar Sistema de Pausa (ESC = Pausa).

## 🔵 Fase 3: Feedback Loop (UI & Som)
*O jogador precisa entender o que está acontecendo.*

- [ ] Adicionar HUD Básico (Vida, Pontos, Munição).
- [ ] Adicionar SFX para:
    - [ ] Pulo / Movimento
    - [ ] Dano (Player e Inimigo)
    - [ ] Coleta de Itens
    - [ ] Vitória / Derrota
- [ ] Adicionar Música de Fundo (Loop simples).

## 🔴 Fase 4: Playtest (Teste de Fogo)
*Envie para 3 pessoas (Amigos, Discord).*

- [ ] O jogo roda em outro PC? (Exportar .exe/.pck).
- [ ] Os controles são intuitivos? (Sem explicar nada).
- [ ] O jogo é divertido por pelo menos 5 minutos?

### ⚠️ Próximo Passo: Vertical Slice
Se passou no Playtest, prossiga para `vertical_slice_checklist.md`.
Se não, volte para a Fase 1 e refine o Core Loop.
