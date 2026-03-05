---
name: Platformer Level Design
description: Spatial architecture principles, challenge progression, and player guidance in 2D levels.
---

# Platformer Level Design

O level design é a resposta direta às habilidades do personagem. Se o personagem pula 3 blocos, o desafio deve ser construído em torno disso.

## Princípios de Espaçamento e Escala

1. **A Regra do Salto**: Se o pulo máximo é 4 unidades, use:
   - **3 unidades**: Confortável.
   - **3.5 unidades**: Desafiador (exige precisão).
   - **4 unidades**: Pulo de risco máximo.
2. **Respiro Visual**: Evite claustrofobia. Deixe espaço livre acima do jogador para que a câmera e o pulo não pareçam "presos".

## Guia Silencioso (Narrativa Visual)

Ensine sem textos:
- **Iluminação**: Coloque uma luz no final do corredor para atrair o jogador.
- **Moedas/Itens**: Use trilhas de moedas para indicar a parábola correta de um pulo cego.
- **Formas**: Triângulos ou objetos inclinados apontando para onde o jogador deve ir.

## Evolução de Desafios (Skill Loop)

| Fase | Descrição | Exemplo |
| :--- | :--- | :--- |
| **Introdução** | Ambiente seguro para testar a mecânica. | Plataforma simples com chão sólido abaixo. |
| **Desenvolvimento** | Adiciona risco (ex: buraco). | Pular sobre um buraco pequeno. |
| **Variação** | Muda as condições (ex: plataforma móvel). | Pular em uma plataforma que sobe e desce. |
| **Conclusão (Teste)** | Combina com outras mecânicas. | Pular plataforma móvel enquanto atira. |

## Dicas de Fluxo
- **Checkpoints**: Coloque checkpoints logo após desafios intensos ou antes de chefes.
- **Pacing**: Alterne momentos de alta tensão (ação) com momentos de descanso (exploração/segurança).
- **Leitura**: O jogador deve entender o que é perigoso em menos de 1 segundo. Cor vermelha ou espinhos são padrões universais.
