---
description: Auditoria de Consistência e Versão do Estúdio
---

# 🔍 Workflow: Studio Auditor (v1.0)

Este workflow deve ser executado periodicamente ou quando o usuário solicitar uma "revisão de sistema". Ele garante que os projetos não fiquem com componentes obsoletos.

## 📋 Passo a Passo

### 1. Inventário de Componentes Ativos
Identifique quais componentes da `studio_library` estão sendo usados nos projetos:
- Liste os arquivos em `projects/[PROJETO]/godot_project/src/shared/components/`.
- Verifique se existem referências diretas no `project.godot` (Autoloads).

### 2. Comparação de Versões
Para cada componente localizado:
- Leia a primeira linha do arquivo local (ex: `## v3.0`).
- Considere a versão do registro central em `Melanora/studio_library/_registry/component_registry.json`.
- Verifique se há uma versão mais recente disponível na pasta do componente (ex: `studio_library/logic/health_component/v2/`).
- Se o registro ou a pasta indicar uma versão maior (ex: mestre v3.2 ou v2.0 vs local v1.0), marque para atualização.
- **Importante:** Se a atualização for MAJOR (v1 -> v2), verifique se o projeto suporta a mudança (Side-by-Side versioning).

### 3. Verificação de Integridade UI (Themes)
- Verifique se o projeto possui um `StudioThemeManager`.
- Verifique se os `StudioButton` estão configurados com o grupo `studio_buttons`.

### 4. Auditoria de Hierarquia e Especialização (v2.0)
Analise se os componentes do projeto respeitam a estrutura de níveis:
- **Violação de Nível:** Componentes de Nível 1 referenciando Nível 3 ou nomes de nós específicos do projeto.
- **Mismatch de Estilo:** Componentes de `platformer` sendo usados em projetos `topdown` (ou vice-versa) sem adaptação.
- **Empty Exports:** Busque por componentes de Nível 2 ou 3 que não tenham suas referências obrigatórias (requires) conectadas no Inspetor.

### 5. Relatório de Auditoria Completa
Gere um relatório para o usuário no formato:

**⚠️ Componentes Desatualizados em [Projeto]:**
- `player_driver_2d.gd`: Projeto v3.0 | Biblioteca v3.2 (Melhoria: Adicionado Coyote Time)
- `hud_component.gd`: Projeto v1.0 | Biblioteca v1.2 (Melhoria: Suporte a Temas)

### 5. Execução da Sincronização
Com a permissão do usuário:
1. Sobrescreva o arquivo local com o conteúdo do arquivo mestre.
2. Certifique-se de manter qualquer customização específica do projeto (se houver, use o `multi_replace_file_content` para fundir as alterações).
3. Atualize o `component_registry.json` se necessário.
