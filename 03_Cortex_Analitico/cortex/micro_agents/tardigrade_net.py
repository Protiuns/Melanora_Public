import logging
from typing import List, Dict, Any
from cortex.logic.neural_irrigation import global_gland

logger = logging.getLogger("TardigradeTissue")

class SynapticGroup:
    """
    Sub-Cluster da Malha Neural.
    Agrupa nós que têm a mesma finalidade genérica. Permite ligar/desligar regiões inteiras
    do cérebro para poupar CPU, simulando a varredura "Soneca" ciclicamente.
    """
    def __init__(self, name: str, node_count: int, base_affinity: str):
        self.name = name
        self.node_count = node_count
        self.base_affinity = base_affinity # "survive", "explore", "maintain"
        
        # Meta-status do Cluster O(1)
        self.is_active = True
        self.inactivity_ticks = 0
        self.accumulated_need = 0.0 # Quanto tempo esse cluster foi deixado em coma
        
    def scan_need(self) -> float:
        """Calcula o Nível de Socorro do Cluster com base no abandono e no hormônio base."""
        # Se for um cluster de Manutenção parado (inactivity_ticks alto), a necessidade grita.
        needs = (self.inactivity_ticks * 0.5) 
        if needs > 95.0:
            needs = 100.0 # Bate no teto
        self.accumulated_need = needs
        return needs


class SynapticNode:
    """
    Nó Microscópico Otimizado.
    Pertence a um SynapticGroup, e NÃO RODA se o grupo estiver dormindo.
    """
    def __init__(self, node_id: int, parent_group: str):
        self.node_id = node_id
        self.parent_group = parent_group
        
        # Aptidão Baseada no Grupo Parente
        self.affinity_score = 0.5 

    def fire(self, climate: Dict[str, float], parent_affinity: str) -> float:
        """Equação de Vontade Baseada no Clima (Calculada O(1))"""
        adrenaline = climate.get("adrenaline", 0.0)
        dopamine = climate.get("dopamine", 0.0)
        serotonin = climate.get("serotonin", 0.5)

        score = self.affinity_score
        
        if parent_affinity == "survive":
            score *= (1.0 + (adrenaline * 3.0))
        elif parent_affinity == "explore":
            score *= (1.0 + (dopamine * 2.0))
        elif parent_affinity == "maintain":
            score *= (serotonin * 2.0)
            
        return score


class TardigradeTissue:
    """
    O Córtex Adormecido.
    Composto por Sub-Grupos (Clusters). Ativa apenas a Mente necessária,
    economizando recursos massivos. Os grupos em "Soneca" acordam para checar
    a temperatura a cada 10 ciclos.
    """
    def __init__(self):
        # A Arquitetura Particionada do Usuário
        self.clusters = {
            "c_escape": SynapticGroup("c_escape", 50, "survive"),
            "c_curiosity": SynapticGroup("c_curiosity", 30, "explore"),
            "c_memory": SynapticGroup("c_memory", 120, "maintain")
        }
        
        # Populando os nós dentro dos dicionários 
        self.nodes_map = {
            "c_escape": [SynapticNode(i, "c_escape") for i in range(50)],
            "c_curiosity": [SynapticNode(i, "c_curiosity") for i in range(30)],
            "c_memory": [SynapticNode(i, "c_memory") for i in range(120)]
        }
        
        # Relógio de Varredura Superficial
        self.CLOCK_NAP_CHECK = 10 
        
        logger.info(f"🐛 Tecido Sub-Agrupado Mimetizado: 200 Nós alocados em 3 Clusters independentes.")

    def process_stimulus(self, stimulus_type: str, payload: Any) -> float:
        """
        O grande filtro de eficiência.
        """
        climate = global_gland.extract_climate()
        
        # 1. ORQUESTRAÇÃO DE SONECA ---------------------------------------
        # Define quem deve ficar ativo baseado no hormônio primário
        highest_hormone = max(climate, key=climate.get)
        
        if highest_hormone == "adrenaline" and climate["adrenaline"] > 0.4:
            active_target = "survive"
        elif highest_hormone == "dopamine" and climate["dopamine"] > 0.5:
            active_target = "explore"
        else:
            active_target = "maintain" # Default Paz
            
        # Altera os status O(1) dos Bairros Cerebrais
        for c_name, cluster in self.clusters.items():
            if cluster.base_affinity == active_target:
                cluster.is_active = True
                cluster.inactivity_ticks = 0
            else:
                cluster.is_active = False
                cluster.inactivity_ticks += 1
                
        # 2. VARREDURA E CÁLCULO SELETIVO ---------------------------------
        total_excitement = 0.0
        nodes_computed_count = 0
        
        for c_name, cluster in self.clusters.items():
            # Aceleração Massiva: Se inativo e não for hora da soneca, pule o laço!
            if not cluster.is_active:
                if cluster.inactivity_ticks % self.CLOCK_NAP_CHECK != 0:
                    continue # Soneca Profunda. O(0) gasto aqui.
                    
                # HORA DA VARREDURA SUPERFICIAL (Soneca Leve O(n/4))
                logger.info(f"💤 Varredura Leve no Cluster Dorminhoco: {c_name}...")
                need = cluster.scan_need()
                if need >= 90.0:
                    logger.warning(f"🚨 [Córtex Analítico] O Cluster Inativo {c_name} reportou abandono Crítico! Solicitando Dopamina...")
                    # Simula um grito por recursos para o Córtex Analítico.
                
                # Só calcula 25% dos nós adormecidos
                nodes_to_calc = max(1, cluster.node_count // 4)
                for i in range(nodes_to_calc):
                    total_excitement += self.nodes_map[c_name][i].fire(climate, cluster.base_affinity)
                nodes_computed_count += nodes_to_calc
                
            else:
                # CLUSTER FOCAL: Calcula 100% dos nós
                for node in self.nodes_map[c_name]:
                    total_excitement += node.fire(climate, cluster.base_affinity)
                nodes_computed_count += cluster.node_count
                
        # Finaliza com a média com base SO no que foi computado.
        # A matemática não dilui nos nós dorminhocos.
        average = total_excitement / nodes_computed_count if nodes_computed_count > 0 else 0
        final_priority_weight = min(100.0, average * 50.0)
        
        # Debug Logs (Pode remover em prod)
        # print(f"Nós Computados este tick: {nodes_computed_count}/200. Economia: {((200-nodes_computed_count)/200)*100}%")
        return final_priority_weight

# Singleton Temporário (Apenas para Benchmark de Laboratório)
# global_tissue = TardigradeTissue()
