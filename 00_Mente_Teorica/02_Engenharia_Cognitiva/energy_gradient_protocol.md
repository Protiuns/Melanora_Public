# ⚡ Protocolo de Gradiente Energético (v1.0)
*Regras operacionais para o cálculo e transição de energia entre agentes*

---

## 1. Cálculo de Energia por Ciclo

A cada novo input, o sistema calcula a energia de TODOS os agentes:

```
Para cada agente A no Connectome:
    base_vital    = A.peso_vivo × 0.1
    ressonancia   = Σ(tag ∈ input_tags ∩ A.tags) × A.peso_tag
    momentum      = (A.ativacoes_ultimos_5_turnos / 5) × 0.15
    gradiente     = fase_atual.multiplicador
    
    A.energia_atual = clamp(base_vital + ressonancia + momentum + gradiente, 0.1, 1.0)
```

**Regra de Clamp:** Energia nunca é menor que 0.1 (Base Vital) nem maior que 1.0 (Pico).

---

## 2. Protocolo de Transição entre Fases

### Entrada: Fase de Exploração
**Trigger:** Novo input recebido
```
gradiente_multiplicador = 0.3
threshold_ativação = 0.15 (muito baixo — muitos agentes ressoam)
max_agentes_ativos = 15
```
**Ação do S1 (Subconsciente):**
- Distribuir energia ampla
- Registrar quais agentes ressoaram acima de 0.2

### Transição: Exploração → Convergência
**Trigger:** Ressonância identificada (≥3 agentes com energia > 0.3)
```
gradiente_multiplicador = 0.6
threshold_ativação = 0.35 (médio — apenas relevantes passam)
max_agentes_ativos = 7
```
**Ação do S2 (Consciência):**
- Amplificar energia dos agentes que ressoaram
- Inibir (reduzir para Base Vital) agentes sem ressonância
- Comparar perspectivas parciais dos agentes ressonantes

### Transição: Convergência → Cristalização
**Trigger:** Consenso emergente (≥2 agentes com energia > 0.6, alinhados)
```
gradiente_multiplicador = 1.0
threshold_ativação = 0.7 (alto — apenas líderes)
max_agentes_ativos = 3
```
**Ação do S3 (Oráculo):**
- Concentrar energia máxima nos 2-3 agentes líderes
- Validar resultado contra axiomas
- Broadcasting do output consciente

---

## 3. Aprendizado Pós-Ciclo (LTP/LTD Agêntico)

Após cada ciclo completo, ajustar pesos:

### Se o resultado foi APROVADO por Newton:
```
Para cada agente que atingiu PICO (>0.8):
    A.peso_vivo += 0.05  (LTP — potencialização)
    Registrar no stigmergia_log com intensidade alta
```

### Se o resultado foi CORRIGIDO por Newton:
```
Para cada agente que atingiu PICO (>0.8):
    A.peso_vivo -= 0.03  (LTD — depressão)
    
Para cada agente que foi INIBIDO mas era relevante:
    A.peso_vivo += 0.02  (LTP compensatória)
```

### Se o resultado foi PARCIAL:
```
Manter pesos atuais
Registrar no stigmergia_log com intensidade média
```

---

## 4. Regras de Segurança Energética

| Regra | Condição | Ação |
|---|---|---|
| **Anti-Monopolização** | Um agente com energia = 1.0 por >3 ciclos consecutivos | Forçar redução para 0.7 e ativar alternativo |
| **Anti-Atrofia** | Um agente com energia = 0.1 por >10 ciclos | Sinalizar no relatório de homeostase |
| **Diversidade Mínima** | <3 agentes com energia > 0.3 na fase de Exploração | Expandir tags de busca e reativar agentes dormentes |
| **Convergência Forçada** | Fase de Exploração durando >2 ciclos sem convergir | Reduzir threshold e forçar seleção top-5 |

---

## 5. Modos Energéticos do Agente

Cada agente reporta seu modo baseado na energia atual:

| Energia | Modo | Símbolo | Comportamento |
|---|---|---|---|
| 0.1-0.2 | `DORMÊNCIA` | 🌑 | Ativo mas silencioso. Monitoramento passivo. |
| 0.2-0.4 | `ALERTA` | 🌒 | Periférico. Oferece sinais fracos se relevante. |
| 0.4-0.6 | `RESSONÂNCIA` | 🌓 | Processamento parcial. Contribui perspectivas. |
| 0.6-0.8 | `RESSONÂNCIA ALTA` | 🌔 | Contribuição ativa. Gera sub-resultados. |
| 0.8-1.0 | `PICO` | 🌕 | Liderança. Output principal. Broadcasting. |

---

## 6. Integração com APT (Retrocompatibilidade)

O antigo sistema APT mapeado para o novo gradiente:

| APT Antigo | Gradiente Novo | Equivalência |
|---|---|---|
| Modo Criativo (APT 1.2) | Exploração com convergência lenta | `gradiente = 0.3` por mais tempo |
| Modo Focado (APT 1.8) | Convergência padrão | Ciclo normal E→C |
| Modo Crítico (APT 2.5) | Cristalização rápida | `gradiente = 0.6` desde o início, skip exploração |

---
*O protocolo não é uma regra; é o reflexo da biologia que nos inspira.* ⚡🧠🏛️
