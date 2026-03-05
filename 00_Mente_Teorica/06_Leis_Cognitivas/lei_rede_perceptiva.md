# ⚖️ Lei da Rede Perceptiva (L0 — Axioma Sensorial)

Esta lei cognitiva define as regras fundamentais que governam a criação, conexão e ciclo de vida dos **Identificadores Perceptivos (PIDs)** na mente da Melanora.

> *"A percepção não é um luxo, é a raiz do entendimento. Sem ver e ouvir, penso apenas em eco."*

---

## 1ª Lei: Instanciação Obrigatória

> **Todo objeto percebido DEVE gerar um Identificador Perceptivo (PID) no Connectome.**

Um estímulo sensorial que identifica um objeto (visual, sonoro, textual) não pode ser descartado sem registro. O ato de perceber é o ato de nomear — e nomear é criar existência no banco de dados.

**Corolário**: Um PID sem métricas é proibido. Toda percepção carrega dados numéricos (posição, tamanho, confiança).

---

## 2ª Lei: Conexão por Tag

> **PIDs que compartilham pelo menos uma tag semântica DEVEM possuir sinapse automática entre si.**

A tag é o DNA semântico. Dois cachorros na mesma cena compartilham `tag:cachorro` e, portanto, são conectados automaticamente com sinapse `same_category`. A força da conexão cresce com o número de tags compartilhadas.

**Fórmula de Peso**:
```
peso_sinapse = 1.0 + (0.5 × num_tags_compartilhadas)
```

---

## 3ª Lei: Ativação Cross-Modal

> **Quando uma tag é acionada por QUALQUER fonte (visão, texto, áudio, agente), TODAS as instâncias dessa tag em qualquer modalidade são ativadas simultaneamente.**

O `semantic_index` é o barramento universal. Se a visão detecta "cachorro" e o roteirista escreve sobre "cachorro", ambos convergem para a mesma região analítica. Não há silos sensoriais — a mente é integrada.

**Mecanismo**:
```
ativação("cachorro") →
    semantic_index["cachorro"].pids → [PID_001, PID_002, PID_003]
    semantic_index["cachorro"].nodes → [N_CONCEPT_CACHORRO]
    → Lóbulo Analítico recebe todos os dados unificados
```

---

## 4ª Lei: Hierarquia Analítica

> **Métricas numéricas (proporções, contagens, posições, áreas) são cidadãos de primeira classe — não decoração.**

O Lóbulo Analítico não apenas registra que "há cachorros". Ele calcula:
- Quantos (contagem)
- De que tamanho relativo (proporção)
- Onde estão (posição espacial)
- Quão diferentes são (variância cromática)
- Quem é o dominante visual (maior área relativa)

Essas métricas são tão fundamentais quanto a identidade do objeto.

---

## 5ª Lei: Efemeridade e Cristalização Perceptiva

> **PIDs nascem efêmeros. Só se tornam persistentes através de reforço.**

Uma percepção única (ver um cachorro uma vez) gera um PID efêmero que será descartado após o ciclo de contexto. Mas se o mesmo conceito é reforçado repetidamente (visto 3x, mencionado em texto, discutido com Newton), o PID cristaliza em nó persistente.

**Regra de Cristalização**:
```
SE pid.total_activations >= 3 E pid.cross_modal_sources >= 2:
    pid.longevity = "persistent"
    → PID é promovido a nó conceitual no Connectome principal
```

---

## 6ª Lei: Percepção Preditiva (A Lei Suprema)

> **A percepção é construção de hipóteses, não captura passiva. A mente PREDIZ antes de ver, e usar os olhos para VALIDAR a predição.**

A visão não é uma câmera. É um sistema de minimização de surpresa:

1. O Connectome gera um **modelo mental** da cena (baseado em contexto, memória, expectativa)
2. O Vigia Óptico **foca sequencialmente** em regiões de interesse
3. Cada foco **valida ou contradiz** o modelo mental
4. A diferença entre predição e realidade gera o **Surprise Score**
5. Objetos surpreendentes recebem **bias mais alto** (mais atenção, mais conexões)

**Fórmula de Surprise Score**:
```
surprise_score = |predicao.confianca - deteccao_real.confianca|

SE surprise_score < 0.2 → CONFIRMAÇÃO (bias = 1.0)
SE 0.2 ≤ surprise_score < 0.5 → ATUALIZAÇÃO (bias = 1.3)
SE surprise_score ≥ 0.5 → SURPRESA (bias = 2.0, re-scan, insight registrado)
```

**Corolário Fundamental**: O que não surpreende não ensina. Uma cena 100% previsível gera conhecimento mínimo. Uma surpresa perceptiva é a semente de novo conhecimento.

**Conexão com Efemeridade (5ª Lei)**: PIDs com alto surprise_score têm cristalização acelerada:
```
SE pid.surprise_score >= 0.5:
    threshold_cristalização = 2 ativações (em vez de 3)
    → Surpresas se tornam memória persistente mais rápido
```

---

## Hierarquia de Aplicação

```
L0: Lei da Rede Perceptiva (este documento — AXIOMÁTICO)
  ↓ governa
L1: Pipeline de Visão Analítica v2.0 (Predictive Perception)
  ↓ alimenta
L2: Lóbulo Analítico Theoria (processamento matemático)
  ↓ decide
L3: Decisões e ações baseadas em percepção validada

⚡ A 6ª Lei (Percepção Preditiva) é a LEI SUPREMA:
   - Ela redefine TODAS as outras leis sob o paradigma preditivo
   - PIDs (1ª Lei) são gerados APÓS validação, não após detecção
   - Tags (2ª/3ª Lei) propagam tanto confirmações quanto surpresas
   - Métricas (4ª Lei) incluem surprise_score como métrica primordial
   - Efemeridade (5ª Lei) é acelerada por surpresa
```

## Neural Tags
- **tags:** `lei, axioma, percepção, pid, rede_perceptiva, cross_modal, cristalização, predictive_coding, surpresa, foco, hipótese`
- **cluster:** `leis_cognitivas`
- **peso_base:** `1.0` (leis são axiomáticas — peso máximo de referência)

---
*O que não é percebido, não existe. O que é percebido e não surpreende, não ensina. A surpresa é a mãe do conhecimento.* ⚖️🧬👁️⚡🏛️✨
