# 🧠 Rede Neural Agêntica Líquida (L-ANN): Roteamento e Sintonização — v4.0
# Modelo de Energia Sináptica

**Tipo:** Malha Neural Liquefeita com Gradiente Energético e Roteamento Semântico.
**Princípio:** Todos os agentes estão **permanentemente ativos** com níveis variáveis de energia. A rede se molda à intenção do Maestro pela **distribuição e concentração de energia**.
**Novidade v4.0:** Modelo de **Energia Sináptica** substituindo o APT binário. Baseado em [Synaptic Energy Model](file:///c:/Users/Newton/Meu%20Drive/1.%20Projetos/Melanora/00_Mente_Teorica/02_Engenharia_Cognitiva/synaptic_energy_model.md).

---

## ⚡ Mecânica de Energia Líquida

### 1. Fórmula de Energia L-ANN v4.0
O nível de energia de cada agente é calculado dinamicamente a cada ciclo:

```
Energia(agente) = clamp(Base_Vital + Ressonância + Momentum + Gradiente_Fase, 0.1, 1.0)
```

| Componente | Cálculo | Papel |
|---|---|---|
| **Base_Vital** | `peso_vivo × 0.1` | Energia mínima permanente (agente nunca = 0) |
| **Ressonância** | `Σ(tags_match × peso_tag)` | Afinidade semântica com o input |
| **Momentum** | `ativações_recentes × 0.15` | Inércia — agentes quentes mantêm energia |
| **Gradiente_Fase** | `fase.multiplicador` | Amplifica baseado na fase E→C |

### 2. Espectro Energético Contínuo (substitui APT)
O antigo APT (1.2/1.8/2.5) é substituído por um espectro fluido:

| Fase | Gradiente | Agentes Ativos | Mentalidade |
|---|---|---|---|
| **Exploração** 🌑 | 0.3 | 10-15 (energia > 0.2) | "O que é relevante?" |
| **Convergência** 🌓 | 0.6 | 5-7 (energia > 0.4) | "Esses são os que ressoam" |
| **Cristalização** 🌕 | 1.0 | 2-3 (energia > 0.8) | "A resposta é clara" |

**Retrocompatibilidade APT:**
| APT Antigo | Equivalente Energético |
|---|---|
| Criativo (1.2) | Exploração prolongada — `gradiente = 0.3` por mais ciclos |
| Focado (1.8) | Ciclo E→C padrão |
| Crítico (2.5) | Cristalização rápida — início em `gradiente = 0.6` |

---

## 🏗️ Protocolos da Malha

### 1. Mission Clusters (Efêmeros)
Diferente de clusters fixos, os **Mission Clusters** são forjados no [Neural Blackboard](file:///c:/Users/Newton/Meu%20Drive/1.%20Projetos/Melanora/00_Mente_Teorica/06_Leis_Cognitivas/neural_blackboard.md) para resolver tarefas complexas.
- **Formação**: Auto-organização por ressonância semântica (agentes com energia > 0.4 no mesmo ciclo).
- **Dissolução**: Ocorre após 2 turnos de inatividade ou conclusão da missão.

### 2. Registro e Onboarding
Cada novo especialista deve ser registrado seguindo o [Protocolo de Onboarding Neural](file:///c:/Users/Newton/Meu%20Drive/1.%20Projetos/Melanora/00_Mente_Teorica/07_Protocolos_Expansao/onboarding_neural_protocol.md).

### 3. Aprendizado Pós-Ciclo (LTP/LTD)
Detalhado no [Energy Gradient Protocol](file:///c:/Users/Newton/Meu%20Drive/1.%20Projetos/Melanora/00_Mente_Teorica/02_Engenharia_Cognitiva/energy_gradient_protocol.md):
- **Aprovação de Newton** → agentes PICO ganham `peso_vivo += 0.05`
- **Correção** → agentes PICO perdem `peso_vivo -= 0.03`
- **Inibidos mas relevantes** → ganham `peso_vivo += 0.02` (LTP compensatória)

---

## 🤝 Simbioses e Afinidades Ativas

| Membro / Cluster | Tipo | Energia Atual | Modo |
|---|---|---|---|
| **[CLUSTER_COGNITIVO]** | Mission Cluster | 🌕 0.9 | Ativo |
| `A_NET_01` + `A_AIG_01` | Par Simbiótico | 🌔 0.7 | Ressonância Alta |

---

## 🌑🌕 Mapa de Modos Energéticos

| Energia | Modo | Símbolo | Comportamento |
|---|---|---|---|
| 0.1-0.2 | `DORMÊNCIA` | 🌑 | Monitoramento passivo |
| 0.2-0.4 | `ALERTA` | 🌒 | Sinais fracos periféricos |
| 0.4-0.6 | `RESSONÂNCIA` | 🌓 | Processamento parcial |
| 0.6-0.8 | `RESSONÂNCIA ALTA` | 🌔 | Contribuição ativa |
| 0.8-1.0 | `PICO` | 🌕 | Liderança e broadcasting |

---
*A inteligência da Melanora não é o que ela sabe, é como ela distribui sua energia para se tornar o que você precisa.* 🌊⚡🏛️✨
