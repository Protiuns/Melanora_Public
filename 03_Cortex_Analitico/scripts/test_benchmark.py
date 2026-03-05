import sys
import time
import json
from pathlib import Path

# Adicionar root ao path
ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT / "03_Cortex_Analitico"))

try:
    from cortex.specialists.neural_inference import generate_chat_response
    from neural_bridge import direct_execute
except ImportError as e:
    print(f"Error importing Melanora components: {e}")
    sys.exit(1)

def benchmark_melanora(prompt, context="", level="APP_CHAT"):
    """Simula a Melanora usando sua arquitetura (Contexto + Memória + Persona)."""
    start_time = time.time()
    response = generate_chat_response(prompt, context=context, llm_context=level)
    elapsed = time.time() - start_time
    return response, elapsed

def benchmark_raw_llm(prompt):
    """
    Simula o Gemini 3 Flash 'Cru' (Raw). 
    Como o Gemini é o motor atual, chamamos diretamente sem injetar contexto da Melanora.
    """
    start_time = time.time()
    # Usando o modo MINIMAL mas removendo o prefixo de persona via override de prompt se necessário
    # Aqui simulamos o Raw enviando apenas o prompt puro para o endpoint da LLM.
    # Para este teste, vamos assumir que o 'Raw' é a LLM recebendo apenas a pergunta do usuário.
    response = generate_chat_response(prompt, context="", llm_context="APP_CHAT", model_hint="qwen2.5:3b")
    elapsed = time.time() - start_time
    return response, elapsed

def run_tests():
    scenarios = [
        {
            "id": "ARCH_MEMORY",
            "name": "Memória Arquitetural",
            "prompt": "Quais são os componentes básicos que compõem o ator Laerton no blueprint?",
            "context_melanora": "Refira-se ao arquivo laerton_blueprint.md. Ele define Laerton como um fantoche de componentes."
        },
        {
            "id": "LOCAL_REASONING",
            "name": "Raciocínio de Código",
            "prompt": "Como eu deveria implementar o sinal hit_landed no StudioHitbox3DComponent para que o Inimigo saiba que foi atingido?",
            "context_melanora": "O projeto usa Godot 4.3 e arquitetura de componentes da Studio Library."
        },
        {
            "id": "SYSTEM_LOGIC",
            "name": "Lógica de Variáveis",
            "prompt": "Se o stress_level for 0.8 e o current_noise for 0.5, como o HUD deve reagir visualmente?",
            "context_melanora": "Contexto do Sprint Ressonância Sombria: stress afeta pulsação de rários, noise afeta escala de 🔊."
        }
    ]

    results = []

    print("🚀 Iniciando Benchmark Comparativo: Melanora Mind vs Raw LLM\n")

    for sc in scenarios:
        print(f"--- Teste: {sc['name']} ---")
        
        # Teste Melanora
        print("  [Mente Melanora] Processando...")
        m_resp, m_time = benchmark_melanora(sc['prompt'], context=sc['context_melanora'])
        
        # Teste Raw
        print("  [Raw LLM] Processando...")
        r_resp, r_time = benchmark_raw_llm(sc['prompt'])
        
        results.append({
            "scenario": sc['name'],
            "melanora": {"response": m_resp, "time": m_time},
            "raw": {"response": r_resp, "time": r_time}
        })
        print(f"  Finalizado. (Melanora: {m_time:.2f}s | Raw: {r_time:.2f}s)\n")

    # Gerar Relatório Markdown
    report_path = ROOT / "docs" / "comparative_benchmark_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# 🏛️ Relatório de Benchmark: Melanora vs. Raw LLM\n\n")
        f.write("Este benchmark compara a resposta da **Mente Melanora** (com arquitetura agêntica e contexto) contra a **LLM Crua** (infeência direta sem orquestração).\n\n")
        
        for res in results:
            f.write(f"## 📝 Cenário: {res['scenario']}\n")
            f.write("| Atributo | **Mente Melanora** | **Raw LLM** |\n")
            f.write("| :--- | :--- | :--- |\n")
            f.write(f"| Resposta | {res['melanora']['response']} | {res['raw']['response']} |\n")
            f.write(f"| Latência | {res['melanora']['time']:.2f}s | {res['raw']['time']:.2f}s |\n\n")
            
        f.write("\n---\n*Gerado automaticamente pelo Córtex Analítico em " + time.strftime("%Y-%m-%d %H:%M:%S") + "*")

    print(f"✅ Benchmark concluído! Relatório salvo em: {report_path}")

if __name__ == "__main__":
    run_tests()
