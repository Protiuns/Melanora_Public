import time
import logging
from typing import Dict

logger = logging.getLogger("NeuralIrrigation")

class VirtualGland:
    """
    Sistema Endócrino do Córtex Analítico.
    Em vez de recalcular pesos de rede neural (caro), este módulo altera o "clima" global (barato).
    Os micro-agentes leem o clima antes de agir, mudando drasticamente seus comportamentos nulos.
    """
    def __init__(self):
        # Níveis hormonais flutuam de 0.0 (Ausente) a 1.0 (Saturação Máxima)
        self.fluids = {
            "adrenaline": 0.0,   # Instiga prioridades de Fuga, Voo e Movimento brusco
            "dopamine": 0.0,     # Instiga o Axiom Associator a buscar padrões profundos (Curiosidade)
            "serotonin": 0.5     # Estabilizador base. Alto = Manutenção, Limpeza, Homeostase
        }
        
        self.last_injection_time = time.time()
        self.metabolic_decay_rate = 0.05  # Quanto o hormônio decai por segundo até o estado base

    def inject(self, hormone: str, amount: float):
        """Injeta uma concentração química no sistema."""
        if hormone in self.fluids:
            # Nunca passa de 1.0
            self.fluids[hormone] = min(1.0, self.fluids[hormone] + amount)
            self.last_injection_time = time.time()
            logger.info(f"💉 Irrigação Ativa: +{amount:.2f} {hormone.upper()} (Saturação: {self.fluids[hormone]:.2f})")

    def metabolize(self):
        """
        Decaimento metabólico.
        Restaura o equilíbrio vagarosamente se não houver novos impulsos.
        """
        now = time.time()
        elapsed = now - self.last_injection_time
        
        if elapsed > 1.0: # Roda decaimento se passou de 1 segundo
            for hormone in self.fluids:
                if hormone == "serotonin":
                    # Serotonina tende a voltar para 0.5 (Base)
                    if self.fluids[hormone] > 0.5:
                        self.fluids[hormone] = max(0.5, self.fluids[hormone] - self.metabolic_decay_rate)
                    elif self.fluids[hormone] < 0.5:
                        self.fluids[hormone] = min(0.5, self.fluids[hormone] + self.metabolic_decay_rate)
                else:
                    # Adrenalina e Dopamina tendem a 0.0
                    self.fluids[hormone] = max(0.0, self.fluids[hormone] - self.metabolic_decay_rate)
            
            self.last_injection_time = now

    def extract_climate(self) -> Dict[str, float]:
        """
        Retorna a leitura instantânea do clima químico atual da rede.
        Nós nulos usarão isso para calcular multiplicadores (Ex: base * (1 + adrenaline))
        """
        self.metabolize()
        return self.fluids.copy()

# Singleton para a ponte neural acessar o mesmo banho químico
global_gland = VirtualGland()
