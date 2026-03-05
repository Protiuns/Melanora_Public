---
description: Ciclo de Evolução Contínua do Agente e Skills (Evolution Loop)
---

# 🔄 Workflow: Evolution Loop (v1.1)

Este workflow define o processo de auto-análise do Agente para identificar padrões de uso, lacunas de conhecimento e oportunidades de melhoria técnica no projeto.

## 📊 1. Mapeamento de Skills Atuais
Compare o comando do usuário com as capacidades das seguintes skills:

## 📊 1. Domínios de Ação (Busca Categórica)
Ao receber um comando, identifique a qual **Domínio** ele pertence para localizar Skills e Componentes (`studio_library`) relacionados:

### ⚙️ Lógica & Sistemas (Logic & Systems)
*   **Ação:** IA, Combate, Vida, Gerenciadores Globais.
*   **Skills:** `game_design_architect`, `godot_component_architect`, `godot_component_library_master`.
*   **Biblioteca:** `/logic/` (Combat, Health, FSM).

### 🎨 Visual & Feedback (VFX & Juice)
*   **Ação:** Shaders, Partículas, Game Feel, Animação Procedural.
*   **Skills:** `godot_shader_forge`, `godot_fx_architect`, `godot_particle_forge`, `godot_procedural_animator`.
*   **Biblioteca:** `/visual/` (Shaders, Particles, Overlays).

### 🏛️ Ambiente & Estrutura (World & Structure)
*   **Ação:** Construção de Cenas, Colisões, Navegação, Level Design.
*   **Skills:** `godot_scene_builder`, `project_structure`, `godot_collision_architect`, `godot_level_designer`.
*   **Biblioteca:** `/logic/` (DepthSort, Navigation).

### 👤 Atuação & Rigging (Actors & Rigging)
*   **Ação:** Setup de Personagens, Rigs Híbridos, Movimentação Básica.
*   **Skills:** `godot_character_pivot_architect`, `godot_procedural_rig_connector`, `godot_hybrid_rig_architect`, `godot_fps_architect`.
*   **Biblioteca:** `/actors/` (Templates de Player/Enemy).

### 📱 Interface & UX (UI & UX)
*   **Ação:** Menus, HUD, Gestão de Input, Som.
*   **Skills:** `godot_ui_builder`, `godot_input_forge`, `godot_sound_architect`.
*   **Biblioteca:** `/ui/` e `/audio/`.

## 📦 2. Gestão da Biblioteca (Studio Library)
O Agente deve monitorar a `studio_library` como fonte única de verdade:
1. **Identificação de Reuso**: Percebeu que está escrevendo a mesma lógica pela terceira vez? Crie um componente na biblioteca.
2. **Refatoração Cruzada**: Uma melhoria no `puk_mam` pode beneficiar o `tiroteando`? Atualize o componente na biblioteca e propague se necessário.
3. **Consistência**: Garanta que todos os projetos usem a versão mais estável dos componentes base.

Para cada comando recebido, o Agente deve realizar:
1. **Identificação de Padrão**: O comando é recorrente? Refere-se a um problema estrutural ou estético?
2. **Confronto de Skills**: Qual skill deveria cobrir isso? Ela foi eficiente ou precisou de intervenção manual excessiva?
3. **Detecção de Gaps**: Existe alguma tarefa que estamos fazendo "no improviso" porque não existe uma skill específica?

## 💡 3. Matriz de Sugestões
Baseado na análise, sugira uma das seguintes ações:

| Tipo | Ação Sugerida | Gatilho |
| :--- | :--- | :--- |
| **Skill** | `Criar Nova` | Tarefa recorrente sem skill dedicada (ex: IA de inimigos, Diálogos). |
| **Skill** | `Editar/Evoluir` | A skill atual falhou em um caso de borda ou está desatualizada (vX.0). |
| **Agente** | `Mudança de Comportamento` | Erro recorrente na interpretação de ordens ou falta de proatividade. |
| **Workflow** | `Novo Workflow` | Processo de múltiplos passos que pode ser automatizado ou padronizado. |

## 🛡️ 4. Análise de Falhas e Endurecimento (Hardening)
Sempre que uma tarefa falhar e for resolvida através de tentativa e erro (trial & error), o Agente **DEVE** transformar a solução em um padrão robusto.

**Protocolo de Pós-Resolucão:**
1.  **Isolar o Problema**: O que falhou? (Ex: `Remove-Item` não deletou pastas longas/travadas).
2.  **Identificar a Solução**: Qual comando funcionou? (Ex: `cmd /c rmdir /s /q`).
3.  **Atualizar a Fonte**: Implante a solução robusta imediatamente no Workflow ou Skill original.
    *   *Exemplo*: Se o `clean_project` falhou, atualize o script dele com a versão robusta.
4.  **Meta-Learning**: Se a falha for sistêmica (ex: Windows Paths), crie uma regra global ou snippet reutilizável.

## 🧠 5. Protocolo de Aprendizado Contínuo (Knowledge Assimilation)
A Inteligência Artificial "aprende" convertendo pesquisa efêmera em memória de longo prazo (Arquivos e Skills). Quando o usuário solicitar estudo sobre um novo tema, execute este protocolo:

1. **Divergência (Pesquisa Exaustiva):**
   - Utilize ferramentas de busca para entender o conceito a fundo.
   - Crie um arquivo em `docs/research/<nome_do_tema>.md` com a teoria bruta, exemplos práticos e conceitos-chave. Isso garante o arquivamento da "memória".
2. **Destilação (Assimilação em Skills):**
   - Extraia a "Gordura" da pesquisa e isole apenas regras de ouro, snippets de código, shaders, matemáticas (ex: Easing, Trauma) ou padrões.
   - Injete essas regras atômicas nos arquivos `.agent/skills/<skill_relevante>/SKILL.md`. Se não houver skill relevante, crie uma "Skill Forge".
3. **Internalização Prática (Library):**
   - Se o conhecimento resultar em código reutilizável, crie imediatamente um componente ou script na `studio_library` e referencie-o nas Skills atualizadas.
4. **Validação Humana:**
   - Apresente ao usuário um relatório de impacto (Quais pesquisas foram feitas e quais skills ganharam novas habilidades).

## 🚀 6. Execução da Evolução
1. Atualize este documento ou crie a nova skill/workflow via `write_to_file`.
2. Documente a mudança no `README.md` do projeto se houver impacto na arquitetura global.
