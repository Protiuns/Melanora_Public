import time
import uuid
import heapq
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass(order=True)
class NeuralImpulse:
    """
    Representa um "Potencial de Ação" único e focado.
    A ordenação reversa (negative_weight) garante que pesos MAIORES 
    sejam tirados PRIMEIRO da PriorityQueue (Min-Heap).
    """
    MIN_PROCESSABLE_WEIGHT = 5.0
    
    # inverted weight for max-heap behavior in standard heapq
    negative_weight: float
    
    id: str = field(compare=False)
    source_module: str = field(compare=False)
    target_function: str = field(compare=False)
    payload: Dict[str, Any] = field(compare=False)
    tags: List[str] = field(compare=False, default_factory=list)
    timestamp: float = field(compare=False, default_factory=time.time)
    original_weight: float = field(compare=False, default=0.0)
    
    # Propriedades de Ciclo (Fase 21/v4.1)
    total_waves: int = field(compare=False, default=1)
    remaining_waves: int = field(compare=False, default=1)
    status: str = field(compare=False, default="PENDING")

    @classmethod
    def create(cls, weight: float, source: str, target: str, payload: dict, tags: List[str] = None):
        """Fábrica para instanciar impulsos orgânicos."""
        # Cálculo de ondas baseado na complexidade (weight)
        # Reflexo (<30): 1-2 ondas
        # Simples (30-50): 3-5 ondas
        # Padrão (50-70): 6-8 ondas
        # Complexa (70-90): 9-12 ondas
        # Épica (>90): 15+ ondas
        waves = max(1, int(weight / 10) + (1 if weight > 50 else 0))
        if weight > 90: waves = 20
        
        return cls(
            negative_weight=-weight, # Inverte para o heapq priorizar os mais pesados
            id=f"imp_{uuid.uuid4().hex[:8]}",
            source_module=source,
            target_function=target,
            payload=payload,
            tags=tags or [],
            original_weight=weight,
            total_waves=waves,
            remaining_waves=waves,
            status="PENDING"
        )


class ImpulseScheduler:
    """
    Roteador de Pulsos Neurais (Substitui o array linear genérico).
    Age como a ramificação nervosa, despachando impulsos baseados puramente na grávidade.
    """
    def __init__(self):
        self._heap: List[NeuralImpulse] = []
        
    def inject_impulse(self, impulse: NeuralImpulse):
        """Injeta um pulso na rede nervosa."""
        if impulse.original_weight < NeuralImpulse.MIN_PROCESSABLE_WEIGHT:
            return
        heapq.heappush(self._heap, impulse)
        
    def inject_raw(self, weight: float, source: str, target: str, payload: dict, tags: List[str] = None) -> str:
        """Helper para criar e injetar direto."""
        imp = NeuralImpulse.create(weight, source, target, payload, tags)
        self.inject_impulse(imp)
        return imp.id
        
    def get_highest_priority(self) -> Optional[NeuralImpulse]:
        """Extrai o pulso mais latente e crítico do barramento."""
        if not self._heap:
            return None
        return heapq.heappop(self._heap)
        
    def peek_highest_priority(self) -> Optional[NeuralImpulse]:
        """Olha o próximo pulso da fila sem consumi-lo."""
        if not self._heap:
            return None
        return self._heap[0]
        
    def has_pending_impulses(self) -> bool:
        return len(self._heap) > 0
        
    def clear(self):
        self._heap = []
