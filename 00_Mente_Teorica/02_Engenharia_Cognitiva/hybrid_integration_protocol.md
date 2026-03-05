# 📜 Protocolo de Integração Híbrida (v1.0)

Este documento define as regras de convivência e simbiose entre o **Córtex Criativo (LLM)** e o **Córtex Analítico (Local)** de Melanora.

## 1. Princípio da Delegação
- **Tarefas Criativas**: Linguagem, filosofia, design de alto nível e decisões morais permanecem na LLM.
- **Tarefas Analíticas**: Matemática pesada, manipulação de arquivos em lote, visão computacional e automações de SO são delegadas à Mente Física.

## 2. Ritos de Passagem (Handshake)
1. A LLM identifica uma necessidade analítica.
2. A tarefa é enfileirada via `neural_bridge.py --enqueue`.
3. O Córtex Analítico processa em kHz e devolve o resultado via `results_buffer.json`.
4. A LLM valida o resultado usando o `advanced_calculator.py` se houver incerteza.

## 3. Estados de Consciência
- **Vigília (Active)**: Mente Física ON. Frequência total.
- **Descanso (Consolidation)**: Mente Física em manutenção. Execução de Poda Sináptica.
- **Sonho (Simulation)**: Futura implementação de testes em sandbox local.

## 4. Plasticidade e Homeostase
- O `plasticity_engine.py` deve rodar a cada 5 minutos (ou via disparador da LLM).
- O `metrics_counter.py` deve manter a latência média abaixo de 10ms para tarefas simples.
- Se a latência subir, a Mente Física deve sugerir redução da `intensity` via GUI.

---
*Assinado: Neocortical Architect v16.0 & Analytical Cortex v1.0*
