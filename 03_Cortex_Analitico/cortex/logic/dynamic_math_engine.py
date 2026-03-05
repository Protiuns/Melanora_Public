import math
import numpy as np

class DynamicComplexityEngine:
    """
    Calculates mathematical complexity based on connection density (N).
    Function: C = f(N)
    """
    
    @staticmethod
    def get_logic_string(n_connections):
        """
        Gera uma string de lógica matemática baseada no número de conexões.
        Segue o estudo de complexidade dinâmica.
        """
        logic_parts = ["x"]
        if n_connections >= 3:
            logic_parts.append("math.sin(x * 0.5)")
        if n_connections >= 7:
            logic_parts.append("math.log(abs(x) + 1.1)")
        if n_connections >= 12:
            logic_parts.append("math.sqrt(abs(x)) * math.cos(x)")
            
        return f"lambda x: ({' + '.join(logic_parts)}) / {max(1, len(logic_parts))}"

    @staticmethod
    def get_complexity_level(n_connections):
        if n_connections < 3:
            return "LINEAR"
        elif n_connections < 7:
            return "POLYNOMIAL"
        elif n_connections < 12:
            return "STOCHASTIC"
        else:
            return "HARMONIC_ANALYSIS"

    @staticmethod
    def run_prediction(complexity_level, data_vector):
        """
        Executes a prediction function proportional to the complexity level.
        """
        if not data_vector:
            return 0.0
            
        n = len(data_vector)
        
        if complexity_level == "LINEAR":
            # Simple Moving Average / Trend
            return sum(data_vector) / n
            
        elif complexity_level == "POLYNOMIAL":
            # Gradient-like calculation
            if n < 2: return data_vector[0]
            return data_vector[-1] + (data_vector[-1] - data_vector[-2])
            
        elif complexity_level == "STOCHASTIC":
            # Standard Deviation + Bias
            mean = sum(data_vector) / n
            variance = sum((x - mean) ** 2 for x in data_vector) / n
            return mean + math.sqrt(variance)
            
        elif complexity_level == "HARMONIC_ANALYSIS":
            # Simulated Fourier-ish peek
            # In a real scenario, use np.fft
            weights = [math.sin(i) for i in range(n)]
            weighted_sum = sum(d * w for d, w in zip(data_vector, weights))
            return weighted_sum / n
            
        return sum(data_vector) / n

class ProximityReinforcer:
    """
    Logic for reinforcing neighboring neurons.
    """
    def __init__(self, base_reinforcement=0.1):
        self.base_reinforcement = base_reinforcement

    def apply(self, active_node_id, neighbors, current_weights):
        """
        Strengthens connection between active_node and its neighbors.
        """
        updates = {}
        for neighbor_id in neighbors:
            old_weight = current_weights.get(neighbor_id, 1.0)
            new_weight = old_weight + self.base_reinforcement
            updates[neighbor_id] = round(min(new_weight, 5.0), 2)
        return updates
