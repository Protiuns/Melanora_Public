import json
import time
from pathlib import Path
from cortex.utils.cortex_utils import cortex_function
from neural_bridge import log_event

# Caminhos de configuração
CONFIG_DIR = Path(__file__).parent.parent / "config"
STATE_FILE = CONFIG_DIR / "neural_state.json"
HISTORY_FILE = CONFIG_DIR / "dialogue_history.json"
LLM_CONTEXT_FILE = CONFIG_DIR / "llm_context_config.json"

# Motores de IA e Memória
from cortex.specialists.neural_inference import generate_chat_response
try:
    from cortex.specialists.semantic_memory import get_semantic_engine
    memory_engine = get_semantic_engine()
except ImportError:
    memory_engine = None

def _get_active_chat_context(override_context_name: str = None):
    """Retorna as configs do contexto ativo para o chat do app."""
    defaults = {"inject_semantic_memory": False, "inject_history_turns": 1, "system_prompt_mode": "MINIMAL"}
    try:
        with open(LLM_CONTEXT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        ctx_name = override_context_name or data.get("active_app_context", "APP_CHAT")
        return data.get("contexts", {}).get(ctx_name, defaults), ctx_name
    except Exception:
        return defaults, override_context_name or "APP_CHAT"

@cortex_function
def extract_unified_prompt(text: str = "", audio_metadata: dict = None, vision_metadata: dict = None, llm_context_override: str = None) -> dict:
    """
    🧠 Orquestrador de Diálogo: Unifica entradas multi-modais em um rastro de intenção.
    """
    try:
        # 1. Carregar estado atual para contexto
        state = {}
        if STATE_FILE.exists():
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)

        symbiotic_mode = state.get("symbiotic_mode", "NORMAL")
        
        # Carregar perfil de contexto LLM
        ctx_cfg, ctx_name = _get_active_chat_context(llm_context_override)
        max_history = ctx_cfg.get("inject_history_turns", 1)
        use_semantic = ctx_cfg.get("inject_semantic_memory", False)
        
        # 2. Refinamento Afetivo (Baseado no modo de simbiose)
        refined_text = text
        urgency = 1.0
        
        if symbiotic_mode == "CHAOS":
            urgency = 2.0
        elif symbiotic_mode == "FLOW":
            urgency = 0.5
            
        # 3. Resolução Deítica (Contexto de Visão)
        deictic_context = ""
        if vision_metadata and vision_metadata.get("active"):
            focus = vision_metadata.get("detected_focus", "unknown")
            if "isso" in text.lower() or "aqui" in text.lower():
                deictic_context = f" [Visual: {focus}]"
        
        # 4. Contexto de Memória Semântica (apenas se habilitado pelo perfil)
        semantic_context = ""
        if use_semantic and memory_engine:
            semantic_context = memory_engine.query_context(text, top_k=2)
        
        # 5. Histórico Recente (limitado pelo perfil)
        recent_history = ""
        if max_history > 0 and HISTORY_FILE.exists():
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    hist_data = json.load(f).get("entries", [])[-max_history:]
                    for entry in hist_data:
                        recent_history += f"U: {entry.get('user_text')}\nM: {entry.get('intent', {}).get('ai_response', '')}\n"
            except: pass

        # 6. Geração de Resposta pela LLM Local
        context_payload = f"Modo: {symbiotic_mode}"
        if semantic_context:
            context_payload += f"\nMemória:\n{semantic_context}"
        if recent_history:
            context_payload += f"\nHist:\n{recent_history}"
        ai_response = generate_chat_response(f"{refined_text}{deictic_context}", context=context_payload, llm_context=ctx_name)

        # 5. Construção do Payload Final
        unified_intent = {
            "raw_text": text,
            "final_prompt": f"{refined_text}{deictic_context}",
            "ai_response": ai_response,
            "metadata": {
                "urgency": urgency,
                "symbiotic_mode": symbiotic_mode,
                "sensors_active": {
                    "audio": audio_metadata.get("active", False) if audio_metadata else False,
                    "vision": vision_metadata.get("active", False) if vision_metadata else False
                },
                "timestamp": time.time()
            }
        }

        log_event(f"DIÁLOGO: Prompt gerou resposta '{ai_response[:30]}...' (Urgência: {urgency})")
        return {"status": "OK", "intent": unified_intent}

    except Exception as e:
        log_event(f"Falha no Orquestrador de Diálogo: {str(e)}", "ERROR")
        return {"status": "ERROR", "message": str(e)}

if __name__ == "__main__":
    # Teste de fusão
    print(extract_unified_prompt("O que é isso?", vision_metadata={"active": True, "detected_focus": "arquivo perception_engine.py"}))
