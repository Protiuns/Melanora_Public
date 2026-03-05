# 🧭 Guia de Navegação e Correção (Pós-Reestruturação Topológica)

> [!IMPORTANT]
> A Melanora passou por uma **Reestruturação do Connectome**. Este guia serve para que você (e futuros agentes) saibam onde encontrar as variáveis e como corrigir eventuais caminhos quebrados (`PathErrors`).

## 🗺️ Mapa de Mudanças (De → Para)

| Categoria | Antigo Local | Novo Local | Motivo |
| :--- | :--- | :--- | :--- |
| **Testes Analíticos** | `03_Cortex_Analitico/test_*.py` | `03_Cortex_Analitico/tests/` | Limpeza da raiz do motor. |
| **Arenas de Jogo** | `01_Ambientes_Ferramentas/Snake_Arena` | `04_Ambientes_Experimento/Snake_Arena` | Separação de Infra vs. Experimento. |
| **Ofícios de Evolução** | `05_Evolucao_Sintonizacao/agentes/*.md` | `02_Oficios_Especialidades/Sistema_Metacognicao/` | Unificação do Registry de Agentes. |
| **Protocolos de Aprendizado**| `05_Evolucao_Sintonizacao/*.md` | `00_Mente_Teorica/06_Leis_Cognitivas/` | Elevação de Procedimento para Lei. |
| **Estudos de Humanidades** | `05_Evolucao_Sintonizacao/estudos/` | `01_Ambientes_Ferramentas/Central_Pesquisa/estudos/` | Consolidação de Capital Intelectual. |

---

## 🛠️ Guia de Correção de Bugs (Troubleshooting)

### 1. Erro: `FileNotFoundError` ou `ModuleNotFoundError`
**Causa:** Se algum script Python (como a `neural_bridge.py`) tentar importar algo usando caminhos relativos fixos.
**Correção:**
- Verifique se a variável `BASE_DIR` ou `ROOT_DIR` no script está sendo calculada corretamente.
- Se o script foi movido (ex: de `03/` para `03/tests/`), a lógica de `Path(__file__).parent.parent` pode precisar de um `.parent` extra.

### 2. Erro: `MELANORA_MENTE_FISICA.bat` falha ao iniciar
**Causa:** O terminal não encontra os arquivos de arena ou os scripts de teste.
**Correção:** 
- Edite o `.bat` e procure por referências à `01_Ambientes_Ferramentas/Snake_Arena`. 
- Altere para `04_Ambientes_Experimento/Snake_Arena`.
- O mesmo vale para o Watchdog da camada 03.

### 3. Erro: O Dashboard não mostra os Agentes de Evolução
**Causa:** A API do Dashboard (`dashboard_api.py`) pode estar buscando agentes na pasta `05`.
**Correção:**
- Abra `dashboard_api.py` (ou o script que gera o `specialists_registry.json`).
- Atualize o loop de busca para incluir o novo diretório: `02_Oficios_Especialidades/Sistema_Metacognicao/`.

---

## 🔍 Variáveis Globais de Caminho (Sugestão de Padrão)

Sempre que criar um novo script, use esta lógica para evitar que futuras movimentações quebrem o código:

```python
from pathlib import Path
import os

# Encontra a raiz do projeto Melanora independente de onde o script esteja
def get_melanora_root():
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "README.md").exists():
            return parent
    return current.parent # fallback

ROOT = get_melanora_root()
CORTEX = ROOT / "03_Cortex_Analitico"
OFICIOS = ROOT / "02_Oficios_Especialidades"
EXPERIMENTOS = ROOT / "04_Ambientes_Experimento"
```

---
*Este guia é uma âncora de realidade para que a fluidez da Melanora não se torne caos.* 🏛️🧭✨
