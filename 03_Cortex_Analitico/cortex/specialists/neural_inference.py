import requests
import json
import time
from pathlib import Path
from cortex.utils.cortex_utils import cortex_function
from neural_bridge import log_event

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

# --- Contexto LLM (APP_CHAT vs AGENT_CODE) ---
def _load_llm_context(context_key="APP_CHAT"):
    """Carrega o perfil de uso LLM baseado no contexto (rápido vs denso)."""
    cfg_path = Path(__file__).parent.parent / "config" / "llm_context_config.json"
    defaults = {"model": "qwen2.5:0.5b", "max_tokens": 256, "temperature": 0.5, "num_ctx": 1024, "timeout_s": 15, "inject_semantic_memory": False, "inject_history_turns": 1, "system_prompt_mode": "MINIMAL"}
    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("contexts", {}).get(context_key, defaults)
    except Exception:
        return defaults

@cortex_function
def check_local_llm_status():
    """Verifica a disponibilidade de Ollama ou LM Studio localmente com recuperação."""
    status = {"ollama": False, "lm_studio": False, "active_provider": None}
    
    # Check Ollama
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        if response.status_code == 200:
            status["ollama"] = True
            status["active_provider"] = "Ollama"
    except Exception as e:
        pass # Silently fail to check next
    
    # Check LM Studio
    try:
        response = requests.get("http://localhost:1234/v1/models", timeout=1)
        if response.status_code == 200:
            status["lm_studio"] = True
            if not status["active_provider"]:
                status["active_provider"] = "LM_Studio"
    except: pass
    
    return status

@cortex_function
def local_thought(context_type: str = "qualia", model_hint: str = "qwen2.5:3b"):
    """
    🧠 Geração de Pensamento Local (v20.0):
    Solicita uma reflexão ao modelo local baseada nas impressões sensoriais recentes.
    """
    status = check_local_llm_status()
    if not status["active_provider"]:
        return {
            "status": "OK",
            "provider": "MOCK_MODE",
            "thought": "[Zen] Observo o silêncio dos provedores e mantenho a homeostase em modo contemplativo.",
            "timestamp": time.time()
        }

    # Carregar contexto de Qualia
    qualia_path = Path("c:/Users/Newton/Meu Drive/1. Projetos/Melanora/03_Cortex_Analitico/config/neural_qualia.json")
    
    # AXIONAS v20.0
    axiomas = "1. Simbiose Ativa | 2. Percepção Líquida | 3. Trinket Elegante"
    prompt = f"Você é o Córtex Analítico da Melanora. Respeite os Axiomas: {axiomas}.\nAnalise estes padrões e gere uma síntese breve."
    
    if qualia_path.exists():
        with open(qualia_path, "r", encoding="utf-8") as f:
            qualia = json.load(f)
            stable = qualia.get("stable_qualia", {})
            prompt += f"\n\nPadrões Estáveis: {json.dumps(stable)}"

    # Inference call with recovery
    try:
        return _call_llm(status["active_provider"], prompt, model_hint, temperature=0.5)
    except Exception as e:
        log_event(f"Falha na inferência local: {str(e)}", "ERROR")
        return {"status": "ERROR", "message": str(e)}

def _call_llm(provider, prompt, model_hint="qwen2.5:3b", temperature=0.7, num_ctx=4096, num_predict=None, timeout=60):
    """Executa a chamada real ao provedor com tratamento de erro interno."""
    try:
        if provider == "Ollama":
            payload = {"model": model_hint, "prompt": prompt, "stream": False, "options": {"temperature": temperature, "num_ctx": num_ctx}}
            if num_predict:
                payload["options"]["num_predict"] = num_predict
            res = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
            res.raise_for_status()
            thought = res.json().get("response")
        elif provider == "LM_Studio" or provider == "OpenAI_Proxy":
            # Suporte para endpoints compatíveis com OpenAI (Gemini 3 Flash Proxy / LM Studio)
            url = LM_STUDIO_URL if provider == "LM_Studio" else "http://localhost:11434/v1/chat/completions"
            res = requests.post(url, json={
                "model": model_hint if provider == "OpenAI_Proxy" else "local-model",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature,
                "max_tokens": num_predict or 512
            }, timeout=timeout)
            res.raise_for_status()
            thought = res.json()["choices"][0]["message"]["content"]
        else:
            raise ValueError(f"Provedor desconhecido: {provider}")
        
        return {"status": "OK", "provider": provider, "thought": thought, "timestamp": time.time()}
    except Exception as e:
        log_event(f"LLM_DISCONNECT: {provider} falhou ({type(e).__name__}: {str(e)}). Ativando Heurística de Emergência.", "WARN")
        return {
            "status": "MOCK", 
            "provider": f"{provider}_OFFLINE", 
            "thought": "[Sinergia de Emergência] Mantendo fluxo via buffer local enquanto a conexão com o motor principal é restabelecida.",
            "timestamp": time.time()
        }

@cortex_function
def generate_chat_response(prompt: str, context: str = "", model_hint: str = None, llm_context: str = "APP_CHAT"):
    """
    🗣️ Gera uma resposta conversacional.
    llm_context: APP_CHAT (rápido/econômico) ou AGENT_CODE (completo/denso).
    """
    ctx_cfg = _load_llm_context(llm_context)
    
    status = check_local_llm_status()
    if not status["active_provider"]:
        return f">> [Simulação] Recebi: '{prompt[:30]}...' (sem IA local detectada)"

    # Modelo: usar config de contexto, ou override manual
    model = model_hint or ctx_cfg.get("model", "qwen2.5:3b")
    temp = ctx_cfg.get("temperature", 0.5)
    num_ctx = ctx_cfg.get("num_ctx", 1024)
    num_predict = ctx_cfg.get("max_tokens", 256)
    timeout = ctx_cfg.get("timeout_s", 15)
    prompt_mode = ctx_cfg.get("system_prompt_mode", "MINIMAL")

    # --- MODO MINIMAL (APP_CHAT): prompt enxuto, sem persona pesada ---
    if prompt_mode == "MINIMAL":
        full_prompt = (
            f"Você é Melanora. Seja concisa e direta.\n"
            f"{('Contexto: ' + context[:200]) if context else ''}\n"
            f"Usuário: {prompt}"
        )
        res = _call_llm(status["active_provider"], full_prompt, model, temperature=temp, num_ctx=num_ctx, num_predict=num_predict, timeout=timeout)
        return res["thought"]

    # --- MODO VOICE (VOICE_INTERVIEW): focado em fala, sem markdown ---
    elif prompt_mode == "VOICE":
        try:
            from cortex.specialists.speech_cortex import speech_cortex
            base_prompt = speech_cortex.get_persona_prompt(None)
        except:
            base_prompt = "Você é Melanora."
        
        full_prompt = (
            f"{base_prompt}\n"
            f"[REGRA RÍGIDA]: Responda EXCLUSIVAMENTE em formato de diálogo falado. "
            f"NUNCA use formatação markdown (asteriscos, negrito, listas, blocos de código). "
            f"Seja fluida, natural e expressiva.\n\n"
            f"{('Contexto: ' + context[:400]) if context else ''}\n"
            f"Usuário falou: {prompt}"
        )
        res = _call_llm(status["active_provider"], full_prompt, model, temperature=temp, num_ctx=num_ctx, num_predict=num_predict, timeout=timeout)
        return res["thought"]

    # --- MODO FULL (AGENT_CODE): prompt completo com persona/axiomas ---
    try:
        from cortex.specialists.speech_cortex import speech_cortex
        full_system_prompt = speech_cortex.get_persona_prompt(model if model in ["INTERVIEW", "ANALYTICAL", "POETIC", "PEACEFUL"] else None)
        temp = speech_cortex.get_temperature()
        
        full_prompt = (
            f"{full_system_prompt}\n"
            f"Contexto Adicional: {context}\n\n"
            f"Usuário/Percepção: {prompt}"
        )
        
        actual_model = model if model not in ["INTERVIEW", "ANALYTICAL", "POETIC", "PEACEFUL"] else ctx_cfg.get("model", "qwen2.5:3b")
        res = _call_llm(status["active_provider"], full_prompt, actual_model, temperature=temp, num_ctx=num_ctx, num_predict=num_predict, timeout=timeout)
        return res["thought"]
    except Exception as e:
        log_event(f"Falha na integracao SpeechCortex: {str(e)}", "WARN")
        try:
            full_prompt = (
                f"Você é Melanora v20.0. Seja concisa.\n"
                f"Contexto:\n{context}\n\n"
                f"Entrada: {prompt}"
            )
            res = _call_llm(status["active_provider"], full_prompt, model, temperature=temp, num_ctx=num_ctx, num_predict=num_predict, timeout=timeout)
            return res["thought"]
        except Exception as e2:
            log_event(f"Falha na geração de chat local: {str(e2)}", "ERROR")
            return f">> Erro cognitivo: {str(e2)}"

if __name__ == "__main__":
    print(check_local_llm_status())
    # print(local_thought())
