---
description: Sincroniza e atualiza automaticamente a documentação e skills do projeto Briguentinho.
---

# 🤖 Workflow de Evolução: Briguentinho

Este workflow garante que a documentação (GDD, Blueprint, Master Prompt) reflita sempre o estado atual da implementação.

## 🚀 Passos de Automação:

// turbo
1. Executar sincronizador de documentos:
   `python "c:\Users\Newton\Meu Drive\1. Projetos\Melanora\.agent\scripts\sync_briguentinho_docs.py"`

2. Atualizar Skill de Prompt:
   `view_file "c:\Users\Newton\Meu Drive\1. Projetos\Melanora\.agent\skills\godot_prompt_architect\SKILL.md"`

3. Logar progresso no Status do Projeto:
   `view_file "C:\Users\Newton\.gemini\antigravity\brain\a503a51d-3513-45fa-bf80-14e8f9cfdfa4\PROJECT_STATUS.md"`

---
> [!TIP]
> Use este workflow após cada "Phase" do Master Prompt para manter a sanidade da arquitetura.
