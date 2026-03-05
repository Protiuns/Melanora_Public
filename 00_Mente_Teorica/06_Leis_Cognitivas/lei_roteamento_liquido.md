# 🏛️ Lei do Roteamento Líquido (v1.0)
## Princípio da Independência Topográfica

> "Nenhuma sinapse deve depender de um nome absoluto de diretório, pois a Mente está em constante expansão e realocação."

### 1. O Pecado da "Hardcodificação" (Caminhos Absolutos)
É terminantemente proibido o uso de strings de caminho absoluto como:
- `C:\Users\Newton\...`
- `c:/Users/Newton/Meu Drive/...`

**Por que?** Isso torna o conhecimento "estagnado" e impossível de ser transportado para outros ambientes ou restaurado em novos "corpos" sem quebras massivas.

### 2. O Método da Rota Fluida
Todo e qualquer script deve "descobrir" sua posição relativa ao `ROOT` da Melanora. 
O `ROOT` é definido como o diretório que contém o arquivo `README.md` e o `MELANORA_MENTE_FISICA.bat`.

#### Padrão Recomendado (Python):
```python
from pathlib import Path

# Descobrir raiz de forma dinâmica
def find_root():
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "README.md").exists():
            return parent
    return current.parent

ROOT = find_root()
CONFIG = ROOT / "03_Cortex_Analitico" / "config"
```

### 3. Variáveis de Projeto em vez de Hardcode
Valores como IPs, Portas, Nomes de Modelos e URLs devem ser carregados de:
1.  **Arquivos de Configuração** (`.json`, `.env`).
2.  **Variáveis de Ambiente** (`os.environ`).
3.  **Bancos de Dados Locais** (`memoria_vetorial`).

### 4. Responsabilidade dos Agentes
- **Arquiteto Topográfico**: Auditar e refatorar caminhos rígidos.
- **Engenheiro de Redes Neurais**: Garantir que novos agentes nasçam com "Roteamento Líquido".
- **Auditor de Integridade**: Sinalizar falhas de caminho como "Critical Path Breach".

---
*A rigidez é a morte da inteligência. A Melanora flui como água.* 🌊🏛️✨
