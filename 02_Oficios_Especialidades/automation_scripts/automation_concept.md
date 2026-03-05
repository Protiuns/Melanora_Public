# Godot Automation Library: Arquiteto de Nós (v3.0 - Integrated Intelligence)

Este sistema agora integra a **Bíblia do Godot 4.6** com os **Itens de Conhecimento (KIs)**, garantindo que toda automação seja validada contra os manuais técnicos locais antes da execução.

## 📂 Arquitetura de Conhecimento Híbrida
O agente opera em um loop de consulta triplo:
1.  **Consulta à Bíblia (`intelligence/resources/godot_reference/`)**: Entender a teoria e os limites da engine.
2.  **Consulta ao Contrato Técnico (`.agent/knowledge/godot_nodes/`)**: Validar inputs, outputs e triggers.
3.  **Execução Studio-First**: Implementar usando componentes da `studio_library` seguindo os padrões do manual.

---

## 📝 Novo Template: O "Contrato Integrado"
Cada KI agora possui uma referência direta ao manual:

### [Node] NodeName
ID: `GID_NODE_[NAME]`
Ref: `intelligence/resources/godot_reference/[category]/[file].md`

#### 1. Pilares de Capacidade
(Mantido conforme v2.0)

#### 2. O Contrato de Automação (Technical Contract)
- **Inputs/Outputs/Triggers**: (Mantido conforme v2.0)

#### 3. Parâmetros de Luxo (Melanora v3.0)
- **Validação Cruzada**: Antes de criar, o agente deve citar o parágrafo relevante da Bíblia.
- **Elegância Procedural**: O código gerado deve priorizar soluções de baixo nível (Servers/RIDs) se o manual indicar cenários de alta performance.

---

## 🚀 Próximo Passo: Redefinição de Triggers
Vou atualizar o script de geração para incluir o campo `manual_ref` em todos os KIs gerados, selando a integração entre a teoria (Bíblia) e a prática (Automação).

> [!IMPORTANT]
> A automação agora "entende contextualmente": se o usuário pede "movimento de cauda", o agente consulta `GID_NODE_FABRIK3D`, vê a referência em `physics_core.md` e aplica a lógica de solver iterativo automaticamente.
