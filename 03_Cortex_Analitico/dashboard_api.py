"""
📡 Melanora Dashboard API (v1.0)
Servidor leve para fornecer dados ao Dashboard Premium.
Integra os arquivos JSON do Córtex com a Interface React.
"""

from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import json
import os
import time
import sys
import io

# Configuração de encoding via ambiente (PYTHONIOENCODING=utf-8) é preferida.
import sys
from pathlib import Path
API_ROOT = Path(__file__).resolve().parent
if str(API_ROOT) not in sys.path: sys.path.append(str(API_ROOT))

import cv2 # Para o stream MJPEG
import numpy as np
import requests
from pathlib import Path
import subprocess
import platform

# Import Watchdog Logic
try:
    from cortex.logic.watchdog_engine import update_heartbeat, check_health
except ImportError:
    def update_heartbeat(n): pass
    def check_health(): return {}

# Import Shared Control Agent (Simbiose)
try:
    from shared_control_agent import SharedControlAgent
    import threading
    shared_agent = SharedControlAgent()
    shared_thread = None
except ImportError:
    SharedControlAgent = None

# Percepção Streams
try:
    import mss
    import pyautogui
    pyautogui.FAILSAFE = False # Importante para controle remoto
    sct = mss.mss()
    MSS_AVAILABLE = True
except ImportError:
    MSS_AVAILABLE = False
    pyautogui = None

VISION_SOURCE = "WEBCAM" # WEBCAM | SCREEN
SENSORS_STATE = {"camera": False, "mic": False} # Sensores desligados por padrão

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app) # Permitir acesso do dashboard (Vite/Static)

@app.route("/")
def serve_index():
    return app.send_static_file("index.html")

# Topologia Neural
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path: sys.path.append(str(ROOT))
from core_topology import NeuralTopology

BASE_DIR = NeuralTopology.get_area_path("COGNITIVE")
CONFIG_DIR = NeuralTopology.get_capacity_path("Config")

def read_json(name):
    path = CONFIG_DIR / f"{name}.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def write_json(name, data):
    path = CONFIG_DIR / f"{name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

@app.before_request
def track_pulse():
    """Registra o rastro de interação do usuário para simbiose de fluxo."""
    update_heartbeat("dashboard_api")
    
    if request.path.startswith("/api/"):
        path = CONFIG_DIR / "user_pulse.json"
        pulse_data = {"pulses": []}
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    pulse_data = json.load(f)
            except: pass
        
        pulse_data["pulses"].append({
            "timestamp": time.time(),
            "method": request.method,
            "endpoint": request.path
        })
        # Manter apenas os últimos 100 pulsos para análise
        pulse_data["pulses"] = pulse_data["pulses"][-100:]
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pulse_data, f, indent=2)

@app.route("/api/state", methods=["GET"])
def get_state():
    # Atualizar o estado de simbiose antes de retornar
    try:
        from cortex.logic.symbiosis_engine import analyze_user_flow
        analyze_user_flow()
    except: pass

    state = read_json("neural_state")
    profile = read_json("machine_profile")
    results = read_json("results_buffer")
    
    # Extrair métricas recentes
    last_res = results.get("last_result")
    if last_res is None: last_res = {}
    
    return jsonify({
        "active": state.get("physical_mind_active", False),
        "intensity": state.get("intensity", "MEDIUM"),
        "frequency": profile.get("profile", {}).get("freq_max_hz", 200),
        "hardware": profile.get("profile", {}).get("cpu", "Unknown"),
        "latency": last_res.get("elapsed_ms", 0),
        "last_status": last_res.get("status", "IDLE"),
        "processed": read_json("task_queue").get("processed", 0),
        "cpu_load": read_json("machine_profile").get("telemetry", {}).get("cpu_usage", 0),
        "symbiotic_mode": state.get("symbiotic_mode", "NORMAL"),
        "cognitive_status": state.get("cognitive_status", "STABLE")
    })

@app.route("/api/specialists", methods=["GET"])
def get_specialists():
    specialists = read_json("specialists_registry")
    return jsonify(specialists)

@app.route("/api/audit", methods=["GET"])
def get_audit():
    audit = read_json("neural_audit")
    return jsonify(audit)

def generate_frames():
    global VISION_SOURCE, SENSORS_STATE
    cap = None
    
    while True:
        # Se a câmera estiver configurada como DESLIGADA, liberamos o hardware
        if not SENSORS_STATE["camera"]:
            if cap is not None:
                cap.release()
                cap = None
            
            # Gerar um frame de "Privacidade Ativa" (Preto com texto)
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "SENSING_SOVEREIGNTY: ACTIVE (OFF)", (50, 240), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 171), 2)
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            time.sleep(1) # Baixa taxa de atualização quando desligado
            continue

        if VISION_SOURCE == "WEBCAM":
            if cap is None or not cap.isOpened():
                cap = cv2.VideoCapture(0)
            success, frame = cap.read()
            if not success:
                time.sleep(0.1)
                continue
        elif VISION_SOURCE == "SCREEN" and MSS_AVAILABLE:
            if cap is not None:
                cap.release()
                cap = None
            
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)
            frame = np.array(sct_img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            success = True
        else:
            time.sleep(0.1)
            continue

        # HUD Dinâmico no Frame
        timestamp = time.strftime("%H:%M:%S")
        label = "OBSERVER: SCREEN" if VISION_SOURCE == "SCREEN" else "EYE: PHYSICAL"
        cv2.putText(frame, f"MELANORA_VISION :: {label} :: {timestamp}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (171, 255, 0), 2)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    if cap is not None:
        cap.release()

@app.route("/api/motor/mouse", methods=["POST"])
def motor_mouse():
    """Executa comandos de mouse (clique, movimento) via PyAutoGUI."""
    if not pyautogui:
        return jsonify({"status": "ERROR", "message": "PyAutoGUI não disponível."}), 501
    
    data = request.json
    action = data.get("action", "click")
    x_pct = data.get("x", 0.5) # 0.0 a 1.0
    y_pct = data.get("y", 0.5)
    
    # Obter resolução real
    width, height = pyautogui.size()
    target_x = int(x_pct * width)
    target_y = int(y_pct * height)
    
    try:
        if action == "move":
            pyautogui.moveTo(target_x, target_y)
        elif action == "click":
            pyautogui.click(target_x, target_y)
        elif action == "right_click":
            pyautogui.rightClick(target_x, target_y)
        elif action == "double_click":
            pyautogui.doubleClick(target_x, target_y)
            
        return jsonify({"status": "OK", "pos": [target_x, target_y]})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route("/api/motor/keyboard", methods=["POST"])
def motor_keyboard():
    """Executa comandos de teclado via PyAutoGUI."""
    if not pyautogui:
        return jsonify({"status": "ERROR", "message": "PyAutoGUI não disponível."}), 501
    
    data = request.json
    text = data.get("text", "")
    key = data.get("key")
    
    try:
        if key:
            pyautogui.press(key)
        elif text:
            pyautogui.write(text)
            
        return jsonify({"status": "OK"})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route("/api/vision/source", methods=["GET", "POST"])
def set_vision_source():
    global VISION_SOURCE
    if request.method == "POST":
        data = request.json
        new_source = data.get("source", "WEBCAM").upper()
        if new_source in ["WEBCAM", "SCREEN"]:
            VISION_SOURCE = new_source
            return jsonify({"status": "OK", "source": VISION_SOURCE})
        return jsonify({"status": "ERROR", "message": "Fonte inválida."}), 400
    return jsonify({"source": VISION_SOURCE})

@app.route("/api/vision/stream")
def vision_stream():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/api/sensors/config", methods=["GET", "POST"])
def sensor_config():
    global SENSORS_STATE
    if request.method == "POST":
        data = request.json
        sensor = data.get("sensor")
        active = data.get("active", False)
        if sensor in SENSORS_STATE:
            SENSORS_STATE[sensor] = active
            return jsonify({"status": "OK", "sensors": SENSORS_STATE})
        return jsonify({"status": "ERROR", "message": "Sensor inválido"}), 400
    return jsonify(SENSORS_STATE)

@app.route("/api/toggle", methods=["POST"])
def toggle_mind():
    state = read_json("neural_state")
    state["physical_mind_active"] = not state.get("physical_mind_active", False)
    write_json("neural_state", state)
    
    # Orquestração física
    if state["physical_mind_active"]:
        # Chamar inicialização via terminal (detalhado) - Usando melanora.py start logic
        subprocess.Popen([sys.executable, str(API_ROOT / "melanora.py"), "start"], creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        # Encerrar
        from melanora import stop_mind
        stop_mind()

    return jsonify({"status": "OK", "active": state["physical_mind_active"]})

@app.route("/api/voice/toggle", methods=["POST"])
def toggle_voice_bridge():
    """Ativa ou desativa a ponte de voz via Bridge."""
    data = request.json or {}
    active = data.get("active", False)
    
    from neural_bridge import direct_execute
    if active:
        result = direct_execute("voice_bridge", "activate_voice_bridge")
    else:
        result = direct_execute("voice_bridge", "deactivate_voice_bridge")
        
    return jsonify(result)

@app.route("/api/intensity", methods=["POST"])
def set_intensity():
    data = request.json
    new_intensity = data.get("intensity", "MEDIUM")
    state = read_json("neural_state")
    state["intensity"] = new_intensity
    write_json("neural_state", state)
    return jsonify({"status": "OK", "intensity": new_intensity})

@app.route("/api/neural/tags", methods=["GET", "POST"])
def neural_tags():
    """Gerencia as Contextual Neural Tags ativas."""
    state = read_json("neural_state")
    active_tags = state.get("active_tags", ["engineering", "science", "gamedev"])
    
    if request.method == "POST":
        data = request.json or {}
        new_tags = data.get("tags")
        if isinstance(new_tags, list):
            state["active_tags"] = new_tags
            write_json("neural_state", state)
            return jsonify({"status": "OK", "active_tags": new_tags})
        return jsonify({"status": "ERROR", "message": "Lista de tags inválida"}), 400
        
    return jsonify({"active_tags": active_tags})

@app.route("/api/execute", methods=["POST"])
def execute_command():
    data = request.json
    module = data.get("module")
    function = data.get("function")
    params = data.get("params", {})
    
    # Importar bridge dinamicamente para evitar lock circular se rodando no mesmo processo
    from neural_bridge import direct_execute
    result = direct_execute(module, function, params)
    return jsonify(result)

@app.route("/api/audition/spectrum", methods=["GET"])
def audition_spectrum():
    """Retorna dados de espectro em tempo real (telemetria rápida)."""
    try:
        from cortex.specialists.audition_engine import capture_audio_sample
        # Amostra ultra-curta para telemetria sem travar a API
        data = capture_audio_sample(source="MIC", duration_s=0.1)
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route("/api/qualia", methods=["GET"])
def get_qualia():
    """Retorna as impressões e padrões solidificados (Qualia Neural)."""
    try:
        from cortex.logic.synthesis_engine import load_qualia
        data = load_qualia()
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route("/api/dreams", methods=["GET"])
def get_dreams():
    """Retorna os snapshots oníricos gerados pelo Motor Onírico."""
    data = read_json("oneiric_snapshots")
    return jsonify(data.get("dreams", []))

# Síntese de Voz (v7.0)
try:
    from cortex.specialists.speech_cortex import speech_cortex
    from cortex.specialists.speech_synthesis import speech_engine
except ImportError:
    speech_cortex = None
    speech_engine = None

@app.route("/api/dialogue/submit", methods=["POST"])
def submit_dialogue():
    """Recebe entradas multi-modais e as orquestra para extração de prompt."""
    data = request.json
    text = data.get("text", "")
    audio_meta = data.get("audio_metadata", {})
    vision_meta = data.get("vision_metadata", {})
    
    from cortex.specialists.dialogue_orchestrator import extract_unified_prompt
    result = extract_unified_prompt(text, audio_meta, vision_meta)
    
    if result["status"] == "OK":
        # Salvar no estado neural
        state = read_json("neural_state")
        state["last_dialogue_intent"] = result["intent"]
        write_json("neural_state", state)
        
        # Persistir no histórico
        history_path = CONFIG_DIR / "dialogue_history.json"
        history = {"entries": []}
        if history_path.exists():
            try:
                with open(history_path, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except: pass
        
        history["entries"].append({
            "timestamp": time.time(),
            "user_text": text,
            "intent": result["intent"],
            "sensors": {
                "audio": audio_meta.get("active", False),
                "vision": vision_meta.get("active", False)
            }
        })
        # Manter apenas as últimas 50 interações
        history["entries"] = history["entries"][-50:]
        
        try:
            with open(history_path, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=2)
        except: pass
            
        # 3. Disparar Voz se Mic estiver ativo (v7.0)
        if (audio_meta.get("active") or SENSORS_STATE["mic"]) and speech_cortex and speech_engine:
            def speak_async():
                try:
                    ai_text = result["intent"]["ai_response"]
                    pulses = speech_cortex.encode_prosody(ai_text)
                    speech_engine.speak_with_prosody(pulses)
                except Exception as e:
                    print(f"Speech Loop Error: {e}")
            
            import threading
            threading.Thread(target=speak_async, daemon=True).start()
            
    return jsonify(result)

@app.route("/api/dialogue/history", methods=["GET"])
def get_dialogue_history():
    """Retorna o histórico persistente de interações."""
    history = read_json("dialogue_history")
    return jsonify(history.get("entries", []))

@app.route("/api/memory/graph", methods=["GET"])
def get_memory_graph():
    """Gera o grafo estrela em tempo real baseado nos markdowns teóricos e Áreas."""
    nodes = [{"id": "MELANORA_CORE", "group": 0, "size": 40, "label": "Melanora"}]
    links = []
    
    # Adicionar Áreas Topológicas principais
    areas_principais = ["00_Mente_Teorica", "01_Ambientes_Ferramentas", "02_Oficios_Especialidades", "03_Cortex_Analitico", "04_Ambientes_Experimento"]
    for area in areas_principais:
        nodes.append({"id": area, "group": 1, "size": 25, "label": area.split("_", 1)[-1]})
        links.append({"source": "MELANORA_CORE", "target": area, "value": 3})
        
    # Explorar a Mente Teórica para os Nodos de Memória (Documentos)
    try:
        from core_topology import NeuralTopology
        mente_teorica = NeuralTopology.get_area_path("THEORETICAL")
        if mente_teorica and mente_teorica.exists():
            for root, dirs, files in os.walk(mente_teorica):
                folder_name = os.path.basename(root)
                # Ignorar histórico e raízes
                if folder_name.startswith("_") or folder_name == "00_Mente_Teorica":
                    continue
                
                # O nodo da pasta liga à Mente Teórica
                pasta_id = f"dir_{folder_name}"
                nodes.append({"id": pasta_id, "group": 2, "size": 15, "label": folder_name.split("_", 1)[-1][:15]})
                links.append({"source": "00_Mente_Teorica", "target": pasta_id, "value": 2})
                
                # Os arquivos na pasta ligam à pasta
                for file in files:
                    if file.endswith(".md"):
                        file_id = f"doc_{file}"
                        nodes.append({"id": file_id, "group": 3, "size": 10, "label": file.replace(".md", "")[:12]})
                        links.append({"source": pasta_id, "target": file_id, "value": 1})
    except Exception as e:
        print(f"Error generating graph: {e}")
        
    return jsonify({"nodes": nodes, "links": links})

@app.route("/api/neural/connectome", methods=["GET"])
def get_connectome():
    """Legado para views puras."""
    graph = read_json("connectome_graph")
    return jsonify(graph)

@app.route("/api/health", methods=["GET"])
def get_health():
    """Retorna o status de saúde do sistema via Watchdog."""
    return jsonify(check_health())

@app.route("/api/dialogue/intent", methods=["GET"])
def get_dialogue_intent():
    """Retorna a última intenção extraída e processada."""
    state = read_json("neural_state")
    return jsonify(state.get("last_dialogue_intent", {}))

@app.route("/api/haptic", methods=["GET"])
def get_haptic():
    """Retorna a saúde arquitetônica e entropia do código."""
    try:
        from cortex.specialists.haptic_engine import get_haptic_state
        data = get_haptic_state()
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route("/api/memory/search", methods=["GET"])
def search_memory():
    """Busca conceitos e documentos na memória semântica."""
    query = request.args.get("q", "")
    try:
        from cortex.logic.semantic_memory import get_semantic_engine
        engine = get_semantic_engine()
        results = engine.search(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route("/api/homeostasis", methods=["GET"])
def get_homeostasis():
    """Retorna o estado de equilíbrio interno e ações ambientais."""
    try:
        from cortex.logic.homeostasis_engine import run_homeostasis_check
        data = run_homeostasis_check()
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route("/api/neural/system2/analytics", methods=["GET"])
def get_system2_analytics():
    """Retorna a análise matemática e topológica do Sistema 2."""
    try:
        from cortex.system_2.analyst import perform_topological_analysis
        data = perform_topological_analysis()
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

# --- Phase 11: Neural Tool Studio Endpoints ---

@app.route("/api/neural/tools", methods=["GET"])
def list_neural_tools():
    from cortex.specialists.neural_tool_manager import manage_neural_tool
    return jsonify(manage_neural_tool(action="list"))

@app.route("/api/neural/tools", methods=["POST"])
def create_neural_tool():
    from cortex.specialists.neural_tool_manager import manage_neural_tool
    config = request.json
    return jsonify(manage_neural_tool(action="create", config=config))

@app.route("/api/neural/tools/<tool_id>", methods=["PUT"])
def update_neural_tool(tool_id):
    from cortex.specialists.neural_tool_manager import manage_neural_tool
    config = request.json
    return jsonify(manage_neural_tool(action="update", tool_id=tool_id, config=config))

@app.route("/api/neural/tools/<tool_id>", methods=["DELETE"])
def delete_neural_tool(tool_id):
    from cortex.specialists.neural_tool_manager import manage_neural_tool
    return jsonify(manage_neural_tool(action="delete", tool_id=tool_id))

@app.route("/api/neural/tools/scan", methods=["POST"])
def scan_neural_tool():
    from cortex.specialists.neural_tool_manager import run_neural_tool_scan
    data = request.json or {}
    tool_id = data.get("tool_id")
    sample_data = data.get("sample_data")
    return jsonify(run_neural_tool_scan(tool_id=tool_id, sample_data=sample_data))

@app.route("/api/neural/system2/audit", methods=["POST"])
def run_system2_night_audit():
    """Roda a rotina de manutenção noturna do Sistema 2 (Pruning)."""
    try:
        from cortex.system_2.night_auditor import run_night_audit
        data = run_night_audit()
        return jsonify(data)
    except Exception as e:
        import traceback
        print(f"API_ERROR [Audit]: {e}")
        traceback.print_exc()
        return jsonify({"status": "MOCK", "message": "Auditoria em modo de segurança (LLM Offline)."}), 200

@app.route("/api/neural/deep_thought", methods=["POST"])
def trigger_deep_thought():
    """Aciona o Arquiteto Profundo para multi-agent CoT."""
    data = request.json or {}
    user_prompt = data.get("prompt", "")
    try:
        from cortex.system_2.deep_architect import process_deep_thought
        result = process_deep_thought(user_prompt)
        
        # Save to history for UI to render
        history_path = CONFIG_DIR / "dialogue_history.json"
        history = {"entries": []}
        if history_path.exists():
            try:
                with open(history_path, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except: pass
            
        history["entries"].append({
            "timestamp": time.time(),
            "user_text": f"[DEEP THOUGHT] {user_prompt}",
            "intent": {
                "ai_response": result["final_output"],
                "final_prompt": "System 2: Architectural Debate Concluded."
            },
            "sensors": {"audio": False, "vision": False}
        })
        history["entries"] = history["entries"][-50:]
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

        return jsonify(result)
    except Exception as e:
        import traceback
        print(f"API_ERROR [DeepThought]: {e}")
        traceback.print_exc()
        # Fallback de atualização de estado para o frontend saber que falhou cognitivamente
        state = read_json("neural_state")
        state["cognitive_status"] = "FALLBACK"
        write_json("neural_state", state)
        
        return jsonify({
            "status": "MOCK", 
            "final_output": "[Deep Architect] Conexão com o Motor Cognitivo interrompida. O Arquiteto está operando em modo de rascunho estático.",
            "thought_process": {"draft": "Offline", "critique": "Offline"}
        }), 200





# --- Master Control & LLM Endpoints ---
@app.route("/api/sys/clean", methods=["POST"])
def sys_clean():
    """Limpa arquivos temporários e memória volátil (Córtex de curto prazo)."""
    write_json("task_queue", {"pending": [], "processed": 0})
    write_json("results_buffer", {"pending": []})
    # Só limpa o diálogo pra não apagar insights valiosos
    write_json("dialogue_history", {"entries": []})
    return jsonify({"status": "OK", "message": "Memória efêmera purgada."})

@app.route("/api/sys/power", methods=["POST"])
def sys_power():
    """Desliga a Mente Física (Isso vai matar a própria API web e a Bridge)."""
    data = request.json or {}
    action = data.get("action", "STOP")
    if action == "STOP":
        # Aciona o bat em background com sleep de 1s para dar tempo de retornar resposta 200
        cmd = f"Start-Sleep -s 1; cd '{str(ROOT)}'; ./MELANORA_HUB_V5.bat --stop"
        subprocess.Popen(["powershell", "-c", cmd], creationflags=subprocess.CREATE_NEW_CONSOLE)
        return jsonify({"status": "OK", "message": "Protocolo de Repouso Absoluto iniciado."})
    return jsonify({"status": "ERROR", "message": "Ação desconhecida"}), 400

@app.route("/api/llm/status", methods=["GET"])
def get_llm_status():
    """Inspeciona o motor Ollama local."""
    try:
        proc = subprocess.run(["powershell", "-c", "(Get-Process -Name ollama -ErrorAction SilentlyContinue).Name"], capture_output=True, text=True)
        if "ollama" in proc.stdout.strip().lower():
            try:
                # Buscar qual modelo está carregado na RAM
                m_proc = subprocess.run(["ollama", "ps"], capture_output=True, text=True)
                active = [line.split()[0] for line in m_proc.stdout.split("\n")[1:] if line.strip()]
                return jsonify({"status": "ONLINE", "active_models": active})
            except:
                return jsonify({"status": "ONLINE", "active_models": []})
        return jsonify({"status": "OFFLINE", "active_models": []})
    except:
        return jsonify({"status": "ERROR", "active_models": []})

@app.route("/api/llm/models", methods=["GET"])
def get_llm_models():
    """Retorna as opções de LLM instaladas localmente para o seletor."""
    try:
        proc = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        # Ex: "llama3:latest  a6990ed6be41  4.7 GB  4 weeks ago"
        lines = proc.stdout.split("\n")[1:]
        models = [line.split()[0] for line in lines if line.strip()]
        return jsonify({"status": "OK", "models": models})
    except Exception as e:
        return jsonify({"status": "ERROR", "models": [], "message": str(e)})

@app.route("/api/llm/control", methods=["POST"])
def control_llm():
    """Inicia ou desliga o motor Ollama via interface."""
    data = request.json or {}
    action = data.get("action", "START")
    
    if action == "START":
        subprocess.Popen(["ollama", "serve"], creationflags=subprocess.CREATE_NEW_CONSOLE)
        return jsonify({"status": "OK", "message": "Ignição do Motor LLM iniciada."})
    elif action == "STOP":
        subprocess.run(["powershell", "-c", "Stop-Process -Name ollama -Force -ErrorAction SilentlyContinue"])
        return jsonify({"status": "OK", "message": "Motor LLM derrubado."})
    
    return jsonify({"status": "ERROR", "message": "Ação LLM desconhecida"}), 400

# --- Shared Control Neural Sync Endpoints ---

def run_shared_loop():
    global shared_agent
    if shared_agent:
        shared_agent.perception_loop()

@app.route("/api/shared_control/toggle", methods=["POST"])
def toggle_shared_sync():
    global shared_agent, shared_thread
    if not shared_agent:
        return jsonify({"status": "ERROR", "message": "Shared Control Agent not available"}), 501
    
    if shared_agent.active:
        shared_agent.stop_sync()
        if shared_thread:
            shared_thread.join(timeout=1)
            shared_thread = None
    else:
        shared_agent.active = True
        shared_thread = threading.Thread(target=run_shared_loop, daemon=True)
        shared_thread.start()
        print("SHARED_CONTROL_SYNC: ACTIVE")
        
    return jsonify({
        "status": "OK", 
        "active": shared_agent.active,
        "fps": sum(shared_agent.fps_log)/len(shared_agent.fps_log) if shared_agent.fps_log else 0
    })

@app.route("/api/shared_control/status", methods=["GET"])
def get_shared_status():
    global shared_agent
    if not shared_agent:
        return jsonify({"active": False, "available": False})
    
    return jsonify({
        "active": shared_agent.active,
        "available": True,
        "fps": round(sum(shared_agent.fps_log)/len(shared_agent.fps_log), 1) if shared_agent.fps_log else 0,
        "region": shared_agent.region,
        "focus": shared_agent.focus_region
    })

@app.route("/api/shared_control/focus", methods=["POST"])
def set_neural_focus():
    global shared_agent
    if not shared_agent: return jsonify({"status": "ERROR"}), 501
    data = request.json
    shared_agent.set_focus(data['top'], data['left'], data['width'], data['height'])
    return jsonify({"status": "OK", "focus": shared_agent.focus_region})

@app.route("/api/neural/inference_status", methods=["GET"])
def get_inference_status():
    """Retorna o status da LLM local via neural_bridge."""
    try:
        from neural_bridge import direct_execute
        res = direct_execute("neural_inference", "check_local_llm_status")
        return jsonify(res.get("result", {"ollama": False, "lm_studio": False}))
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route("/api/neural/models", methods=["GET"])
def get_neural_models():
    """Retorna os modelos locais disponíveis via Ollama e o ativo atual."""
    state = read_json("neural_state")
    active_model = state.get("active_llm_model", "qwen2.5:3b")
    models = ["qwen2.5:3b", "phi3:mini", "gemma2:2b"] # Fallback otimizado para 12GB RAM

    try:
        res = requests.get("http://localhost:11434/api/tags", timeout=1)
        if res.status_code == 200:
            models = [m["name"].split(":")[0] for m in res.json().get("models", [])]
    except Exception:
        pass # Mantém fallback se offline

    return jsonify({"status": "OK", "models": list(set(models)), "active": active_model})

@app.route("/api/neural/start", methods=["POST"])
def start_neural_engine():
    """Tenta iniciar o motor LLM localmente via subprocesso (Ollama)."""
    data = request.json or {}
    model = data.get("model", "qwen2.5:3b")
    
    # Salva qual modelo foi escolhido no estado neural
    state = read_json("neural_state")
    state["active_llm_model"] = model
    write_json("neural_state", state)

    try:
        if platform.system() == "Windows":
            # Rodar oculto no Windows sem prender o terminal do Python
            DETACHED_PROCESS = 0x00000008
            subprocess.Popen(["ollama", "run", model], creationflags=DETACHED_PROCESS)
        else:
            subprocess.Popen(["ollama", "run", model], start_new_session=True)
            
        return jsonify({"status": "OK", "message": f"Iniciando ignição no modelo {model}..."})
    except Exception as e:
        return jsonify({"status": "ERROR", "message": f"Falha na ignição: {str(e)}"}), 500

@app.route("/api/neural/intuition", methods=["GET"])
def get_neural_intuition():
    """Retorna uma fagulha sintética ultrarrápida do ambiente usando Sistema 1."""
    try:
        from cortex.logic.cortex_reflexo import generate_quick_intuition
        res = generate_quick_intuition()
        return jsonify(res)
    except Exception as e:
        return jsonify({"status": "ERROR", "intuition": "..."}), 500

@app.route("/api/sensors/vision_telemetry", methods=["POST"])
def receive_vision_telemetry():
    """Recebe telemetria visual simbólica de ambientes (ex: Snake Game) e injeta no pulso."""
    data = request.json or {}
    
    pulse_file = CONFIG_DIR / "user_pulse.json"
    pulse_state = {"pulses": []}
    if pulse_file.exists():
        try:
            pulse_state = read_json("user_pulse")
        except:
            pass
            
    # Cria uma simulação de "Atividade detectada na tela"
    event_desc = f"VISÃO: {data.get('source', 'Unknown')} - {data.get('action', '')}. Detalhes: {data.get('details', '')}"
    
    pulse_state["pulses"].append({
        "timestamp": time.time(),
        "type": "VISION_SYM",
        "endpoint": event_desc
    })
    
    # Mantém apenas os 5 mais recentes
    pulse_state["pulses"] = pulse_state["pulses"][-5:]
    write_json("user_pulse", pulse_state)
    
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    lock_file = CONFIG_DIR / "api.lock"
    if lock_file.exists():
        print("[!] Dashboard API ja em execucao.")
        exit(0)
        
    try:
        lock_file.touch()
        # Tentar rodar na porta 5000
        print("Melanora API Gateway - Online")
        app.run(port=5000, debug=False)
    finally:
        if lock_file.exists():
            try: lock_file.unlink()
            except: pass
