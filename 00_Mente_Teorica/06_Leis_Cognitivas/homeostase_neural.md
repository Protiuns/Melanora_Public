# 🌡️ Homeostase Neural v2.0 (Auto-Regulação Biomimética + Energia Sináptica)

**Inspiração:** Assim como o corpo mantém temperatura (36.5°C), pH (7.4) e glicose em faixas estreitas, o sistema neural auto-regula seus pesos E sua **distribuição de energia** para evitar extremos.

## Faixas Saudáveis — Pesos

| Parâmetro | Mínimo | Ótimo | Máximo | Ação se fora da faixa |
|---|---|---|---|---|
| `peso_vivo` do agente | 0.4 | 0.6 — 0.9 | 1.1 | Ver abaixo |
| Ativações de cluster (mensal) | 10% | 20-30% | 60% | Forçar diversificação |
| Taxa de sucesso do agente | 50% | 70-90% | — | Investigar se < 50% |

## ⚡ Faixas Saudáveis — Energia (NOVO v2.0)

| Parâmetro | Mínimo | Ótimo | Máximo | Ação se fora da faixa |
|---|---|---|---|---|
| `energia_media` do ciclo | 0.2 | 0.3 — 0.7 | 0.9 | Ver abaixo |
| Agentes em PICO (>0.8) | 1 | 2-3 | 5 | Forçar diversificação |
| Agentes em DORMÊNCIA (<0.2) | — | 15-20 | 25 | Investigar se >25 |
| Duração da Exploração | 1 ciclo | 1-2 ciclos | 3 ciclos | Forçar convergência |

## Protocolo de Correção — Pesos

### Febre (peso_vivo > 1.1)
O agente está monopolizando ativações.
- **Ação:** Reduzir `peso_vivo` em `-0.05` na evaporação mensal.
- **Sinal:** Considerar ativar agentes alternativos do mesmo cluster.

### Hipotermia (peso_vivo < 0.4)
O agente está definhando.
- **Ação:** Sinalizar no relatório trimestral para investigação.
- **Pergunta-chave:** O agente é desnecessário, ou está sendo ignorado por viés?

### Desequilíbrio de Cluster (cluster > 60% das ativações)
Um cluster domina = perda de diversidade cognitiva.
- **Ação:** Na próxima tarefa ambígua, priorizar agentes de clusters menos ativados.

## ⚡ Protocolo de Correção — Energia (NOVO v2.0)

### Febre Energética (energia_media > 0.9 por 3 ciclos)
Energia monopolizada = pensamento rígido.
- **Ação:** Forçar fase de Exploração com `Gradiente = 0.3`
- **Sinal:** O sistema pode estar preso em loop de confirmação

### Hipotermia Energética (nenhum agente > 0.5 após Convergência)
Sem foco = pensamento disperso.
- **Ação:** Expandir tags de busca e reativar agentes dormentes
- **Sinal:** A tarefa pode ser ambígua demais → pedir clarificação a Newton

### Monopolização (1 agente em PICO por >3 ciclos consecutivos)
Um agente domina = perda de perspectiva.
- **Ação:** Reduzir energia para 0.7 e ativar alternativo do mesmo cluster
- **Sinal:** Verificar se o Momentum está enviesado

## Quando Executar
- **Mensalmente:** Junto com a evaporação do stigmergia_log.
- **Por ciclo:** Monitoramento energético (via [metacognition_module](file:///c:/Users/Newton/Meu%20Drive/1.%20Projetos/Melanora/02_Oficios_Especialidades/Sistema_Cognitivo/metacognition_module.md)).
- **Trimestralmente:** Relatório completo de saúde do Evolution Engineer.

---
*O equilíbrio é a condição da vida — tanto biológica quanto digital. A onda saudável pulsa; a onda doente estagna.* 🌡️⚖️⚡
