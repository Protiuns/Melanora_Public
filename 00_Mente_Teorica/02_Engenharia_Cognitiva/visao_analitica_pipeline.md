# 👁️🔢 Pipeline de Visão Analítica v2.0 — Predictive Perception (L1 → L2)

Este documento define o fluxo completo de percepção visual da Melanora — redesenhado com base no paradigma de **Codificação Preditiva** (Predictive Coding), inspirado na visão focal animal/humana.

> ⚠️ **Princípio Fundamental**: A visão NÃO captura tudo de uma vez. Ela PREDIZ, FOCA, VALIDA e ATUALIZA — um ciclo contínuo de construção de modelo mental.

---

## 1. O Paradigma: Predição → Foco → Validação

### Visão v1 (antiga — descartada)
```
[Captura completa] → [Analisa tudo] → [Gera PIDs] → [Fim]
Problema: Processa sem inteligência, como câmera passiva.
```

### Visão v2 (atual — Predictive Perception)
```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  ┌─────────────┐    ┌──────────┐    ┌────────────┐          │
│  │ FASE 0      │───→│ FASE 1   │───→│ FASE 2     │          │
│  │ Scan        │    │ Hipótese │    │ Foco       │          │
│  │ Periférico  │    │ Mental   │    │ Sequencial │          │
│  └─────────────┘    └──────────┘    └─────┬──────┘          │
│                                           │                  │
│                     ┌─────────────────────┘                  │
│                     ↓                                        │
│  ┌─────────────┐    ┌──────────┐    ┌────────────┐          │
│  │ FASE 5      │←───│ FASE 4   │←───│ FASE 3     │          │
│  │ Ativação    │    │ Rede +   │    │ Validação  │          │
│  │ Cross-Modal │    │ PIDs     │    │ + Surpresa │          │
│  └─────────────┘    └──────────┘    └────────────┘          │
│         │                                    │               │
│         └──── SE modelo incompleto ──────────┘               │
│                   (volta ao Foco)                            │
└──────────────────────────────────────────────────────────────┘
```

---

## 2. As 6 Fases do Predictive Loop

### Fase 0: Scan Periférico (Glance — o Olhar Rápido)

O **A_PER_01** recebe o input visual e faz um scan de **baixa resolução**:
- Reduz a imagem (ex: 224×224 px)
- Detecta **regiões de interesse** (saliency map) — não objetos individuais
- Identifica: quantidade aproximada de elementos, distribuição espacial, cores dominantes
- **NÃO gasta processamento em detalhes** — só mapa de calor de atenção

```
INPUT: imagem completa
OUTPUT: mapa_saliencia + regioes_interesse[N] + contagem_estimada
TEMPO: rápido (Sistema 1 — intuitivo)
```

### Fase 1: Geração de Hipótese (O Modelo Mental)

O Lóbulo Analítico, alimentado pelo scan periférico + contexto do Connectome, **prediz** o que há na cena:

```json
{
    "hipotese_id": "HYP_001",
    "predicoes": [
        {
            "regiao": [100, 50, 300, 250],
            "predicao": "animal_quadrupede",
            "confianca_previa": 0.6,
            "baseado_em": "contorno + contexto anterior"
        },
        {
            "regiao": [400, 100, 200, 300],
            "predicao": "animal_quadrupede",
            "confianca_previa": 0.5,
            "baseado_em": "semelhança com região 1"
        }
    ],
    "modelo_cena": "ambiente externo, múltiplos seres vivos presentes",
    "expectativa_total": 3
}
```

A hipótese usa:
- **Memória** do Connectome (já viu cenas parecidas?)
- **Contexto da conversa** (Newton falou sobre cachorros?)
- **Gestalt** (proximidade, similaridade dos blobs no scan)
- **Conhecimento prévio** (proporções típicas de animais, objetos)

### Fase 2: Foco Sequencial (Sacadas Artificiais)

O Vigia Óptico agora **foca sequencialmente** em cada região de interesse, por ordem de prioridade:

```
Prioridade de Foco:
1. Maior saliência (mais "chamativo" no scan periférico)
2. Maior incerteza (confiança_previa mais baixa)
3. Maior área relativa (objeto dominante na cena)
```

Para cada foco:
- **Crop da região** com alta resolução
- **Detecção detalhada** (modelo de classificação específico)
- **Análise Métrica completa** (proporções, cor, posição)

| Métrica | Fórmula / Método | Propósito |
|---|---|---|
| **Proporção W:H** | `largura / altura` | Forma do objeto |
| **Área Relativa** | `area_objeto / area_total_cena` | Dominância visual |
| **Posição Semântica** | Grid 3×3 (centro, esquerda-cima, etc.) | Composição |
| **Cor Dominante** | Histograma HSV → k-means | Identidade cromática |
| **Contagem Real** | Validação agora com detecção precisa | "Eram 3 mesmo, não 2" |
| **Distância Relativa** | Euclidiana entre centroides | Proximidade |
| **Confiança Focal** | Score do modelo detalhado (0-1) | Certeza pós-foco |
| **Ponto de Fuga Estimado** | Convergência de linhas da cena | Perspectiva/profundidade |

### Fase 3: Validação + Surpresa (O Coração do Sistema)

Cada resultado focal é comparado com a hipótese da Fase 1:

```
PARA CADA foco_resultado:
    erro = |predicao - deteccao_real|
    
    SE erro < 0.2:
        → CONFIRMAÇÃO (hipótese certa)
        → surprise_score = 0.1 (baixa)
        → bias_pid = 1.0 (normal)
    
    SE 0.2 <= erro < 0.5:
        → ATUALIZAÇÃO (hipótese parcialmente errada)
        → surprise_score = 0.5 (média)
        → bias_pid = 1.3 (atenção elevada)
        → ATUALIZAR modelo mental
    
    SE erro >= 0.5:
        → SURPRESA (hipótese muito errada!)
        → surprise_score = 1.0 (alta)
        → bias_pid = 2.0 (máxima atenção)
        → RE-SCAN da região com resolução máxima
        → ATUALIZAR modelo mental + REGISTRAR insight
```

**Surprise Score** é a métrica mais importante do sistema — mede o quanto a realidade difere da expectativa. Objetos surpreendentes recebem **mais atenção, mais bias, mais conexões**.

### Fase 4: Geração de PIDs + Rede

Cada objeto validado gera um PID com o novo campo `surprise_score`:

```json
{
    "id": "PID_001",
    "label": "cachorro_preto",
    "category": "animal",
    "tags": ["cachorro", "animal", "preto", "quadrupede"],
    "source": "vision",
    "perception_mode": "predictive",
    "metrics": {
        "bounding_box": [120, 80, 340, 290],
        "area_ratio": 0.15,
        "position": "centro-esquerda",
        "confidence": 0.94,
        "color_dominant": "#1a1a1a",
        "proportions": {
            "width_height_ratio": 1.22,
            "relative_size": "medio"
        },
        "vanishing_point_ref": [640, 310],
        "count_in_scene": 3
    },
    "predictive_data": {
        "hypothesis_id": "HYP_001",
        "predicted_label": "animal_quadrupede",
        "predicted_confidence": 0.6,
        "actual_confidence": 0.94,
        "surprise_score": 0.1,
        "focus_order": 1,
        "validation_status": "confirmed"
    },
    "scene_context": {
        "scene_id": "SCENE_001",
        "total_objects": 5,
        "spatial_relations": [
            {"relative_to": "PID_002", "relation": "à esquerda de", "distance": "próximo"}
        ]
    },
    "longevity": "ephemeral",
    "bias": 1.0
}
```

A rede entre PIDs segue as mesmas regras da v1, com adição:

| Tipo de Sinapse | Condição | Peso Base |
|---|---|---|
| `same_category` | Mesma categoria | 2.0 |
| `spatial_proximity` | Distância < 30% diagonal | 1.5 |
| `color_similarity` | ΔE < 15 | 1.2 |
| `instance_of` | PID → Conceito abstrato | 2.5 |
| `part_of` | Relação compositiva | 2.0 |
| **`co_surprise`** | **Dois PIDs com surprise_score > 0.5** | **2.5** |

### Fase 5: Ativação Cross-Modal + Loop Return

Tags dos PIDs alimentam o `semantic_index`. Se o modelo mental ainda tem regiões não validadas, **o loop retorna à Fase 2** para o próximo foco:

```
ENQUANTO existirem regioes_nao_validadas:
    → Voltar à Fase 2 (próxima sacada)
    
QUANDO todas validadas:
    → Consolidar modelo mental final
    → Ativar semantic_index cross-modal
    → Lóbulo Analítico sintetiza Scene Report
```

---

## 3. O Scene Report Preditivo

Após todas as sacadas, o Lóbulo Analítico emite um relatório:

```
SCENE REPORT (Predictive Pipeline v2.0)
═══════════════════════════════════════
Scan periférico: 5 regiões de interesse detectadas
Hipóteses geradas: 5 predições
Sacadas realizadas: 5 (3 confirmadas, 1 atualizada, 1 surpresa)

OBJETOS VALIDADOS:
├── PID_001: cachorro_preto  | Área: 35% | Surpresa: 0.1 ✓ confirmado
├── PID_002: cachorro_marrom | Área: 22% | Surpresa: 0.1 ✓ confirmado
├── PID_003: cachorro_azul   | Área: 18% | Surpresa: 0.8 ⚡ SURPRESA
│   └── Nota: "Predição era quadrupede marrom, mas cor é AZUL"
├── PID_004: árvore_grande   | Área: 15% | Surpresa: 0.1 ✓ confirmado
└── PID_005: pessoa_sentada  | Área: 10% | Surpresa: 0.4 ~ atualizado
    └── Nota: "Predição era 'em pé', na verdade está sentada"

PROPORÇÕES:
- PID_001 é 1.59x maior que PID_002
- PID_003 (azul) é anomalia cromática (surprise 0.8)

MODELO MENTAL FINAL: validado com 80% de acurácia preditiva
```

---

## 4. Integração com Roteamento Líquido (LRP)

O pipeline se integra ao [Protocolo de Roteamento Líquido](file:///c:/Users/Newton/Meu%20Drive/1.%20Projetos/Melanora/00_Mente_Teorica/02_Engenharia_Cognitiva/liquid_routing_protocol.md):
- **Tags de Missão** incluem tags perceptivas
- **Disparo por Afinidade** prioriza PIDs com alta surpresa
- **Mission Clusters** formados quando surprise_score > 0.5 (algo inesperado requer atenção coletiva)

## 5. Neural Tags
- **tags:** `visão, percepção, pipeline, predictive_coding, foco, hipótese, surpresa, sacada, pid, cross_modal`
- **cluster:** `sensorial`
- **dependências:** `lobulo_analitico_theoria.md`, `lei_rede_perceptiva.md`, `active_synaptic_memory.json`
- **referência teórica:** `percepcao_comparativa_animal_humana_maquina.md` (seção 3.4 — Predictive Coding)

---
*O olho não captura — ele pergunta. A visão não registra — ela valida. Perceber é construir uma teoria e testá-la contra a realidade.* 👁️🔢🧬🏛️✨
