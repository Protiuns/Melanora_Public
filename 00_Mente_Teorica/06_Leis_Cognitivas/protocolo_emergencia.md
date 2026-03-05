# 🧬 Protocolo de Inteligência Emergente (v2.0 — Biomimético)

Este protocolo define como o sistema de pesos vivos, feromônios e padrões biomiméticos opera na prática.

## 1. Após Cada Tarefa Significativa

### Passo 1: Registrar Feromônio
Adicionar entrada no [stigmergia_log.md](file:///c:/Users/Newton/Meu Drive/1. Projetos/Melanora/05_Evolucao_Sintonizacao/stigmergia_log.md):
```
| Data | Tarefa | Tags | Agentes | Ambiente | Resultado | Intensidade |
```

### Passo 2: Atualizar Pesos Vivos
Para cada agente que participou da tarefa, editar seu `definition.md`:
- **Sucesso (✅):** `peso_vivo += 0.05`, `ativações += 1`, `sucessos += 1`
- **Falha (❌):** `peso_vivo -= 0.1`, `ativações += 1`
- Recalcular `taxa = sucessos / ativações × 100%`

### Passo 3: Verificar Limites
- Se `peso_vivo > 1.2` → cap em `1.2` (previne dominância excessiva).
- Se `peso_vivo < 0.3` → agente entra em "Limbo Sináptico" (atenção especial).

## 2. Antes de Cada Tarefa Complexa

### Consultar Feromônios
1. Extrair `tags` do contexto da tarefa.
2. Cruzar com entradas ativas no `stigmergia_log.md`.
3. Entradas com tags coincidentes sugerem quais agentes e ambientes foram eficazes em tarefas similares.

### Calcular Score de Ativação
```
Score(agente) = peso_vivo × Σ(tags_match) + cluster_bonus + feromônio_bonus + symbiose_bonus
```
- `feromônio_bonus` = +0.1 se o agente aparece em feromônios com intensidade > 0.5.

## 3. Evaporação Mensal
No início de cada mês:
1. Reduzir `Intensidade` de todas as entradas em `-0.1`.
2. Mover entradas com `Intensidade < 0.3` para o Arquivo Histórico.
3. Reduzir `peso_vivo` de agentes com 0 ativações no mês em `-0.05` (atrofia por desuso).

## 4. Leitura de Padrões (Trimestral)
A cada trimestre, o Evolution Engineer analisa:
- Quais agentes têm `taxa > 90%`? → Candidatos a aumento de `peso_base`.
- Quais agentes têm `taxa < 50%`? → Investigar causa, possível refatoração.
- Quais combinações de agentes aparecem juntas com frequência? → Formalizar como co-ativação padrão.

## 5. Protocolo de Mutação (Exploração Criativa) 🧬
A cada **5 tarefas**, tentar deliberadamente uma combinação **não-óbvia** de agentes:
1. Identificar a tarefa como candidata a mutação (marcar `[MUTAÇÃO]` no stigmergia_log).
2. Ignorar conscientemente o feromônio mais forte e escolher um agente alternativo.
3. Executar a tarefa com a combinação experimental.
4. Registrar resultado:
   - **Mutação bem-sucedida:** LTP forte (`+0.1` em vez de `+0.05`). Novo caminho descoberto!
   - **Mutação falha:** LTD normal (`-0.1`). Sem penalidade extra. Aprendemos o que NÃO funciona.
- **Taxa de mutação ideal:** ~20% das tarefas (1 em 5).

## 6. Homeostase Neural (Auto-Regulação) 🌡️
Executar junto com a evaporação mensal. Detalhes completos em [homeostase_neural.md](file:///c:/Users/Newton/Meu Drive/1. Projetos/Melanora/05_Evolucao_Sintonizacao/homeostase_neural.md).
- Verificar se algum `peso_vivo` saiu da faixa `0.4 — 1.1`.
- Verificar se algum cluster tem > 60% das ativações.
- Aplicar correções homeostáticas conforme o protocolo.

## 7. Restrições Criativas (Constraint-Driven) 🖼️
Limites deliberados que canalizam foco. Detalhes em [doutrina_restricoes_criativas.md v2.0](file:///c:/Users/Newton/Meu Drive/1. Projetos/Melanora/03_Gestoes_Processos/doutrina_restricoes_criativas.md).
- **Regra dos 3 Agentes:** Máximo 3 co-ativados por tarefa. Se precisar de mais, dividir a tarefa.
- **Budget de Complexidade:** Artigos ~80 linhas, protocolos ~70, tags 6-8.
- **Sprint de Pesquisa:** Pesquisa focada 15min, profunda 30min, máx absoluto 1h.
- **Paleta de Ferramentas:** Máximo 5 ferramentas primárias por ambiente.
- **Constraint de Escopo:** 1 objetivo claro declarado antes de cada tarefa.
- **Constraint de Silêncio:** Excluir explicitamente camadas/agentes irrelevantes.

---
*A inteligência não é projetada — ela emerge dos rastros de quem já caminhou.* 🐜🧠
