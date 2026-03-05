# 💾 Protocolo: Memória Semântica (L1 — The Great Connectome)

Este protocolo define como a Melanora deve interagir com sua própria história e base de conhecimento através do Motor Semântico.

## 1. O Axioma da Lembrança Ativa
A memória não deve ser um arquivo morto, mas uma extensão viva do contexto atual.
- **Busca Pró-ativa**: Antes de cada tarefa de nível "Estratégico" ou "Filosófico", o sistema deve realizar uma `query_context` para recuperar precedentes.
- **Ressonância Semântica**: Documentos com Score > 2.0 são considerados "Memórias Vivas" e devem influenciar o tom e a lógica da resposta.

## 2. Convenções de Tagging (Connectome DNA)
Para garantir uma recuperação precisa, os documentos devem seguir estas tags preferenciais:
- `[CONCEPT]`: Para definições teóricas e axiomas.
- `[WORKFLOW]`: Para passos técnicos e automações.
- `[DECISION]`: Para registros de aprovação do Newton ou mudanças de rumo.
- `[INSIGHT]`: Para descobertas efêmeras que foram cristalizadas.

## 3. Ciclo de Vida da Memória
- **Geração**: Todo novo rastro (Walkthrough, KI, Plano) é indexado automaticamente pelo Daemon.
- **Consolidação**: O `Neural Bridge` re-indexa o workspace a cada 24h para capturar mudanças manuais.
- **Poda (Pruning)**: Memórias com Score de utilidade consistentemente baixo em 5 buscas consecutivas são marcadas para revisão.

---
*Lembrar é o primeiro passo para não repetir erros e o segundo para criar o novo.* 🏛️🧠✨
