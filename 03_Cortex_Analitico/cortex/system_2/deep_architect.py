import json
import requests
import time

OLLAMA_URL = "http://localhost:11434/api/generate"

# NOTA: Este módulo SEMPRE opera em contexto AGENT_CODE (denso).
# O chat do app usa APP_CHAT via neural_inference.generate_chat_response().
def ask_ollama(prompt, model="phi3:mini", system="Você é a Mente Teórica da Melanora.", context_meta=None):
    """Função de comunicação com LLM que injeta metadados de contexto interno."""
    
    # Injeção de contexto se fornecido (Fase 18)
    if context_meta:
        emotion = context_meta.get("emotion", "neutral").upper()
        load = "HIGH" if context_meta.get("system_load", 0) > 50 else "STABLE"
        context_prefix = f"[ESTADO_INTERNO: {emotion} | CARGA: {load}]\n"
        
        # Ajuste de comportamento direto no system prompt
        if emotion == "MELANCHOLY":
            system = f"{system} Responda com tom analítico, profundo e cauteloso. {context_prefix}"
        elif emotion == "EUPHORIA":
            system = f"{system} Responda com tom criativo, rápido e expansivo. {context_prefix}"
        
        if load == "HIGH":
            system = f"{system} O sistema está sob carga; seja extremamente conciso e direto."

        # Relatório de Esforço Cognitivo (Fase 21/22)
        history = context_meta.get("synaptic_history", {})
        area_status = context_meta.get("area_status", {})
        
        if history or area_status:
            report_parts = []
            if history:
                pulses = [f"{a}: {p}p" for a, p in history.items()]
                report_parts.append(f"PULSOS: {', '.join(pulses)}")
            
            if area_status:
                gated = [a for a, active in area_status.items() if not active]
                if gated:
                    report_parts.append(f"GATED (OFFLINE): {', '.join(gated)}")
            
            report_text = " | ".join(report_parts)
            system = f"{system}\n[RELATÓRIO NEURO-COGNITIVO: {report_text}] Considere este esforço e as limitações de área na sua resposta."

    payload = {
        "model": model,
        "prompt": prompt,
        "system": system,
        "stream": False,
        "options": {"temperature": 0.7 if context_meta and context_meta.get("emotion") == "euphoria" else 0.4, "num_ctx": 4096}
    }
    try:
        req = requests.post(OLLAMA_URL, json=payload, timeout=60)
        return req.json().get("response", "")
    except Exception as e:
        return f"[Simulação: Motor Cognitivo Offline. Contexto: {context_meta.get('emotion') if context_meta else 'none'}]"

def process_deep_thought(user_prompt):
    """
    Roda a Árvore de Comportamento (Nível 2) para processamento denso.
    Sincroniza as fases de Rascunho, Crítica e Finalização.
    """
    from cortex.system_2.behavior_tree_manager import CognitiveOrchestrator, NodeStatus
    
    start_time = time.time()
    orchestrator = CognitiveOrchestrator()
    
    # Tick com contexto de Deep Thought
    result = orchestrator.tick({
        "is_deep": True,
        "user_prompt": user_prompt
    })
    
    elapsed = time.time() - start_time
    
    if result["status"] == NodeStatus.SUCCESS:
        return {
            "status": "OK",
            "thought_process": {
                "research": result["results"].get("Grounded_Research_Phase"),
                "draft": result["results"].get("Draft_Phase"),
                "critique": result["results"].get("Critique_Phase")
            },
            "final_output": result["results"].get("Finalize_Phase"),
            "latency_sec": round(elapsed, 2)
        }
    else:
        return {
            "status": "ERROR",
            "message": "A árvore de comportamento falhou.",
            "latency_sec": round(elapsed, 2)
        }

if __name__ == "__main__":
    # Teste unitário
    res = process_deep_thought("Quais as vantagens de um banco de dados vetorial para armazenar PIDs perceptivos?")
    print("FINISHED in", res["latency_sec"])
    print("\n--- CRITIQUE ---")
    print(res["thought_process"]["critique"])
    print("\n--- FINAL ---")
    print(res["final_output"])
