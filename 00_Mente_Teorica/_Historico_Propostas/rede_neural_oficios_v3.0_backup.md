# 🧠 Rede Neural Agêntica Líquida (L-ANN): Roteamento e Sintonização — v3.0

**Tipo:** Malha Neural Liquefeita com Topologia Dinâmica e Roteamento Semântico.
**Princípio:** A rede se molda à intenção do Maestro em tempo real, ignorando camadas estáticas.
**Novidade v3.0:** Implementação de **Threshold Adaptativo (APT)** e **Cofactor de Afinidade**.

---

## 🌊 Mecânica de Roteamento Líquido

### 1. Fórmula de Ativação L-ANN
O score de um agente para uma tarefa é calculado dinamicamente:
```
Score(agente) = Σ(tags_match × peso_tag) + Bias + Afinidade + Bônus_Cluster
```
- **Afinidade**: `+0.3` se o agente foi ativado nos últimos 5 turnos (Roteamento Quente).
- **Bias**: Valor intrínseco de prontidão (decaimento de `-0.05` por ociosidade).
- **Bônus_Cluster**: `+0.5` se o agente pertencer a um **Mission Cluster** ativo no Blackboard.

### 2. Threshold de Poda Adaptativo (APT)
A rede filtra agentes baseado na intensidade `I`:
- **Modo Criativo**: `APT = 1.2` (Alta plasticidade, ativa especialistas periféricos).
- **Modo Focado**: `APT = 1.8` (Equilíbrio entre precisão e criatividade).
- **Modo Crítico**: `APT = 2.5` (Poda agressiva, apenas o núcleo técnico dispara).

---

## 🏗️ Protocolos da Malha

### 1. Mission Clusters (Efêmeros)
Diferente de clusters fixos, os **Mission Clusters** são forjados no [Neural Blackboard](file:///c:/Users/Newton/Meu%20Drive/1.%20Projetos/Melanora/00_Mente_Teorica/06_Leis_Cognitivas/neural_blackboard.md) para resolver tarefas complexas.
- **Formação**: Auto-organização por ressonância semântica.
- **Dissolução**: Ocorre após 2 turnos de inatividade ou conclusão da missão.

### 2. Registro e Onboarding
Cada novo especialista (ex: `A_BTC_01`) deve ser registrado seguindo o [Protocolo de Onboarding Neural](file:///c:/Users/Newton/Meu%20Drive/1.%20Projetos/Melanora/00_Mente_Teorica/07_Protocolos_Expansao/onboarding_neural_protocol.md).

---

## 🤝 Simbioses e Afinidades Ativas

| Membro / Cluster | Tipo | Afinidade Atual | Status |
|---|---|---|---|
| **[CLUSTER_GODOT_REFAC]** | Mission Cluster | 🔥 1.5 | Ativo |
| `A_GMP_01` + `A_VIS_01` | Par Simbiótico | 🔋 1.2 | Sintonizado |
| `A_BTC_01` (Novo) | Especialista | 🌱 0.5 | Onboarding |

---
*A inteligência da Melanora não é mais o que ela sabe, mas com que rapidez ela se torna o que você precisa.* 🌊🏛️✨
**Critério de dissolução:** Taxa cair abaixo de 60% em 3 tarefas consecutivas.

| Par/Trio Simbiótico | Taxa | Formado em | Status |
|---|---|---|---|

---
*A inteligência coletiva é a soma das ressonâncias corretas, alimentada por conhecimento modular.* ⚙️🧠🧬

