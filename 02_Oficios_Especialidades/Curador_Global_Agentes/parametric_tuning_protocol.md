# 🎛️ Protocolo de Ajuste Paramétrico (NSR-to-Config)

Este protocolo define a lógica de tradução entre o **Registro Sináptico Neural (NSR)** e a configuração ativa dos componentes da Melanora.

## 📈 1. Mapeamento de Vieses (Agentes/Nódulos)

| Métrica Neural (Bias) | Parâmetro de Operação | Efeito no Comportamento |
| :--- | :--- | :--- |
| **Bias > 1.4** | `Proactivity: HYPER` | O agente sugere mudanças e antecipa necessidades sem comando. |
| **1.0 < Bias <= 1.4** | `Proactivity: ACTIVE` | O agente responde com alternativas e insights extras. |
| **Bias < 1.0** | `Proactivity: REACTIVE` | O agente executa estritamente o que foi solicitado. |

## 🔗 2. Mapeamento de Pesos (Sinapses/Conexões)

| Força Sináptica (Weight) | Parâmetro de Rigor | Efeito na Execução |
| :--- | :--- | :--- |
| **Weight > 1.6** | `Confidence: TOTAL` | Execução direta com pouca redundância de logs. |
| **1.0 < Weight <= 1.6** | `Confidence: BALANCED` | Execução com logs detalhados e checkpoints. |
| **Weight < 1.0** | `Confidence: CAUTIOUS` | Exige tripla validação e confirmação do Subconsciente. |

## 🛠️ 3. Aplicação em Ferramentas (Ex: Pesquisa)

- **Profundidade (Mining Depth)**: Calculada como `(Bias do Agente + Weight da Sinapse Tool) / 2`.
  - Result > 1.5: Pesquisa na 2ª e 3ª camada de links.
  - Result <= 1.5: Foco apenas no conteúdo principal (1ª camada).

---
*A técnica agora responde à pressão do pensamento.* ⚡⚙️
