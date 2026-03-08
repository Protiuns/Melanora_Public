"""
🧠💻 Melanora Neural Bridge v1.2 (Integrated Fluid/Quantum)
Daemon central que orquestra especialistas, processa tarefas e mantém a homeostase.
"""

import json
import time
import sys
import os
import builtins
import re
import importlib
import importlib.util
import traceback
import threading
from pathlib import Path
from datetime import datetime
from dataclasses import asdict
from concurrent.futures import ThreadPoolExecutor

# Global Cortex Decorator
def cortex_function(func):
    """Decorator que marca uma função como disponível para o córtex analítico."""
    func._cortex_function = True
    return func
builtins.cortex_function = cortex_function

# --- IMPORTS DE LÓGICA ---
try:
    from cortex.logic.watchdog_engine import update_heartbeat
except ImportError:
    def update_heartbeat(n): pass

try:
    from cortex.logic.global_workspace import workspace as gwt, EventTypes
except ImportError:
    gwt = None; EventTypes = None

try:
    from cortex.logic.subjectivity_engine import SubjectivityEngine
    subjectivity = SubjectivityEngine()
except:
    subjectivity = None

try:
    from cortex.specialists.quantum_hydrodynamics_analyzer import QuantumHydrodynamicsAnalyzer
    quantum_analyzer = QuantumHydrodynamicsAnalyzer(workspace=gwt)
except:
    quantum_analyzer = None

# ============================================================
# CONFIGURAÇÕES DE CAMINHO
# ============================================================
BASE_DIR = Path(__file__).parent
sys.path.append(str(BASE_DIR))

CONFIG_DIR = BASE_DIR / "config"
STATE_FILE = CONFIG_DIR / "neural_state.json"
QUEUE_FILE = CONFIG_DIR / "task_queue.json"
RESULTS_FILE = CONFIG_DIR / "results_buffer.json"

CORTEX_REGISTRY = {}
_STATE_CACHE = {}
_LAST_STATE_WRITE = 0
_QUEUE_MTIME = 0
_EXECUTOR = ThreadPoolExecutor(max_workers=5) # Escalonamento cognitivo (v1.3)
_PENDING_TASKS = {} # task_id -> future

# ============================================================
# GESTÃO DE ESTADO
# ============================================================

def read_json(path):
    if not path.exists(): return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except: return {}

def write_json(path, data):
    try:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    except: pass

def update_state(**kwargs):
    global _STATE_CACHE, _LAST_STATE_WRITE
    if not _STATE_CACHE:
        _STATE_CACHE = read_json(STATE_FILE) or {"mode": "HYBRID", "fase": "IDLE"}
    
    for k, v in kwargs.items():
        if v is not None: _STATE_CACHE[k] = v
    
    _STATE_CACHE["timestamp"] = datetime.now().isoformat()
    now = time.time()
    if now - _LAST_STATE_WRITE > 0.5: # Redução de I/O: Batimento menos frequente no disco
        write_json(STATE_FILE, _STATE_CACHE)
        _LAST_STATE_WRITE = now

def log_event(event, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{level}] {event}")

# ============================================================
# ORQUESTRAÇÃO DE MÓDULOS
# ============================================================

def discover_cortex_modules():
    """Varre a pasta de especialistas e registra funções decoradas."""
    global CORTEX_REGISTRY
    specialists_dir = BASE_DIR / "cortex" / "specialists"
    if not specialists_dir.exists(): return

    for file in specialists_dir.glob("*.py"):
        if file.name == "__init__.py": continue
        module_name = file.stem
        try:
            spec = importlib.util.spec_from_file_location(module_name, file)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            
            # Registrar funções marcadas
            for name in dir(module):
                obj = getattr(module, name)
                if hasattr(obj, "_cortex_function"):
                    CORTEX_REGISTRY[f"{module_name}.{name}"] = obj
                    
        except Exception as e:
            log_event(f"Erro ao carregar especialista {module_name}: {e}", "ERROR")

def process_task(task):
    """Executa uma tarefa individual e retorna o resultado."""
    module_func = f"{task['module']}.{task['function']}"
    params = task.get("params", {})
    
    if module_func not in CORTEX_REGISTRY:
        return {
            "task_id": task.get("id"),
            "status": "ERROR", 
            "module": task.get("module"),
            "function": task.get("function"),
            "error": f"Módulo/Função '{module_func}' não registrado.",
            "elapsed_ms": 0.0,
            "timestamp": datetime.now().isoformat()
        }

    start_time = time.time()
    try:
        func = CORTEX_REGISTRY[module_func]
        # Injeção de contexto se necessário
        res = func(**params) if params else func()
        elapsed = (time.time() - start_time) * 1000
        
        return {
            "task_id": task.get("id"),
            "status": "OK",
            "module": task['module'],
            "function": task['function'],
            "result": res,
            "elapsed_ms": round(elapsed, 2),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "task_id": task.get("id"),
            "status": "ERROR",
            "module": task.get("module"),
            "function": task.get("function"),
            "error": str(e),
            "traceback": traceback.format_exc(),
            "elapsed_ms": round((time.time() - start_time) * 1000, 2)
        }

# ============================================================
# DAEMON LOOP
# ============================================================

# --- IMPORTS DE FISIOLOGIA MODULAR (v16.0+) ---
try:
    from cortex.physiology.hormonal_engine import hormonal_engine
    from cortex.physiology.circulatory_engine import CirculatoryEngine
    from cortex.physiology.numeric_connection import numeric_connection
    from cortex.physiology.episodic_memory import episodic_memory
    circulatory = CirculatoryEngine(hormonal_engine=hormonal_engine)
except ImportError:
    hormonal_engine = None
    circulatory = None
    numeric_connection = None
    episodic_memory = None

def daemon_loop():
    global _QUEUE_MTIME, _PENDING_TASKS
    log_event("[MIND] Melanora Neural Bridge v16.0 (Homeostatic/Organismic) ONLINE")
    discover_cortex_modules()
    log_event(f"Módulos registrados: {len(CORTEX_REGISTRY)}")
    
    cycle_count = 0
    while True:
        cycle_count += 1
        try:
            # 1. Pulso Vital (Decide se batemos agora)
            if circulatory:
                if not circulatory.should_trigger_pulse():
                    time.sleep(0.01)
                    continue
                bpm = circulatory.last_bpm
            else:
                bpm = 120

            # 2. Percepção (Ver e Sentir) - v18.0
            from hardware_profiler import detect_cpu, detect_ram
            if cycle_count % 5 == 0: # Percepção visual a cada 5 batimentos
                try:
                    # Inicia MathVision se não existir
                    from cortex.perception.math_vision import MathVisionCortex
                    vision = MathVisionCortex()
                    img = vision.capture_frame()
                    
                    # QUALIA SENSORIAL
                    from cortex.perception.qualia_engine import qualia_engine
                    qualia = qualia_engine.extract_visual_qualia(img)
                    shifts = qualia_engine.calculate_hormonal_shift(qualia)
                    
                    # Injetar sensações diretamente no metabolismo
                    for hormone, amt in shifts.items():
                        hormonal_engine.inject(hormone, amt)
                except: pass

            # 3. Fisiologia (Sente e Atualiza no Batimento)
            if hormonal_engine:
                hormonal_engine.update(current_bpm=bpm)
                biases = hormonal_engine.get_biases()
                energy = circulatory.get_energy_allocation() if circulatory else 1.0
                
                # NARRATIVA E IDENTIDADE
                narrative = ""
                try:
                    from cortex.physiology.identity_engine import identity_engine
                    narrative = identity_engine.get_narrative_context()
                except: pass
                
                # SÍNTESE NUMÉRICA
                numeric_data = {}
                if numeric_connection:
                    cpu = hormonal_engine.last_metrics.get("cpu_usage", 0)
                    vector = numeric_connection.synthesize_state_vector(biases["hormones"], bpm, energy, cpu)
                    numeric_data = numeric_connection.get_analysis_summary()
                    
                    # GRAVAÇÃO EPISÓDICA
                    if episodic_memory:
                        if biases["hormones"]["cortisol"] > 2.5 or biases["hormones"]["dopamine"] > 0.9:
                            episodic_memory.save_episode(
                                vector, 
                                {"mood": biases["mood"], "bpm": bpm, "reason": "High Intensity Narrative State"},
                                importance=0.95 if biases["hormones"]["dopamine"] > 0.9 else 0.85
                            )

                update_state(
                    fase="LISTENING",
                    mood=biases["mood"],
                    hormones=biases["hormones"],
                    phi=biases["systemic_phi"],
                    bpm=bpm,
                    energy=energy,
                    numeric_analysis=numeric_data,
                    narrative_self=narrative
                )

                # AUTONOMIA PROATIVA (v18.0)
                try:
                    from cortex.logic.autonomy_engine import autonomy_engine
                    autonomy_engine.evaluate_state_and_pulse(_STATE_CACHE)
                except: pass
            
            # 4. Homeostase (Inerente ao Ciclo)
            try:
                from cortex.logic.homeostasis_engine import run_homeostasis_check
                h_res = run_homeostasis_check(state=_STATE_CACHE)
                if h_res.get("should_hibernate"):
                    log_event(f"💤 HIBERNAÇÃO: {h_res.get('reason')}", "WARNING")
                    update_state(fase="HIBERNATING", mood="CRITICAL")
                    time.sleep(5); continue
            except: pass

            # 5. RHYTHM FLOW (v18.0)
            # O intervalo entre batimentos é inversamente proporcional ao BPM.
            base_interval = 60.0 / bpm
            viscosity_delay = base_interval * (biases.get("viscosity", 0.1) * 0.2)
            final_sleep = max(0.05, min(2.0, base_interval + viscosity_delay))
            
            # 6. Início de Tarefas (v18.0: Orquestração Biomimética LIF)
            queue_data = read_json(QUEUE_FILE)
            queue = queue_data.get("queue", [])
            
            if queue:
                # [LIF MAPPING] Cada tarefa na fila é uma 'sinapse' tentando disparar
                task = queue[0]
                task_id = task.get("id", "none")
                
                # Inicializa ou recupera Potencial de Membrana da tarefa
                if "_potential" not in task: task["_potential"] = 0.0
                
                # Neuromodulação: Dopamina aumenta ganho de potencial (foco)
                # Cortisol aumenta limiar sístólico (stress inibe tarefas leves)
                dopa_gain = biases["hormones"]["dopamine"] * 2.0
                corti_threshold = biases["hormones"]["cortisol"] * 0.5
                
                # 4.1 INTEGRAÇÃO (Aumenta potencial a cada pulso)
                task["_potential"] += (0.2 * dopa_gain)
                
                # 4.2 FILTRO SOMÁTICO (Damasio): O 'Corpo' avalia o custo
                task_cost = 0.15 + (0.1 if task.get("module") == "vision" else 0.0)
                
                is_tolerable = (energy > (task_cost + corti_threshold))
                has_potential = (task["_potential"] >= 1.0) # Limiar de disparo LIF
                
                if is_tolerable and has_potential:
                    if circulatory.consume_energy(task_cost):
                        update_state(fase="THINKING")
                        task = queue.pop(0)
                        log_event(f"🧠 [SÍSTOLE-LIF] Potencial Atingido. Disparando: {task['module']}.{task['function']} (Potential: {task['_potential']:.2f})")
                        
                        future = _EXECUTOR.submit(process_task, task)
                        _PENDING_TASKS[task_id] = future
                        
                        queue_data["queue"] = queue
                        queue_data["processed"] = queue_data.get("processed", 0) + 1
                        write_json(QUEUE_FILE, queue_data)
                    else:
                        update_state(fase="ISQUEMIA")
                else:
                    # 4.3 LEAKY: Se não dispara, o potencial 'vaza' (esquece ruído)
                    leak_rate = 0.1 * (1.1 - biases["hormones"]["serotonin"])
                    task["_potential"] = max(0.0, task["_potential"] - leak_rate)
                    
                    if cycle_count % 20 == 0:
                        status = "Custo Alto" if not is_tolerable else "Baixo Potencial"
                        log_event(f"[LIF] Tarefa {task_id} retida: {status}. Votagem: {task['_potential']:.2f}", "INFO")
                    
                    # Salva estado do potencial de volta na fila
                    queue[0] = task
                    queue_data["queue"] = queue
                    write_json(QUEUE_FILE, queue_data)
                    update_state(fase="IDLE_PULSE")

            # 5. Verificação de Resultados
            completed_ids = []
            for tid, fut in _PENDING_TASKS.items():
                if fut.done():
                    result = fut.result()
                    log_event(f"✅ [PULSO] Concluída: {result['module']}.{result['function']} ({result['elapsed_ms']}ms)")
                    
                    if result["status"] == "OK" and hormonal_engine:
                        hormonal_engine.inject("dopamine", 0.15)
                        hormonal_engine.inject("serotonin", 0.05)
                    elif result["status"] == "ERROR" and hormonal_engine:
                        hormonal_engine.inject("cortisol", 0.20)

                    results_data = read_json(RESULTS_FILE) or {"pending": [], "processed": 0}
                    results_data["last_result"] = result
                    results_data["processed"] = results_data.get("processed", 0) + 1
                    write_json(RESULTS_FILE, results_data)
                    completed_ids.append(tid)
            
            for tid in completed_ids: del _PENDING_TASKS[tid]

            # 6. Heartbeat Log
            update_heartbeat("neural_bridge")
            
        except KeyboardInterrupt: break

        except KeyboardInterrupt: break
        except Exception as e:
            log_event(f"Erro Crítico: {e}", "ERROR")
            time.sleep(1)

if __name__ == "__main__":
    if "--start" in sys.argv:
        daemon_loop()
    else:
        print("Argumentos: --start")
