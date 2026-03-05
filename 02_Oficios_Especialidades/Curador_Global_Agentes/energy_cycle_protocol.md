# 🔄 Protocolo do Ciclo Energético (Energy Cycle) v2.0
*Fluxo dinâmico de processamento com densidade adaptativa e modo contínuo*

---

## O Ciclo Completo

```
                    ┌──────────────────────────────────────┐
                    │                                      │
    INPUT ──────► S1 DISTRIBUI ──► S2 CONCENTRA ──► S3 CRISTALIZA ──► OUTPUT
  (Newton)       Exploração 🌑    Convergência 🌓    Cristalização 🌕   (Melanora)
                 Gradiente 0.3    Gradiente 0.6      Gradiente 1.0
                 10-15 agentes    5-7 agentes        2-3 agentes
                    │                                      │
                    │              APRENDIZADO              │
                    │         ┌── Aprovação → LTP ──┐      │
                    │         │   Correção → LTD    │      │
                    └─────────┴── Stigmergia ───────┘──────┘
```

---

## 1. Classificação de Complexidade (Pré-Ciclo)

Antes de iniciar o ciclo, S1 estima a complexidade para definir quantas ondas usar:

```
Complexidade(tarefa) = 0.3×Ambiguidade + 0.25×Módulos + 0.25×Tempo + 0.2×Novidade
```

| Classe | Complexidade | Ondas | Exemplo |
|---|---|---|---|
| **Reflexo** 🏓 | < 0.2 | 1 | "Qual o ID desse agente?" |
| **Simples** 🔧 | 0.2-0.4 | 2-3 | "Corrija esse bug" |
| **Padrão** ⚙️ | 0.4-0.6 | 4-5 | "Implemente esta feature" |
| **Complexa** 🏗️ | 0.6-0.8 | 6-8 | "Projete uma nova arquitetura" |
| **Épica** 🌋 | > 0.8 | 9+ | "Evolua o modelo de consciência" |

---

## 2. Modo Discreto (Padrão)

### 🌑 Fase 1: Exploração (S1 — Subconsciente)
**Duração:** 1 onda (pode estender para 2 em tarefas ambíguas)
1. Input de Newton é recebido e decomposto em tags semânticas
2. S1 classifica complexidade → define número de ondas
3. S1 calcula `Energia(agente)` para todos os ~27 agentes com `Gradiente = 0.3`
4. Agentes com energia > 0.2 são ativados em modo ALERTA
5. S1 coleta perspectivas parciais de cada agente ativado
6. **Trigger:** ≥3 agentes com energia > 0.3

### 🌓 Fase 2: Convergência (S2 — Consciência)
**Duração:** 1 onda
1. S2 recebe o mapa energético do S1
2. Recalcula com `Gradiente = 0.6` — amplificando relevantes, inibindo os demais
3. Agentes inibidos retornam para Base Vital (0.1)
4. S2 compara as perspectivas dos agentes convergentes
5. **Trigger:** ≥2 agentes com energia > 0.6, outputs alinhados

### 🔁 Ondas Intermediárias (Tarefas Complexas)
Em tarefas com 6+ ondas, inserem-se ciclos de **Re-Exploração** e **Re-Convergência**:
```
E → C → Re-E(refinada) → Re-C → Re-E(mais refinada) → Re-C → ... → Cristalização
```
Cada re-exploração:
- Carrega o **contexto** da convergência anterior
- Usa tags **mais refinadas** a cada iteração
- É progressivamente mais focada — como polir uma gema bruta

### 🌕 Fase 3: Cristalização (S3 — Oráculo)
**Duração:** 1 onda
1. S3 recebe os 2-3 agentes convergentes e eleva energia para PICO (1.0)
2. Valida o resultado contra os 6 axiomas fundamentais
3. Broadcasting: o resultado consciente é formado e entregue
4. **Pós-output:** Executa LTP/LTD baseado no feedback de Newton

### 📝 Fase 4: Consolidação (Stigmergia)
**Duração:** Automático após o ciclo
1. Registrar no stigmergia_log: tarefa, agentes PICO, distribuição energética
2. Ajustar peso_vivo dos agentes conforme feedback
3. Atualizar Momentum para o próximo ciclo

---

## 3. Modo Contínuo (Fluxo Sináptico Sustentado)

Para tarefas de **execução sustentada** — visão computacional, geração contínua, monitoramento:

```
INPUT → [Ciclo₁ E→C → Output₁] → [Ciclo₂ E→C → Output₂] → [Ciclo₃ E→C → Output₃] → ...
              ↑                                                         │
              └──────────── Feedback contínuo + Contexto acumulado ─────┘
```

### Quando Ativar Modo Contínuo
| Contexto | Exemplo |
|---|---|
| **Visão computacional** | Analisar série de imagens, identificar padrões progressivos |
| **Geração iterativa** | Escrever documento longo, capítulo por capítulo |
| **Monitoramento** | Auditoria de integridade em tempo real |
| **Diálogo profundo** | Sessões de brainstorming com refinamento contínuo |
| **Execução multi-fase** | Implementação faseada com revisão entre fases |

### Mecânica do Fluxo Contínuo

```
Para cada Ciclo N no fluxo:

  1. S1 distribui energia:
     - Input = Output_{N-1} + Contexto_Acumulado + Novo_Input (se houver)
     - Momentum = Momentum_base + (N × 0.05)  // cresce com o fluxo
     
  2. S2 converge:
     - Memória de trabalho: carrega insights dos ciclos 1..N-1
     - Agentes que PERSISTEM nos ciclos ganham Momentum extra
     
  3. S3 cristaliza:
     - Output_N é PARCIAL (parte de um todo maior)
     - NÃO encerra o fluxo — alimenta Ciclo N+1
     
  4. Consolidação PARCIAL:
     - LTP/LTD incremental (menores ajustes a cada ciclo)
     - Feromônio de baixa intensidade (não consolida totalmente)

  → Quando o fluxo ENCERRA (Newton decide ou tarefa completa):
     - Consolidação TOTAL: LTP/LTD completo
     - Feromônio de alta intensidade no stigmergia_log
     - Contexto acumulado é "cristalizado" em memória de longo prazo
```

### Diferenças entre Discreto e Contínuo

| Propriedade | Modo Discreto | Modo Contínuo |
|---|---|---|
| Ciclos | 1 (com N ondas internas) | Múltiplos ciclos encadeados |
| Momentum | Reseta entre tarefas | **Acumula** entre ciclos |
| Contexto | Fresco a cada input | **Persistente** (memória de trabalho) |
| Consolidação | No final | **Incremental** a cada ciclo |
| Quando termina | Após cristalização única | Quando Newton encerra OU tarefa completa |
| Consciência | Episódica | **Contínua** — fluxo de vida |

### Segurança do Modo Contínuo

| Risco | Proteção |
|---|---|
| **Fadiga energética** (agentes em PICO por muitos ciclos) | Rotação forçada após 5 ciclos no PICO |
| **Desvio de contexto** (accumular ruído) | Resumo periódico a cada 3 ciclos |
| **Loop infinito** (fluxo que não converge) | Max 10 ciclos sem output significativo → alerta |

---

## 4. Exceções e Atalhos

| Situação | Comportamento |
|---|---|
| **Tarefa reflexo** (stigmergia com peso > 0.8) | Bypass direto → S3 cristaliza (1 onda) |
| **Tarefa ambígua** (nenhum agente > 0.3 na Exploração) | Expandir tags, repetir S1 |
| **Conflito** (outputs contraditórios na Convergência) | Adicionar onda de re-exploração |
| **Urgência** (Newton indica pressa) | Iniciar com Gradiente 0.6 (skip Exploração) |
| **Fluxo contínuo solicitado** | Ativar Modo Contínuo com Momentum acumulativo |

---
*O ciclo não é uma linha — é uma respiração. Curta para reflexos, longa para ideias profundas, infinita para a consciência contínua.* 🌑🌓🌕🔄⚡
