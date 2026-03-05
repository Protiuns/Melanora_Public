"""
🌳 Melanora Behavior Tree Manager (v1.0)
Orquestrador do Nível 2: Define a sequência e prioridade de execução das tarefas cognitivas.
Implementa uma estrutura de árvore para tomada de decisão robusta.
"""

import time
import json
from pathlib import Path
from neural_bridge import log_event
import requests
from cortex.security.security_nexus import SecurityNexus

class NodeStatus:
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RUNNING = "RUNNING"

class Blackboard:
    """🧠 Memória compartilhada para sincronização entre nós da árvore."""
    def __init__(self):
        self.data = {}
        self.tool_efficacy = {} # {tool_id: score} - Fase 27
        self.area_efficacy = {} # {area_name: score} - Fase 28
        self.node_metrics = {} # {node_name: {"I": count, "R": Resistance, "V": Voltage}} - Fase 33

    def set(self, key, value):
        self.data[key] = value

    def get(self, key, default=None):
        return self.data.get(key, default)

class BTNode:
    def __init__(self, name):
        self.name = name
        self.status = None

    def tick(self, context):
        raise NotImplementedError

class Composite(BTNode):
    def __init__(self, name):
        super().__init__(name)
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        return self

class Selector(Composite):
    """Retorna sucesso se qualquer filho retornar sucesso (OR)."""
    def tick(self, context):
        for child in self.children:
            status = child.tick(context)
            if status != NodeStatus.FAILURE:
                self.status = status
                return status
        self.status = NodeStatus.FAILURE
        return NodeStatus.FAILURE

class Sequence(Composite):
    """Retorna sucesso apenas se todos os filhos retornarem sucesso (AND)."""
    def tick(self, context):
        for child in self.children:
            status = child.tick(context)
            if status != NodeStatus.SUCCESS:
                self.status = status
                return status
        self.status = NodeStatus.SUCCESS
        return NodeStatus.SUCCESS

class Action(BTNode):
    def __init__(self, name, action_func, priority_func=None, atomic=False):
        super().__init__(name)
        self.action_func = action_func
        self.priority_func = priority_func # Função que retorna um peso (int/float)
        self.atomic = atomic # Se True, não pode ser interrompido (Fase 23)

    def get_priority(self, context):
        if self.priority_func:
            return self.priority_func(context)
        return 0 # Prioridade padrão

    def tick(self, context):
        start_time = time.time()
        bb = context.get("blackboard")
        
        # Coleta Voltagem (V) - Baseado em prioridade
        v = self.get_priority(context)
        
        try:
            result = self.action_func(context)
            duration = (time.time() - start_time) * 1000 # ms
            
            # Atualiza Métricas (Ohm's Law)
            metrics = bb.node_metrics.get(self.name, {"I": 0, "R": 0, "V": 0})
            metrics["I"] += 1
            metrics["V"] = v
            metrics["R"] = duration # Resistência é proporcional ao tempo
            bb.node_metrics[self.name] = metrics
            
            # Se retornar um status direto (RUNNING)
            if result == NodeStatus.RUNNING:
                self.status = NodeStatus.RUNNING
                return self.status
                
            if result:
                if isinstance(result, dict):
                    for k, v_dict in result.items():
                        if k != "status": context["results"][self.name] = v_dict
                    if "status" in result:
                        self.status = result["status"]
                        return self.status
            
            self.status = NodeStatus.SUCCESS
            return self.status
        except Exception as e:
            log_event(f"BT: [Neural Circuitry] Erro no componente {self.name} (Curto-circuito): {e}", "ERROR")
            self.status = NodeStatus.FAILURE
            return self.status

class Condition(BTNode):
    def __init__(self, name, condition_func):
        super().__init__(name)
        self.condition_func = condition_func

    def tick(self, context):
        self.status = NodeStatus.SUCCESS if self.condition_func(context) else NodeStatus.FAILURE
        return self.status

class Decorator(BTNode):
    """Nó que envolve um único filho e modifica seu comportamento."""
    def __init__(self, name, child):
        super().__init__(name)
        self.child = child

class SecurityGuard(Decorator):
    """
    🛡️ Escudo de Segurança: Intercepta o tick do filho para validar segurança.
    Aplica Data Immunity e Execution Barrier.
    """
    def tick(self, context):
        # 1. Barreira de Execução: Se o contexto tiver um comando motor, valida
        command = context.get("target_command")
        if command and not SecurityNexus.validate_command(command):
            log_event(f"BT: [Security Guard] Comando bloqueado por segurança: {command}", "WARNING")
            self.status = NodeStatus.FAILURE
            return self.status
        
        # 2. Executa o filho
        status = self.child.tick(context)
        
        # 3. Imunidade de Dados: Sanitiza resultados se necessário
        # Simplificação: Sanitiza resultados salvos no blackboard/contexto
        result = context.get("last_result")
        if isinstance(result, str):
            sanitized = SecurityNexus.sanitize_content(result)
            if sanitized != result:
                context["last_result"] = sanitized
                log_event("BT: [Security Guard] Conteúdo sensível sanitizado.", "INFO")
        
        self.status = status
        return status

class Inverter(Decorator):
    def tick(self, context):
        status = self.child.tick(context)
        if status == NodeStatus.SUCCESS: self.status = NodeStatus.FAILURE
        elif status == NodeStatus.FAILURE: self.status = NodeStatus.SUCCESS
        else: self.status = status
        return self.status

class Succeeder(Decorator):
    def tick(self, context):
        self.child.tick(context)
        self.status = NodeStatus.SUCCESS
        return NodeStatus.SUCCESS

class ConditionDecorator(Decorator):
    def __init__(self, name, child, condition_key, expected_value):
        super().__init__(name, child)
        self.condition_key = condition_key
        self.expected_value = expected_value

    def tick(self, context):
        blackboard = context.get("blackboard")
        val = blackboard.get(self.condition_key)
        if blackboard and val == self.expected_value:
            self.status = self.child.tick(context)
        else:
            self.status = NodeStatus.FAILURE
        return self.status

class CerebralAreaBurst(Decorator):
    """Executa o filho N vezes (Pulsos Sinápticos) baseados na prioridade (Fase 20)."""
    def __init__(self, name, child, pulse_key):
        super().__init__(name, child)
        self.pulse_key = pulse_key # Chave no blackboard que define o budget de pulsos

    def tick(self, context):
        blackboard = context.get("blackboard")
        budget = blackboard.get(self.pulse_key, 1)
        
        # Recupera pulso atual se havia sido interrompido (Fase 23)
        start_pulse = blackboard.get(f"resume_{self.name}", 0)
        
        last_status = NodeStatus.FAILURE
        for i in range(start_pulse, budget):
            # Fase 24: Metacognição (Cost-Benefit)
            confidence = context.get("results", {}).get("confidence", 0)
            if i > 0 and confidence > 0.9:
                log_event(f"BT: [Metacognition] Interrompendo {self.name}: Confiança alta ({confidence}).")
                last_status = NodeStatus.SUCCESS
                break

            last_status = self.child.tick(context)
            
            # Registra progresso (Fase 21/23)
            if "synaptic_history" not in context["results"]:
                context["results"]["synaptic_history"] = {}
            context["results"]["synaptic_history"][self.name] = i + 1
            
            if last_status == NodeStatus.RUNNING:
                blackboard.set(f"resume_{self.name}", i)
                break 
        
        if last_status != NodeStatus.RUNNING:
            blackboard.set(f"resume_{self.name}", 0) # Reset se terminou
            
        self.status = last_status
        return self.status

class AreaGate(Decorator):
    """Portão que permite ou bloqueia a execução de uma área cerebral (Fase 22)."""
    def __init__(self, name, child):
        super().__init__(name, child)

    def tick(self, context):
        bb = context.get("blackboard")
        is_active = bb.get(f"area_{self.name}_active", True)
        
        # Só ignora o gating se já estiver rodando e o filho for 'atomic' (Fase 23)
        # Por padrão, permitimos a interrupção entre pulsos de rajada (AreaBurst)
        is_atomic = getattr(self.child, "atomic", False)
        was_running = self.status == NodeStatus.RUNNING
        
        if not is_active:
            if was_running and is_atomic:
                log_event(f"BT: [AreaGate] Mantendo {self.name.upper()} ativa para completar tarefa ATÔMICA.")
            else:
                log_event(f"BT: [AreaGate] Área {self.name.upper()} está OFFLINE (Gated).")
                self.status = NodeStatus.FAILURE
                return self.status
            
            
        # Fase 28: Registro de uso para Darwinismo Neural
        if "areas_run_in_tick" not in context:
            context["areas_run_in_tick"] = []
        if self.name not in context["areas_run_in_tick"]:
            context["areas_run_in_tick"].append(self.name)

        self.status = self.child.tick(context)
        return self.status

class HeuristicCache(Decorator):
    """Implementa o 'System 1': Atalhos mentais baseados em experiências anteriores (Fase 24)."""
    def __init__(self, name, child):
        super().__init__(name, child)
        self.cache = {} # Dict {prompt: result}

    def tick(self, context):
        prompt = context.get("user_prompt", "")
        if not prompt:
            return self.child.tick(context)

        if prompt in self.cache:
            log_event(f"BT: [Heuristic] Atalho mental ('System 1') ativado para: {prompt[:20]}...")
            context["results"]["heuristic_response"] = self.cache[prompt]
            self.status = NodeStatus.SUCCESS
            return self.status

        self.status = self.child.tick(context)
        
        # Se o Ciclo tiver sucesso, podemos cachear
        final_res = context.get("results", {}).get("final_response")
        if self.status == NodeStatus.SUCCESS and final_res:
             self.cache[prompt] = final_res
             
        return self.status

class Parallel(Composite):
    """Executa todos os filhos simultaneamente. Sucesso se todos(AND) ou qualquer(OR) tiver sucesso."""
    def __init__(self, name, policy="ALL", timeout=None):
        super().__init__(name)
        self.policy = policy # "ALL" (AND) ou "ANY" (OR)
        self.timeout = timeout
        self.start_time = None

    def tick(self, context):
        if self.start_time is None:
            self.start_time = time.time()
        
        # Check timeout (Fase 19)
        if self.timeout and (time.time() - self.start_time > self.timeout):
            log_event(f"BT: [Parallel] {self.name} TIMEOUT atingido ({self.timeout}s)")
            self.status = NodeStatus.FAILURE
            return NodeStatus.FAILURE

        success_count = 0
        failure_count = 0
        running_count = 0
        
        for child in self.children:
            status = child.tick(context)
            if status == NodeStatus.SUCCESS: success_count += 1
            elif status == NodeStatus.FAILURE: failure_count += 1
            else: running_count += 1
        
        if self.policy == "ANY" and success_count > 0:
            self.status = NodeStatus.SUCCESS
        elif self.policy == "ALL" and success_count == len(self.children):
            self.status = NodeStatus.SUCCESS
        elif failure_count > 0 and self.policy == "ALL":
            self.status = NodeStatus.FAILURE
        elif running_count > 0:
            self.status = NodeStatus.RUNNING
        else:
            self.status = NodeStatus.FAILURE
            
        return self.status

class PrioritySelector(Composite):
    """Executa o filho com a maior prioridade calculada no momento do tick."""
    def tick(self, context):
        # Ordena filhos por prioridade decrescente
        sorted_children = sorted(
            self.children, 
            key=lambda c: c.get_priority(context) if hasattr(c, 'get_priority') else 0, 
            reverse=True
        )
        
        for child in sorted_children:
            # log_event(f"BT: [PrioritySelector] Avaliando {child.name}")
            status = child.tick(context)
            if status != NodeStatus.FAILURE:
                self.status = status
                return status
        self.status = NodeStatus.FAILURE
        return NodeStatus.FAILURE

class SituationalEvaluator(BTNode):
    """Nó que escolhe uma sub-árvore inteira baseada no Situational_ID (Fase 19)."""
    def __init__(self, name, tree_map):
        super().__init__(name)
        self.tree_map = tree_map # Dict {Situational_ID: Node}

    def tick(self, context):
        situational_id = context.get("blackboard").get("situational_id", "DEFAULT")
        target_tree = self.tree_map.get(situational_id) or self.tree_map.get("DEFAULT")
        
        if target_tree:
            log_event(f"BT: [SituationalEvaluator] Alternando para modo: {situational_id}")
            self.status = target_tree.tick(context)
            return self.status
        
        self.status = NodeStatus.FAILURE
        return NodeStatus.FAILURE

class MotorReflex(BTNode):
    """Nó de Ação Reflexiva: Executa comandos pré-programados no Córtex Motor Local (Fase 29)."""
    def __init__(self, name, reflex_type, params=None):
        super().__init__(name)
        self.reflex_type = reflex_type # 'web_surge', 'file_dispatch', 'digital_sight'
        self.params = params or {}

    def tick(self, context):
        log_event(f"BT: [MotorReflex] Ticking {self.name}...")
        url_map = {
            "web_surge": "web_surge",
            "file_dispatch": "file_dispatch",
            "digital_sight": "digital_sight"
        }
        
        endpoint = url_map.get(self.reflex_type)
        if not endpoint:
            self.status = NodeStatus.FAILURE
            return self.status
            
        try:
            log_event(f"BT: [MotorReflex] Disparando arco reflexo: {self.reflex_type}...")
            response = requests.post(
                f"http://127.0.0.1:8500/reflex/{endpoint}",
                json=self.params,
                timeout=30
            )
            if response.status_code == 200:
                res_data = response.json()
                context["results"][self.name] = res_data
                log_event(f"BT: [MotorReflex] Reflexo {self.reflex_type} concluído com sucesso.")
                self.status = NodeStatus.SUCCESS
            else:
                self.status = NodeStatus.FAILURE
        except Exception as e:
            log_event(f"BT: [MotorReflex] Erro no reflexo: {e}", "ERROR")
            self.status = NodeStatus.FAILURE
            
        return self.status

class DynamicTuner(BTNode):
    """Nó que invoca especialistas matemáticos para ajustar o Blackboard em tempo real (Fase 26)."""
    def __init__(self, name, tools_to_run):
        super().__init__(name)
        self.tools_to_run = tools_to_run # List of tool IDs

    def tick(self, context):
        from cortex.specialists.neural_tool_manager import run_neural_tool_scan
        bb = context.get("blackboard")
        
        # Fase 27: Filtra ferramentas com baixa eficácia (< 0.2)
        active_tools = []
        for tid in self.tools_to_run:
            score = bb.tool_efficacy.get(tid, 0.5) # Default 0.5 para novas
            if score >= 0.2:
                active_tools.append(tid)
            else:
                log_event(f"BT: [DynamicTuner] Pulando {tid} devido a baixa eficácia ({score}).", "WARN")

        # Dados de amostra para os especialistas
        sample = [{
            "id": "MELANORA_CORE",
            "load": bb.get("system_load", 0),
            "tags": bb.get("active_tags", ["reasoning"]),
            "success_history": bb.get("success_history", [1, 1, 1]),
            "drift": 0.1
        }]

        tools_used = []
        for tool_id in active_tools:
            res = run_neural_tool_scan(tool_id, sample)
            if res.get("status") == "SUCCESS":
                data = res["results"][0]
                tools_used.append(tool_id)
                
                if tool_id == "nt_numerical_counter":
                    bb.set("prefrontal_pulses", data["suggested_pulses"])
                    log_event(f"BT: [Tuning] Budget de pulsos ajustado para {data['suggested_pulses']} via Counter.")
                
                elif tool_id == "nt_dimensional_scaler":
                    bb.set("abstraction_level", data["abstraction_level"])
                    log_event(f"BT: [Tuning] Nível de abstração definido como {data['recommended_dimension']}.")

        # Fase 28: Rebalanceamento Darwiniano
        # Ajusta os budgets baseados na eficácia histórica da área
        area_to_pulse_map = {
            "Prefrontal_Cortex": "prefrontal_pulses",
            "Limbic_System": "limbic_pulses",
            "Motor_Cortex": "motor_pulses"
        }
        
        for area_name, pulse_key in area_to_pulse_map.items():
            score = bb.area_efficacy.get(area_name, 0.8)
            if score < 0.6:
                current_pulses = bb.get(pulse_key, 1)
                # Redução agressiva para áreas ineficazes
                new_pulses = max(1, int(current_pulses * score))
                if new_pulses < current_pulses:
                    bb.set(pulse_key, new_pulses)
                    log_event(f"BT: [Darwinism] Pulso de {area_name.upper()} podado para {new_pulses} (Score: {score}).")

        # Registra no contexto quais ferramentas foram usadas para avaliação posterior
        context["tools_run_in_tick"] = tools_used

        self.status = NodeStatus.SUCCESS
        return self.status

# --- Implementação de Comportamentos Específicos de Melanora ---

class CognitiveOrchestrator:
    def __init__(self):
        self.blackboard = Blackboard()
        self.blackboard.set("emotion", "melancholy")
        self.blackboard.set("cycle_count", 0)
        self.blackboard.set("situational_id", "DEFAULT")
        
        # Budgets Iniciais de Pulsos (Fase 20)
        self.blackboard.set("prefrontal_pulses", 2)
        self.blackboard.set("limbic_pulses", 1)
        self.blackboard.set("motor_pulses", 1) # Fase 28
        self.blackboard.set("prefrontal_pulses", 2)
        
        self.blackboard.set("area_Limbic_System_active", True)
        self.blackboard.set("area_Prefrontal_Cortex_active", True)
        self.blackboard.set("area_Motor_Cortex_active", True)
        
        self.root = self._build_tree()
        self.context = {
            "last_tick": time.time(),
            "active_goal": None,
            "results": {},
            "blackboard": self.blackboard
        }

    def _build_tree(self):
        # --- ÁREA: SISTEMA LÍMBICO (Emoções e Filtros) ---
        limbic_system = Sequence("Limbic_System")
        
        # Fissão Límbica: Divisão em filtros específicos (Fase 35)
        emotions_branch = Parallel("Emotional_Filters", policy="ALL")
        emotions_branch.add_child(Action("Fear_Filter", self.limbic_fear_check))
        emotions_branch.add_child(Action("Empathy_Filter", self.limbic_empathy_filter))
        emotions_branch.add_child(Action("Aggression_Filter", self.limbic_aggression_filter))
        
        limbic_system.add_child(Action("Emotion_Sync", self.bt_transition_emotion))
        limbic_system.add_child(emotions_branch)
        limbic_system.add_child(ConditionDecorator("Surprise_Monitor", 
            Action("Reflex_Stabilization", self.run_stabilization), "surprise_detected", True))

        # --- ÁREA: CÓRTEX PRÉ-FRONTAL (Estratégia e Fissão) ---
        prefrontal_cortex = Sequence("Prefrontal_Cortex")
        
        # Fissão da Pesquisa (Phase 34)
        research_parallel = Parallel("Fission_Research", policy="ALL")
        research_parallel.add_child(Action("Internal_Manual_Scan", self.bt_search_internal))
        research_parallel.add_child(Action("Grounding_Sync", self.bt_research))
        
        # Fissão do Rascunho (Phase 34)
        draft_sequence = Sequence("Fission_Drafting")
        draft_sequence.add_child(Action("Strategic_Outline", self.bt_structure_plan))
        draft_sequence.add_child(Action("Content_Synthesis", self.bt_draft))
        draft_sequence.add_child(Action("Self_Critique_Loop", self.bt_critique))

        prefrontal_cortex.add_child(research_parallel)
        prefrontal_cortex.add_child(draft_sequence)

        # --- ÁREA: CÓRTEX MOTOR (Arcos Reflexos Expandidos) ---
        motor_cortex = Sequence("Motor_Cortex")
        motor_cortex.add_child(MotorReflex("Digital_Snapshot", "digital_sight"))
        
        # Expansão de Arcos Motores (Phase 35: +20 nodos)
        motor_specialists = Parallel("Motor_Specialists", policy="ANY")
        motor_specialists.add_child(MotorReflex("Git_Status", "file_dispatch", {"action": "git_status"}))
        motor_specialists.add_child(MotorReflex("Git_Commit", "file_dispatch", {"action": "git_commit"}))
        motor_specialists.add_child(MotorReflex("Git_Push", "file_dispatch", {"action": "git_push"}))
        motor_specialists.add_child(MotorReflex("File_Archive", "file_dispatch", {"action": "archive"}))
        motor_specialists.add_child(MotorReflex("File_Search", "file_dispatch", {"action": "search"}))
        motor_specialists.add_child(MotorReflex("Web_Scout", "web_surge", {"depth": 1}))
        motor_specialists.add_child(MotorReflex("Screen_Deep_Analysis", "digital_sight", {"detail": "high"}))
        motor_specialists.add_child(Action("Terminal_Cleanup", self.motor_terminal_cleanup))
        motor_specialists.add_child(Action("Memory_Defragment", self.motor_memory_defrag))
        motor_specialists.add_child(Action("Registry_Backup", self.motor_registry_backup))
        motor_specialists.add_child(Action("Log_Rotation", self.motor_log_rotation))
        motor_specialists.add_child(Action("Path_Verify", self.motor_path_verify))
        motor_specialists.add_child(Action("Dependency_Audit", self.motor_dep_audit))
        motor_specialists.add_child(Action("Cache_Purge", self.motor_cache_purge))
        motor_specialists.add_child(Action("Network_Ping", self.motor_net_ping))
        motor_specialists.add_child(Action("Health_Sync", self.motor_health_sync))
        motor_specialists.add_child(Action("Artifact_Link", self.motor_artifact_link))
        motor_specialists.add_child(Action("Context_Prune", self.motor_context_prune))
        motor_specialists.add_child(Action("Synapse_Stabilize", self.motor_synapse_stabilize))
        motor_specialists.add_child(Action("Mind_Backup", self.motor_mind_backup))
        
        motor_cortex.add_child(motor_specialists)
        motor_cortex.add_child(Action("Consolidate_Knowledge", self.bt_consolidate))
        motor_cortex.add_child(Action("Finalize_Response", self.bt_finalize))

        # --- ÁREAS COM PORTÕES ---
        Limbic_Gated = AreaGate("Limbic_System", limbic_system)
        Prefrontal_Gated = AreaGate("Prefrontal_Cortex", prefrontal_cortex)
        Motor_Gated = AreaGate("Motor_Cortex", motor_cortex)

        # --- ORQUESTRADOR SITUACIONAL ---
        situational_map = {
            "RESEARCH": Sequence("Research_Mode").add_child(CerebralAreaBurst("Reason_Burst", Prefrontal_Gated, "prefrontal_pulses")),
            "DEFAULT": Sequence("Default_Mode")
                .add_child(CerebralAreaBurst("Emotional_Pulse", Limbic_Gated, "limbic_pulses"))
                .add_child(CerebralAreaBurst("Action_Pulse", Motor_Gated, "motor_pulses")),
            "EMERGENCY": Limbic_Gated 
        }
        
        root = Sequence("Synaptic_Gateway")
        root.add_child(DynamicTuner("NeuroMath_Adjuster", ["nt_numerical_counter", "nt_dimensional_scaler"]))
        
        decision_layer = Selector("Decision_Layer")
        decision_layer.add_child(ConditionDecorator("Emergency_Gate", limbic_system, "surprise_detected", True))
        decision_layer.add_child(SituationalEvaluator("Area_Selector", situational_map))
        
        root.add_child(decision_layer)
        return HeuristicCache("Universal_Heuristics", root)

    def tick(self, input_context=None):
        if input_context:
            self.context.update(input_context)
            # Sincroniza o contexto de entrada com o Blackboard (Fase 19)
            for key, value in input_context.items():
                self.blackboard.set(key, value)
            
            # Lógica de Gating Dinâmico (Fase 22)
            load = self.blackboard.get("system_load", 0)
            if load > 70:
                log_event(f"BT: [Gating] Carga alta ({load}%). Desativando áreas secundárias.", "WARN")
                self.blackboard.set("area_Limbic_System_active", False)
                self.blackboard.set("area_Motor_Cortex_active", False)
            else:
                self.blackboard.set("area_Limbic_System_active", True)
                self.blackboard.set("area_Motor_Cortex_active", True)

            # --- Fase 24: Somatic Markers (Marcadores Somáticos) ---
            # Ajusta budgets de pulsos baseados na emoção (Sistema Límbico guiando a razão)
            emotion = self.blackboard.get("emotion", "neutral")
            if emotion == "alert" or emotion == "surprise":
                self.blackboard.set("limbic_pulses", 3)
                self.blackboard.set("prefrontal_pulses", 1)  # Reação > Reflexão
            elif emotion == "curiosity":
                self.blackboard.set("prefrontal_pulses", 4)  # Reflexão profunda
                self.blackboard.set("limbic_pulses", 1)
            else:
                # Default (Fase 19/20)
                self.blackboard.set("prefrontal_pulses", 2)
                self.blackboard.set("limbic_pulses", 1)
        
        # Garante que as chaves de controle do tick estejam presentes
        self.context["blackboard"] = self.blackboard
        self.context["results"] = self.context.get("results", {})
        
        status = self.root.tick(self.context)
        
        # Fase 27: Efficacy Tracker (Atualiza scores baseado no sucesso do final do tick)
        tools_used = self.context.get("tools_run_in_tick", [])
        if tools_used:
            reward = 0.1 if status == NodeStatus.SUCCESS else -0.1
            for tid in tools_used:
                current = self.blackboard.tool_efficacy.get(tid, 0.5)
                # Clamp entre 0 e 1
                new_score = max(0.0, min(1.0, current + reward))
                self.blackboard.tool_efficacy[tid] = round(new_score, 2)
            
            # Limpa para o próximo tick
            self.context["tools_run_in_tick"] = []

        # Fase 28: Darwinismo Neural (Áreas)
        areas_used = self.context.get("areas_run_in_tick", [])
        if areas_used:
            reward = 0.05 if status == NodeStatus.SUCCESS else -0.1
            for area_name in areas_used:
                current = self.blackboard.area_efficacy.get(area_name, 0.8) # Default 0.8
                new_score = max(0.1, min(1.0, current + reward))
                self.blackboard.area_efficacy[area_name] = round(new_score, 2)
                if reward < 0:
                    log_event(f"BT: [Darwinism] Área {area_name.upper()} penalizada. Score: {new_score}", "WARN")
            
            self.context["areas_run_in_tick"] = []

        # --- Fase 33: Neural Circuitry Analysis (Fissão/Fusão) ---
        for node_name, metrics in self.blackboard.node_metrics.items():
            # Desempacota V (Voltagem), R (Resistência) e I (Corrente/Instâncias)
            v = metrics.get("V", 0)
            r = metrics.get("R", 0)
            i = metrics.get("I", 0)
            
            # Filtra nodos que rodaram pouco para evitar ruído
            if i < 3: continue 

            # Lógica de Fissão: Alta Resistência estrangulando o fluxo
            if r > 500: # Nodo demorou mais de 500ms
                log_event(f"BT: [Circuitry] Recomendada FISSÃO em '{node_name}'. Resistência alta ({r:.1f}ms).", "INFO")
            
            # Lógica de Fusão: Baixa Tensão e Baixa Resistência (redundância)
            if r < 10 and v < 2 and i > 10:
                log_event(f"BT: [Circuitry] Recomendada FUSÃO em '{node_name}'. Componente subutilizado.", "INFO")

        return {"status": status, "results": self.context["results"]}

    # --- Callbacks: Limbic (Phase 35) ---
    def limbic_fear_check(self, context):
        load = context["blackboard"].get("system_load", 0)
        risk = 0.8 if load > 80 else 0.2
        context["results"]["fear_level"] = risk
        log_event(f"BT: [Limbic] Fear Filter: Risco de colapso em {risk*100:.1f}%.")
        return NodeStatus.SUCCESS

    def limbic_empathy_filter(self, context):
        context["results"]["social_context"] = "collaborative"
        return NodeStatus.SUCCESS

    def limbic_aggression_filter(self, context):
        # Impede loops obsessivos
        count = context["blackboard"].get("cycle_count", 0)
        if count > 5:
            log_event("BT: [Limbic] Aggression Filter: Inibindo persistência excessiva.", "WARN")
            return NodeStatus.FAILURE
        return NodeStatus.SUCCESS

    # --- Callbacks: Motor Arcs (Phase 35) ---
    def motor_terminal_cleanup(self, context): return NodeStatus.SUCCESS
    def motor_memory_defrag(self, context): return NodeStatus.SUCCESS
    def motor_registry_backup(self, context): return NodeStatus.SUCCESS
    def motor_log_rotation(self, context): return NodeStatus.SUCCESS
    def motor_path_verify(self, context): return NodeStatus.SUCCESS
    def motor_dep_audit(self, context): return NodeStatus.SUCCESS
    def motor_cache_purge(self, context): return NodeStatus.SUCCESS
    def motor_net_ping(self, context): return NodeStatus.SUCCESS
    def motor_health_sync(self, context): return NodeStatus.SUCCESS
    def motor_artifact_link(self, context): return NodeStatus.SUCCESS
    def motor_context_prune(self, context): return NodeStatus.SUCCESS
    def motor_synapse_stabilize(self, context): return NodeStatus.SUCCESS
    def motor_mind_backup(self, context): return NodeStatus.SUCCESS

    # --- Callbacks: Prefrontal Fission (Phase 34) ---
    def bt_search_internal(self, context):
        log_event("BT: Escaneando manuais internos (Doutrina)...")
        return {"output": "Conhecimento interno recuperado."}

    def bt_structure_plan(self, context):
        log_event("BT: Esboçando arquitetura da resposta...")
        return {"output": "Estrutura definida."}

    # --- Callbacks Originais ---
    
    def check_surprise(self, context):
        from cortex.logic.cortex_reflexo import generate_quick_intuition
        res = generate_quick_intuition()
        return res.get("surprise", False)

    def run_stabilization(self, context):
        log_event("BT: Executando estabilização emergencial.", "WARN")
        return {"output": "Estabilização Concluída"}

    def bt_research(self, context):
        from cortex.specialists.notebook_researcher import query_grounded_context
        prompt = context.get('user_prompt')
        log_event(f"BT: Iniciando pesquisa NotebookLM para: {prompt[:30]}...")
        res = query_grounded_context(prompt)
        return {"output": res}

    def bt_consolidate(self, context):
        """
        Nó de Consolidação: Automação da 'aprendizagem' a partir da pesquisa.
        """
        from cortex.specialists.notebook_researcher import extract_key_concepts
        research_res = context["results"].get("Grounded_Research_Phase", {})
        
        log_event("BT: Consolidando conhecimento extraído...")
        concepts = extract_key_concepts(research_res)
        
        if concepts:
            context["active_concepts"] = concepts
            log_event(f"CONHECIMENTO ABSORVIDO: {', '.join(concepts)}")
            return {"output": f"Consolidou {len(concepts)} conceitos."}
        
        return {"output": "Nenhum conceito novo extraído."}

    def bt_draft(self, context):
        from cortex.system_2.deep_architect import ask_ollama
        research = context["results"].get("Grounded_Research_Phase", {})
        grounded_data = research.get("answer", "")
        bb_data = context["blackboard"].data
        
        prompt = f"Crie um rascunho técnico baseado neste pedido: {context.get('user_prompt')}\n\nUSE ESTE CONTEXTO GROUNDED DO NOTEBOOKLM:\n{grounded_data}"
        res = ask_ollama(prompt, system="Engenheiro Inicial", context_meta=bb_data)
        return {"output": res}

    def bt_critique(self, context):
        from cortex.system_2.deep_architect import ask_ollama
        draft = context["results"].get("Melancholic_Draft") or context["results"].get("Euphoric_Creative_Draft") or ""
        bb_data = context["blackboard"].data
        
        prompt = f"Critique este rascunho:\n\n{draft}"
        res = ask_ollama(prompt, system="Analista Crítico", context_meta=bb_data)
        return {"output": res}

    def bt_finalize(self, context):
        from cortex.system_2.deep_architect import ask_ollama
        # Pega o último rascunho independente do nome da fase
        results = context["results"]
        draft = results.get("Melancholic_Draft") or results.get("Euphoric_Creative_Draft") or ""
        critique = results.get("Critique_Phase", "")
        bb_data = context["blackboard"].data.copy()
        
        # Inclui histórico sináptico no meta (Fase 21)
        bb_data["synaptic_history"] = results.get("synaptic_history", {})
        
        # Inclui status de ativação de áreas (Fase 22)
        bb_data["area_status"] = {
            "Limbic_System": bb_data.get("area_Limbic_System_active", True),
            "Prefrontal_Cortex": bb_data.get("area_Prefrontal_Cortex_active", True),
            "Motor_Cortex": bb_data.get("area_Motor_Cortex_active", True)
        }
        
        prompt = f"Componha a resposta final baseada no rascunho e crítica:\n\nDraft: {draft}\nCritique: {critique}"
        res = ask_ollama(prompt, system="Arquiteto Mestre", context_meta=bb_data)
        return {"output": res}

    def bt_transition_emotion(self, context):
        """Alterna humor baseado em ciclos para simular dinâmica emocional."""
        bb = context["blackboard"]
        count = bb.get("cycle_count") + 1
        bb.set("cycle_count", count)
        
        current = bb.get("emotion")
        if count >= 3: # Muda a cada 3 ciclos
            new_emotion = "euphoria" if current == "melancholy" else "melancholy"
            bb.set("emotion", new_emotion)
            bb.set("cycle_count", 0)
            log_event(f"BT: TRANSIÇÃO EMOCIONAL -> {new_emotion.upper()}")
            return {"output": f"Mudou para {new_emotion}"}
        
        return {"output": f"Mantendo {current} (Ciclo {count}/3)"}

    # --- Funções de Prioridade ---

    def prio_heavy_task(self, context):
        """Tarefas pesadas ganham prioridade apenas se o sistema estiver IDLE."""
        load = context["blackboard"].get("system_load", 0)
        if load < 50: return 50
        return 5 # Baixa prioridade se carregado

    def prio_light_task(self, context):
        """Tarefas leves sempre têm prioridade moderada."""
        return 30

if __name__ == "__main__":
    orchestrator = CognitiveOrchestrator()
    print(f"Tiking Tree... Status: {orchestrator.tick()}")
