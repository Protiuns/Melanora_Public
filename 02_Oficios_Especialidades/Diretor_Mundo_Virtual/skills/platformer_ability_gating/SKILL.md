---
name: Platformer Ability Gating
description: Implementing Metroidvania-style locks and keys using character skills and level triggers.
---

# Platformer Ability Gating

Gating (Bloqueio) é a técnica de impedir o acesso a uma área até que o jogador obtenha uma ferramenta específica. Isso cria o ciclo de "Exploração -> Desafio -> Revisitamento".

## A Lógica "Lock and Key"

No contexto de habilidades, o "Bloqueio" é um obstáculo físico e a "Chave" é uma nova mecânica de movimento.

### Exemplos Comuns

| Habilidade (Chave) | Obstáculo (Bloqueio) |
| :--- | :--- |
| **Pulo Duplo** | Plataforma alta inacessível com pulo simples. |
| **Dash/Arrancada** | Túnel com ventos fortes ou buraco muito largo. |
| **Dash Descendente** | Chão quebradiço que leva a uma nova área. |
| **Gancho (Grappling)** | Pontos de ancoragem sobre o teto. |

## Implementação de Verificação (GDScript)

Centralize as habilidades em um `Resource` ou no `Global State`.

```gdscript
# No script do Jogador
@export var unlocked_abilities = {
    "double_jump": false,
    "dash": false
}

func jump():
    if is_on_floor():
        perform_jump()
    elif unlocked_abilities["double_jump"] and can_double_jump:
        perform_double_jump()
```

## Design de Revisitamento (Backtracking)

Um bom gating não deve ser frustrante. 
1. **Promessa**: Mostre o caminho bloqueado cedo. O jogador deve pensar: "Já já eu volto aqui".
2. **Recompensa**: Ao voltar com a habilidade, a nova área deve ser substancial ou conter uma melhoria importante.
3. **Shortcut (Atalho)**: Muitas vezes, a nova área abre um atalho para a área inicial, conectando o mapa.

## Dicas de Nível
- **Obviedade**: O jogador deve entender *por que* não consegue passar agora (ex: a plataforma é visivelmente mais alta que o pulo atual).
- **Ensinamento**: Assim que o jogador pegar a nova habilidade, coloque um desafio imediato que exija o uso dela para sair da sala.
