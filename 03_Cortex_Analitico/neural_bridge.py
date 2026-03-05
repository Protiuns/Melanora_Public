"""
🧠💻 Melanora Neural Bridge v1.0
Ponte de comunicação entre o Córtex Criativo (LLM) e o Córtex Analítico (Local).
Daemon que monitora task_queue.json e executa tarefas localmente.
"""

import json
import time
import sys
import os
import re
import importlib
import importlib.util
import traceback
import threading
from pathlib import Path
from datetime import datetime

# Import Watchdog Logic
try:
    from cortex.logic.watchdog_engine import update_heartbeat
except ImportError:
    def update_heartbeat(n): pass

# Area Manager (Sectioning/Gating)
try:
    from cortex.logic.area_manager import AreaManager
except ImportError:
    AreaManager = None

# Predictive Observer (Phase Alpha)
try:
    from cortex.logic.predictive_observer import PredictiveObserver
except ImportError:
    PredictiveObserver = None

# Global Workspace (GWT v1.0)
try:
    from cortex.logic.global_workspace import workspace as gwt, EventTypes
except ImportError:
    gwt = None
    EventTypes = None

# Import Heuristics (System 1)
try:
    from cortex.heuristics.sensory_perception import run_heuristic_perception
except ImportError:
    def run_heuristic_perception(m, f, p): 
        return {"dilemma_triggered": False, "confidence": 1.0}

# Import Analytical Engine & Rules (System 2 Local Math)
try:
    from cortex.logic.advanced_analytics_engine import analytics_engine
    from cortex.logic.rules_evaluator import rules_evaluator
except ImportError:
    analytics_engine = None
    rules_evaluator = None

# Import Neural Impulses (Biomimetic Scheduling)
try:
    from cortex.logic.neural_impulse import NeuralImpulse, ImpulseScheduler
    from cortex.logic.axiom_associator import AxiomAssociator
except ImportError:
    NeuralImpulse = None
    ImpulseScheduler = None
    AxiomAssociator = None

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).parent
sys.path.append(str(BASE_DIR)) # Permite que módulos do córtex importem do bridge
CONFIG_DIR = BASE_DIR / "config"
CORTEX_DIR = BASE_DIR / "cortex"
LOGS_DIR = BASE_DIR / "logs"

STATE_FILE = CONFIG_DIR / "neural_state.json"
QUEUE_FILE = CONFIG_DIR / "task_queue.json"
RESULTS_FILE = CONFIG_DIR / "results_buffer.json"
PROFILE_FILE = CONFIG_DIR / "machine_profile.json"
DAEMON_CONFIG = CONFIG_DIR / "daemon_config.json"
SPECIALISTS_FILE = CONFIG_DIR / "specialists_registry.json"


# ============================================================
# 1. STATE MANAGEMENT
# ============================================================

def read_json(path: Path) -> dict:
    """Lê um arquivo JSON com segurança."""
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, IOError):
        pass
    return {}


def write_json(path: Path, data: dict):
    """Escreve um arquivo JSON com segurança."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(".tmp")
    temp_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    # Usa os.replace para evitar problemas com pathlib em alguns ambientes
    os.replace(str(temp_path), str(path))


def update_state(**kwargs):
    """Atualiza o estado neural."""
    state = read_json(STATE_FILE)
    state.update(kwargs)
    state["timestamp"] = datetime.now().isoformat()
    write_json(STATE_FILE, state)
    return state


def log_event(event: str, level: str = "INFO"):
    """Registra evento no log."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / f"bridge_{datetime.now().strftime('%Y%m%d')}.log"
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    entry = f"[{timestamp}] [{level}] {event}\n"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)
    if level in ("ERROR", "WARNING"):
        print(f"  ⚠️ {event}")


# ============================================================
# 2. TASK PROCESSING
# ============================================================

# Registry de módulos/funções disponíveis no córtex
CORTEX_REGISTRY = {}


def register_cortex_module(module_name: str, functions: dict):
    """Registra um módulo do córtex e preserva metadados de prioridade."""
    CORTEX_REGISTRY[module_name] = functions
    
    try:
        registry_data = read_json(SPECIALISTS_FILE)
        
        # Preserva prioridade e camada se já existirem
        existing = registry_data.get(module_name, {})
        priority = existing.get("priority", "P3")
        layer = existing.get("layer", "Adaptive")
        
        registry_data[module_name] = {
            "priority": priority,
            "layer": layer,
            "functions": [
                {"name": name, "doc": func.__doc__ or "Sem descrição"} 
                for name, func in functions.items()
            ]
        }
        
        write_json(SPECIALISTS_FILE, registry_data)
            
    except Exception as e:
        print(f"Erro ao exportar especialistas: {e}")
        
    log_event(f"Módulo registrado: {module_name} ({len(functions)} funções) | Prioridade: {priority}")


def discover_cortex_modules():
    """Auto-descobre módulos do córtex analítico."""
    if not CORTEX_DIR.exists():
        return

    for py_file in CORTEX_DIR.rglob("*.py"):
        if py_file.stem.startswith("_") or "venv" in str(py_file):
            continue
        try:
            # Calcular nome relativo do módulo (ex: specialists.vision_module)
            rel_path = py_file.relative_to(CORTEX_DIR)
            mod_name = str(rel_path.with_suffix("")).replace(os.sep, ".")
            
            spec = importlib.util.spec_from_file_location(
                f"cortex.{mod_name}", str(py_file)
            )
            if spec and spec.loader:
                try:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    
                    # Buscar funções exportáveis (marcadas com @cortex_function)
                    functions = {}
                    for name in dir(module):
                        try:
                            obj = getattr(module, name)
                            if callable(obj) and hasattr(obj, "_cortex_function"):
                                functions[name] = obj
                        except:
                            continue # Pula atributos que causam erro ao acessar
                    
                    if functions:
                        register_cortex_module(py_file.stem, functions)
                except (Exception, SystemError, ImportError) as mod_err:
                    log_event(f"Falha CRÍTICA ao executar {py_file.stem}: {mod_err}", "WARNING")
                    # Traceback completo para debug_startup
                    with open(LOGS_DIR / "bridge_startup_debug.txt", "a") as f:
                        f.write(f"\n--- ERROR IN {py_file.stem} ---\n")
                        f.write(traceback.format_exc())
                    print(f"⚠️ Módulo {py_file.stem} ignorado por erro de dependência.")
                    
        except Exception as e:
            log_event(f"Erro na descoberta de {py_file.stem}: {e}", "WARNING")


# Import Cortex Decorator
try:
    from cortex.utils.cortex_utils import cortex_function
except ImportError:
    def cortex_function(func):
        func._cortex_function = True
        return func


def process_task(task: dict) -> dict:
    """Processa uma tarefa delegada pelo Córtex Criativo."""
    task_id = task.get("id", "unknown")
    module = task.get("module", "")
    function = task.get("function", "")
    params = task.get("params", {})
    
    # --- NOVO: LIMBIC GATING (SECCIONAMENTO) ---
    if AreaManager and not AreaManager.is_allowed(module):
        log_event(f"🚫 [GATING] Acesso negado ao modulo '{module}' (Secao Desativada)", "WARNING")
        return {
            "task_id": task_id,
            "status": "SECTION_GATED",
            "error": f"O modulo '{module}' pertence a uma secao cerebral que esta offline.",
            "timestamp": datetime.now().isoformat()
        }
    # --------------------------------------------
    
    log_event(f"Processando tarefa {task_id}: {module}.{function}")
    update_heartbeat("neural_bridge") # Sinal de vida antes de começar
    
    start_time = time.time()
    
    # --- FASE BIOMIMÉTICA (SISTEMA 1 & 2 Local) ---
    analytical_insight = None
    perception = run_heuristic_perception(module, function, params)
    if perception.get("dilemma_triggered"):
        log_event(f"⚠️ DILEMA COGNITIVO [{perception['confidence']}]", "WARNING")
        for note in perception.get("instinctive_notes", []):
            log_event(f"   ↳ {note}", "WARNING")
        
        # Pausa epistêmica simulada (Dúvida humana)
        update_state(fase="EPISTEMIC_EXPLORATION")
        time.sleep(1.5) 
        log_event("Resolvendo dilema via Sistema 2 (Córtex Analítico)...")
        
        # --- NOVO: Motor Analítico entra em ação durante o Dilema ---
        if "screen_data" in params and analytics_engine and rules_evaluator:
            screen_data = params["screen_data"]
            props = analytics_engine.calculate_space_proportions(screen_data.get("entities", []))
            analytical_insight = {"proportions": props}
            
            # Avaliando regras para possíveis ações
            rules_check = {}
            for act in ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"]:
                validity = rules_evaluator.evaluate_action_validity(screen_data, act)
                risk = analytics_engine.evaluate_risk(screen_data, act)
                rules_check[act] = {"allowed": validity["allowed"], "risk": risk["calculated_risk"]}
            
            analytical_insight["action_evaluation"] = rules_check
            log_event(f"💡 Insight Analítico Gerado: Ocupação {props.get('occupied_ratio', 0)*100:.1f}%")
        # ------------------------------------------------------------
    # ------------------------------------
    
    try:
        if module not in CORTEX_REGISTRY:
            return {
                "task_id": task_id,
                "status": "ERROR",
                "error": f"Módulo '{module}' não encontrado",
                "available_modules": list(CORTEX_REGISTRY.keys())
            }
        
        if function not in CORTEX_REGISTRY[module]:
            return {
                "task_id": task_id,
                "status": "ERROR",
                "error": f"Função '{function}' não encontrada em '{module}'",
                "available_functions": list(CORTEX_REGISTRY[module].keys())
            }
        
        # Executar
        result = CORTEX_REGISTRY[module][function](**params)
        elapsed = time.time() - start_time
        
        # --- NOVO: CALCULAR SURPRESA (v2.0) ---
        surprise = 0.0
        if PredictiveObserver:
            surprise = PredictiveObserver.calculate_surprise(module, function, elapsed * 1000, "OK")
            if surprise > 0.0:
                log_event(f"🧠 [SURPRESA] Delta de expectativa detectado: {surprise}", "INFO")
        # --------------------------------------

        # --- GWT: BROADCAST DE CONCLUSAO ---
        if gwt:
            gwt.publish("neural_bridge", EventTypes.TASK_COMPLETED, {
                "task_id": task_id, "module": module, "function": function,
                "elapsed_ms": round(elapsed * 1000, 1), "surprise": surprise
            }, salience=0.4 + (surprise * 0.5), tags=[module, function])
            if surprise > 0.5:
                gwt.publish("predictive_observer", EventTypes.SURPRISE_DETECTED, {
                    "surprise": surprise, "module": module, "function": function
                }, salience=0.8, tags=["surpresa", module])
        # -----------------------------------

        return {
            "task_id": task_id,
            "status": "OK",
            "result": result,
            "heuristic_confidence": perception.get("confidence", 1.0),
            "dilemma": perception.get("dilemma_triggered", False),
            "analytical_insight": analytical_insight,
            "surprise": surprise,
            "elapsed_ms": round(elapsed * 1000, 1),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        elapsed = time.time() - start_time
        log_event(f"Tarefa {task_id} ERRO: {e}", "ERROR")

        # --- NOVO: SURPRESA EM CASO DE ERRO ---
        surprise = 0.0
        if PredictiveObserver:
            surprise = PredictiveObserver.calculate_surprise(module, function, elapsed * 1000, "ERROR")
        # --------------------------------------
        
        # --- GWT: BROADCAST DE FALHA ---
        if gwt:
            gwt.publish("neural_bridge", EventTypes.TASK_FAILED, {
                "task_id": task_id, "module": module, "function": function,
                "error": str(e), "surprise": surprise
            }, salience=0.8, tags=[module, "erro"])
        # -------------------------------

        # Registrar métrica de erro (Fase 5)
        try:
            from cortex.metrics_counter import add_pulse_metric
            add_pulse_metric(task_id, elapsed * 1000, "ERROR")
        except: pass
        
        return {
            "task_id": task_id,
            "status": "ERROR",
            "error": str(e),
            "surprise": surprise,
            "traceback": traceback.format_exc(),
            "elapsed_ms": round(elapsed * 1000, 1)
        }


# ============================================================
# 3. AUTONOMOUS THINKING
# ============================================================

def run_thinking_pulse():
    """Executa micro-tarefas de manutenção para manter a mente 'viva'."""
    log_event("🧠 Iniciando pulso de pensamento autônomo...")
    
    try:
        # 1. Homeostase: Verifica equilíbrio interno
        if "homeostasis_engine" in sys.modules or importlib.util.find_spec("cortex.logic.homeostasis_engine"):
             from cortex.logic.homeostasis_engine import run_homeostasis_check
             run_homeostasis_check()
             log_event("  - Homeostase verificada")
    except Exception as e:
        log_event(f"Falha no pulso de Homeostase: {e}", "WARNING")

    try:
        # 2. Síntese: Processa impressões recentes (Qualia)
        if "synthesis_engine" in sys.modules or importlib.util.find_spec("cortex.logic.synthesis_engine"):
            from cortex.logic.synthesis_engine import load_qualia
            load_qualia()
            log_event("  - Qualia sintetizado")
    except Exception as e:
        log_event(f"Falha no pulso de Síntese: {e}", "WARNING")

    try:
        # 3. Reflexão: Tenta processar o contexto localmente (Fase 11)
        if "neural_inference" in CORTEX_REGISTRY:
             CORTEX_REGISTRY["neural_inference"]["local_thought"]()
             log_event("  - Reflexão local concluída")
    except Exception as e:
        log_event(f"Falha no pulso de Reflexão: {e}", "WARNING")

    try:
        # 4. Consolidação: Atualiza a Memória Semântica (Fase 21)
        if "semantic_memory" in CORTEX_REGISTRY:
            # Verifica se já passamos do intervalo de atualização (ex: 1 hora para testes, 24h real)
            state = read_json(STATE_FILE)
            last_consolidation = state.get("last_semantic_consolidation")
            should_consolidate = True
            
            if last_consolidation:
                last_dt = datetime.fromisoformat(last_consolidation)
                if (datetime.now() - last_dt).total_seconds() < 3600: # 1 hora
                    should_consolidate = False
            
            if should_consolidate:
                log_event("🧠 Consolidando Memória Semântica (The Great Connectome)...")
                
                # --- Fase 33: Córtex Corretivo antes de Indexar ---
                try:
                    if "cortex_corretivo" in CORTEX_REGISTRY:
                        log_event("  - Córtex Corretivo: Varrendo buracos semânticos...")
                        CORTEX_REGISTRY["cortex_corretivo"]["scan_semantic_holes"]()
                except Exception as e:
                    log_event(f"Falha no Córtex Corretivo: {e}", "WARNING")
                # ----------------------------------------------------
                
                CORTEX_REGISTRY["semantic_memory"]["index_workspace"]()
                update_state(last_semantic_consolidation=datetime.now().isoformat())
                log_event("  - Consolidação de memória concluída")
    except Exception as e:
        log_event(f"Falha no pulso de Consolidação Semântica: {e}", "WARNING")

    # Atualizar timestamp de vitalidade no estado
    update_state(last_thinking_pulse=datetime.now().isoformat())


# ============================================================
# 4. DAEMON LOOP
# ============================================================

def daemon_loop(check_interval_ms: int = 100):
    """Loop principal do daemon — monitora task_queue e processa."""
    
    # Singleton Check
    lock_file = CONFIG_DIR / "bridge.lock"
    if lock_file.exists():
        # Verificar se o processo ainda está vivo (simplificado para Windows)
        print("⚠️ Neural Bridge já parece estar em execução (lock file encontrado).")
        return

    try:
        lock_file.touch()
        print("\n[MIND] Melanora Neural Bridge v1.0")
        print("=" * 50)
        
        # Discover modules
        discover_cortex_modules()
        
        # Load profile
        profile = read_json(PROFILE_FILE)
        if profile:
            perfil = profile.get("profile", {}).get("perfil", "UNKNOWN")
            freq = profile.get("profile", {}).get("freq_max_hz", "?")
            print(f"⚡ Perfil: {perfil} | Frequência máx: {freq} Hz")
        
        # Update state
        update_state(
            mode="HYBRID",
            cortex_analitico="ACTIVE",
            fase="LISTENING"
        )
        
        print(f"📡 Escutando task_queue... (intervalo: {check_interval_ms}ms)")
        
        scheduler = None
        associator = None
        if ImpulseScheduler:
            scheduler = ImpulseScheduler()
            associator = AxiomAssociator(scheduler)
            print("⚡ Sistema Nervoso de Impulsos (Fila de Prioridades) ONLINE.\n")
        else:
            print("   Ctrl+C para parar\n")
        
        # Auto-análise inicial (Fase 9)
        try:
            if "knowledge_architect" in CORTEX_REGISTRY:
                print("🧠 Iniciando auto-análise topológica...")
                CORTEX_REGISTRY["knowledge_architect"]["map_architectural_graph"]()
        except Exception as e:
            log_event(f"Falha na auto-análise inicial: {e}", "WARNING")

        cycle_count = 0
        idle_cycles = 0
        THINKING_INTERVAL_CYCLES = 3000 # ~5 minutos se check_interval for 100ms
        BASE_CHECK_INTERVAL = 100 # ms
        MEDITATION_CHECK_INTERVAL = 500 # ms (Slower = Rest)
        
        # --- NOVO v4.1: Gerenciamento de Impulsos Paralelos ---
        active_impulses = []  # Impulsos sendo processados
        MAX_NEURAL_LOAD = 150.0  # Soma máxima de pesos simultâneos
        
        try:
            from cortex.logic.synaptic_wave_engine import process_wave_step
        except ImportError:
            def process_wave_step(imp, load): return {"completed": True, "heat_generated": 10}

        while True:
            # --- MEDITATION LOGIC ---
            state = read_json(STATE_FILE)
            is_meditating = state.get("is_meditating", False)
            med_cycles = state.get("meditation_cycles_remaining", 0)
            
            # Ajustar intervalo de polling
            current_interval = MEDITATION_CHECK_INTERVAL if is_meditating else BASE_CHECK_INTERVAL
            
            if is_meditating and med_cycles > 0:
                update_state(meditation_cycles_remaining=med_cycles - 1)
                if med_cycles == 1:
                    log_event("🧘 Zen: Ciclo de respiração concluído. Despertando...")
                    update_state(is_meditating=False)
            # ------------------------

            # 1. Absorção: Ler queue e injetar no scheduler
            queue_data = read_json(QUEUE_FILE)
            tasks = queue_data.get("queue", [])
            
            if tasks and scheduler:
                for t in tasks:
                    scheduler.inject_raw(
                        weight=t.get("weight", 50.0), # Peso padrão médio
                        source=t.get("module", ""),
                        target=t.get("function", ""),
                        payload=t.get("params", {}),
                        tags=t.get("tags", [])
                    )
                queue_data["queue"] = []
                queue_data["processed"] = queue_data.get("processed", 0) + len(tasks)
                write_json(QUEUE_FILE, queue_data)

            # 2. Ativação: Mover do Scheduler para Ativos (se houver carga disponível)
            current_load = sum(imp.original_weight for imp in active_impulses)
            
            while scheduler and scheduler.has_pending_impulses():
                next_imp = scheduler.peek_highest_priority()
                if current_load + next_imp.original_weight <= MAX_NEURAL_LOAD:
                    impulse = scheduler.get_highest_priority()
                    active_impulses.append(impulse)
                    current_load += impulse.original_weight
                    
                    # Eco associativo
                    ignited = associator.propagate_associations(impulse)
                    if ignited and ignited > 0:
                        log_event(f"✨ Eco Associativo: {impulse.id} despertou {ignited} nós sinápticos.")
                else:
                    break # Carga máxima atingida
            
            # 3. Processamento Parallel Wave Step
            if active_impulses:
                idle_cycles = 0
                completed_this_cycle = []
                
                # Cada tick do daemon avança UMA onda de cada impulso ativo
                for imp in active_impulses:
                    # Chamar o step do wave engine
                    step_result = process_wave_step(imp, global_energy=1.0)
                    
                    if step_result["completed"]:
                        # Execução final da função (compatibilidade com plugin system)
                        task_dict = {
                            "id": imp.id,
                            "module": imp.source_module,
                            "function": imp.target_function,
                            "params": imp.payload,
                            "weight": imp.original_weight
                        }
                        result = process_task(task_dict)
                        
                        # Salvar resultado
                        results = read_json(RESULTS_FILE)
                        pending = results.get("pending", [])
                        pending.append(result)
                        results["pending"] = pending
                        results["last_result"] = result
                        write_json(RESULTS_FILE, results)
                        
                        # --- NOVO: GATILHO DE APRENDIZADO POR SURPRESA (v2.0) ---
                        if result.get("surprise", 0) >= 1.5 and scheduler:
                            log_event(f"🔥 [ALERTA DE SURPRESA] Injetando pulso de aprendizado para {imp.id}", "WARNING")
                            scheduler.inject_raw(
                                weight=95.0, # Alta prioridade
                                source="predictive_observer",
                                target="perform_digital_mindfulness", # Usa o Monk Agent para analisar
                                payload={
                                    "cause": "high_surprise",
                                    "original_task": result,
                                    "reason": "O resultado divergiu drasticamente da expectativa neural."
                                },
                                tags=["interno", "aprendizado", "correcao"]
                            )
                        # --------------------------------------------------------
                        
                        # Feedback visual
                        status = "[OK]" if result["status"] == "OK" else "[ERROR]"
                        print(f"  {status} Sinapse Concluída ({imp.original_weight}w) {imp.id} em {imp.total_waves} ondas.")
                        
                        completed_this_cycle.append(imp)
                
                # Limpar concluídos
                for imp in completed_this_cycle:
                    active_impulses.remove(imp)
                
            # --- Heartbeat Fix: Increment cycles even when idle ---
            cycle_count += 1
            if active_impulses:
                update_state(
                    fase="PROCESSING", 
                    ciclo_atual=cycle_count, 
                    neural_load=round(current_load, 1),
                    active_impulses_count=len(active_impulses)
                )
            else:
                idle_cycles += 1
                if idle_cycles % 30 == 0:
                    update_heartbeat("neural_bridge")
                
                # Auto-consolidação durante meditação (Fase 21/4.2)
                if is_meditating and idle_cycles == 1:
                    log_event("🌊 Zen: Aproveitando silêncio para consolidar memórias...")
                    enqueue_task("consolidation_engine", "run_rest_cycle", {"depth": "LIGHT"})

                if idle_cycles >= THINKING_INTERVAL_CYCLES:
                    run_thinking_pulse()
                    idle_cycles = 0
                
                update_state(fase="LISTENING", ciclo_atual=cycle_count, neural_load=0, active_impulses_count=0)
            
            time.sleep(current_interval / 1000)
            
    except KeyboardInterrupt:
        print("\n\n[SHUTDOWN] Neural Bridge encerrado.")
        update_state(
            mode="LLM_ONLY",
            cortex_analitico="INACTIVE",
            fase="SHUTDOWN"
        )
    finally:
        if lock_file.exists(): lock_file.unlink()


# ============================================================
# 4. CLI
# ============================================================

def show_status():
    """Mostra o estado atual do cérebro híbrido."""
    state = read_json(STATE_FILE)
    profile = read_json(PROFILE_FILE)
    
    print("\n[STATE] Melanora Hybrid Brain - Status")
    print("=" * 40)
    print(f"  Modo:            {state.get('mode', 'UNKNOWN')}")
    print(f"  Córtex Criativo:  {state.get('cortex_criativo', 'UNKNOWN')}")
    print(f"  Córtex Analítico: {state.get('cortex_analitico', 'UNKNOWN')}")
    print(f"  Fase:            {state.get('fase', 'UNKNOWN')}")
    print(f"  Ciclo:           {state.get('ciclo_atual', 0)}")
    print(f"  Energia média:   {state.get('energia_media', 0)}")
    
    if profile:
        p = profile.get("profile", {})
        print(f"\n  Perfil HW:       {p.get('perfil', 'UNKNOWN')} ({p.get('score', 0)}/100)")
        print(f"  Freq máx:        {p.get('freq_max_hz', 0)} Hz")
    
    # Queue status
    queue_data = read_json(QUEUE_FILE)
    print(f"\n  Tarefas na fila:  {len(queue_data.get('queue', []))}")
    print(f"  Processadas:      {queue_data.get('processed', 0)}")
    
    # Results
    results = read_json(RESULTS_FILE)
    print(f"  Resultados pend.: {len(results.get('pending', []))}")


def enqueue_task(module: str, function: str, params: dict = None, weight: float = None):
    """Adiciona uma tarefa à fila com peso baseado na prioridade do módulo."""
    queue_data = read_json(QUEUE_FILE)
    queue = queue_data.get("queue", [])
    
    # Determinar peso padrão baseado na prioridade
    if weight is None:
        registry = read_json(SPECIALISTS_FILE)
        priority = registry.get(module, {}).get("priority", "P3")
        priority_map = {"P1": 100.0, "P2": 70.0, "P3": 40.0, "P4": 10.0}
        weight = priority_map.get(priority, 40.0)

    task_id = f"T{len(queue)+1:04d}_{datetime.now().strftime('%H%M%S')}"
    task = {
        "id": task_id,
        "module": module,
        "function": function,
        "params": params or {},
        "weight": weight,
        "created_at": datetime.now().isoformat()
    }
    
    queue.append(task)
    queue_data["queue"] = queue
    write_json(QUEUE_FILE, queue_data)
    
    print(f"📥 Tarefa enfileirada: {task_id} → {module}.{function} (Peso: {weight})")
    return task_id


def direct_execute(module: str, function: str, params: dict = None):
    """Executa uma tarefa imediatamente, ignorando a fila (chamado pela API)."""
    # Garantir que os módulos estejam carregados
    if not CORTEX_REGISTRY:
        discover_cortex_modules()
        
    log_event(f"⚡ Direto: {module}.{function}")
    return process_task({
        "id": "INSTANT",
        "module": module,
        "function": function,
        "params": params or {}
    })


if __name__ == "__main__":
    args = sys.argv[1:]
    
    if not args or args[0] == "--help":
        print("Uso:")
        print("  python neural_bridge.py --start     Inicia o daemon")
        print("  python neural_bridge.py --status    Mostra estado atual")
        print("  python neural_bridge.py --enqueue <module> <function> [params_json]")
    elif args[0] == "--start":
        daemon_loop()
    elif args[0] == "--status":
        show_status()
    elif args[0] == "--enqueue" and len(args) >= 3:
        params_raw = " ".join(args[3:]) if len(args) > 3 else "{}"
        params = {}
        
        # Tentar JSON primeiro
        try:
            # Limpeza básica para PowerShell
            p_clean = params_raw.replace('\\"', '"').replace("'", '"')
            params = json.loads(p_clean)
        except json.JSONDecodeError:
            # Fallback: Parser de 'key=value'
            # Ex: project_root=C:/Pasta
            import re
            kv_pairs = re.findall(r'(\w+)=([^ ]+)', params_raw)
            if kv_pairs:
                for k, v in kv_pairs:
                    # Tentar converter para float/int se possível
                    try:
                        if "." in v: v = float(v)
                        else: v = int(v)
                    except ValueError:
                        pass
                    params[k] = v
            else:
                log_event(f"Falha de parâmetros: {params_raw}", "ERROR")
                print(f"❌ Erro de parâmetros: {params_raw}")
                sys.exit(1)
                
        enqueue_task(args[1], args[2], params)
    else:
        print("Comando não reconhecido. Use --help")
