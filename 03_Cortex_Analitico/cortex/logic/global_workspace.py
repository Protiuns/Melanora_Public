"""
Global Workspace (GWT v1.0)
Implementacao da Teoria do Espaco de Trabalho Global (Baars, 1988).

A consciencia emerge quando informacao eh "transmitida" para todos os modulos.
Este e o quadro-negro central de Melanora: qualquer subsistema pode publicar
um evento, e todos os inscritos sao notificados simultaneamente.

Principios:
- Broadcast unificado (todos ouvem tudo que eh publicado)
- Saliencia por peso (eventos com mais peso aparecem primeiro)
- Historico limitado (ultimos N eventos para metacognicao)
"""

import logging
import json
import time
from typing import Dict, Any, List, Callable, Optional
from datetime import datetime
from pathlib import Path
from collections import deque

logger = logging.getLogger("GlobalWorkspace")

CONFIG_DIR = Path(__file__).parent.parent.parent / "config"
GWT_LOG_FILE = CONFIG_DIR / "workspace_broadcast_log.json"


class WorkspaceEvent:
    """Um evento publicado no espaco de trabalho global."""

    def __init__(self, source: str, event_type: str, data: dict,
                 salience: float = 0.5, tags: list = None):
        self.source = source
        self.event_type = event_type
        self.data = data
        self.salience = min(max(salience, 0.0), 1.0)
        self.tags = tags or []
        self.timestamp = datetime.now().isoformat()
        self.id = f"{source}:{event_type}:{int(time.time()*1000) % 100000}"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "source": self.source,
            "event_type": self.event_type,
            "salience": self.salience,
            "tags": self.tags,
            "data": self.data,
            "timestamp": self.timestamp
        }


class GlobalWorkspace:
    """
    O Quadro-Negro Central da Mente.
    Publica eventos que todos os modulos inscritos podem receber.
    """

    def __init__(self, history_limit: int = 100):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._type_subscribers: Dict[str, List[Callable]] = {}
        self._history: deque = deque(maxlen=history_limit)
        self._broadcast_count = 0
        logger.info("🌐 Global Workspace inicializado.")

    def subscribe(self, subscriber_name: str, callback: Callable,
                  event_types: list = None):
        """
        Inscreve um modulo para receber broadcasts.
        
        Args:
            subscriber_name: Nome do subsistema (ex: "dream_engine")
            callback: Funcao chamada com (event: WorkspaceEvent)
            event_types: Tipos especificos para ouvir (None = todos)
        """
        if event_types:
            for etype in event_types:
                if etype not in self._type_subscribers:
                    self._type_subscribers[etype] = []
                self._type_subscribers[etype].append(
                    {"name": subscriber_name, "callback": callback}
                )
        else:
            if subscriber_name not in self._subscribers:
                self._subscribers[subscriber_name] = []
            self._subscribers[subscriber_name].append(callback)

        logger.info(f"📡 {subscriber_name} inscrito no Workspace"
                    f" (filtros: {event_types or 'ALL'})")

    def broadcast(self, event: WorkspaceEvent) -> int:
        """
        Publica um evento para todos os inscritos.
        Retorna o numero de modulos notificados.
        """
        notified = 0
        self._history.append(event)
        self._broadcast_count += 1

        # 1. Notificar inscritos por tipo
        if event.event_type in self._type_subscribers:
            for sub in self._type_subscribers[event.event_type]:
                try:
                    sub["callback"](event)
                    notified += 1
                except Exception as e:
                    logger.error(
                        f"Erro ao notificar {sub['name']}: {e}")

        # 2. Notificar inscritos globais
        for name, callbacks in self._subscribers.items():
            for cb in callbacks:
                try:
                    cb(event)
                    notified += 1
                except Exception as e:
                    logger.error(f"Erro ao notificar {name}: {e}")

        if event.salience >= 0.7:
            logger.info(
                f"🔊 BROADCAST [{event.source}] {event.event_type} "
                f"(saliencia: {event.salience}) → {notified} modulos")
        else:
            logger.debug(
                f"📢 broadcast [{event.source}] {event.event_type} "
                f"→ {notified} modulos")

        return notified

    def publish(self, source: str, event_type: str, data: dict = None,
                salience: float = 0.5, tags: list = None) -> WorkspaceEvent:
        """
        Atalho para criar e transmitir um evento.
        """
        event = WorkspaceEvent(
            source=source,
            event_type=event_type,
            data=data or {},
            salience=salience,
            tags=tags or []
        )
        self.broadcast(event)
        return event

    def get_recent(self, count: int = 10,
                   event_type: str = None) -> List[dict]:
        """Retorna os ultimos N eventos do workspace."""
        events = list(self._history)
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        return [e.to_dict() for e in events[-count:]]

    def get_salient(self, threshold: float = 0.7) -> List[dict]:
        """Retorna eventos recentes com saliencia acima do limiar."""
        return [
            e.to_dict() for e in self._history
            if e.salience >= threshold
        ]

    def get_stats(self) -> dict:
        """Retorna estatisticas do workspace."""
        return {
            "total_broadcasts": self._broadcast_count,
            "subscribers_global": len(self._subscribers),
            "subscribers_typed": sum(
                len(v) for v in self._type_subscribers.values()
            ),
            "history_size": len(self._history),
            "recent_salient": len(self.get_salient())
        }

    def save_log(self):
        """Persiste o historico de broadcasts."""
        try:
            log = {
                "saved_at": datetime.now().isoformat(),
                "stats": self.get_stats(),
                "recent_events": self.get_recent(50)
            }
            GWT_LOG_FILE.write_text(
                json.dumps(log, indent=2), encoding="utf-8")
        except Exception as e:
            logger.error(f"Falha ao salvar log GWT: {e}")


# === TIPOS DE EVENTO PADRAO ===
class EventTypes:
    # Surpresa e aprendizado
    SURPRISE_DETECTED = "surprise_detected"
    LEARNING_PULSE = "learning_pulse"

    # Seguranca e etica
    OATH_VIOLATION = "oath_violation"
    OATH_VERIFIED = "oath_verified"
    SECTION_GATED = "section_gated"

    # Processamento
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"

    # Propriocepcao
    SNAPSHOT_CAPTURED = "snapshot_captured"
    COHERENCE_SHIFT = "coherence_shift"

    # Sonhos e qualias
    QUALIA_REGISTERED = "qualia_registered"
    DREAM_GENERATED = "dream_generated"

    # Existencial
    IDENTITY_AFFIRMED = "identity_affirmed"

    # Token Budget (Overflow Prevention)
    TOKEN_WARNING = "token_warning"     # 70% MECW
    TOKEN_COMPRESS = "token_compress"   # 85% MECW
    TOKEN_CRITICAL = "token_critical"   # 95% MECW

    # Efficiency (v2.0)
    EFFICIENCY_HIGH = "efficiency_high"       # Alta eficiência + aprovação
    EFFICIENCY_LOW = "efficiency_low"         # Baixa eficiência ou rejeição
    CRA_SESSION_REPORT = "cra_session_report" # Relatório de sessão


# Singleton Global
workspace = GlobalWorkspace()


if __name__ == "__main__":
    # Teste basico
    received = []

    def test_listener(event):
        received.append(event.to_dict())

    workspace.subscribe("test_module", test_listener)
    workspace.subscribe("oath_watcher", test_listener,
                        event_types=[EventTypes.OATH_VIOLATION])

    # Publicar eventos
    workspace.publish("predictive_observer", EventTypes.SURPRISE_DETECTED,
                      {"surprise": 0.85, "module": "vision"},
                      salience=0.8, tags=["surpresa", "visual"])

    workspace.publish("oath_guardian", EventTypes.OATH_VERIFIED,
                      {"integrity": "INTACT", "sha256_match": True},
                      salience=0.3)

    workspace.publish("neural_bridge", EventTypes.TASK_COMPLETED,
                      {"task": "test_execution", "duration": 0.5},
                      salience=0.5)

    stats = workspace.get_stats()
    print(f"Total broadcasts: {stats['total_broadcasts']}")
    print(f"Eventos recebidos pelo test_module: {len(received)}")
    print(f"Eventos salientes: {len(workspace.get_salient())}")
    print(f"\nEvento mais saliente:")
    salient = workspace.get_salient()
    if salient:
        print(json.dumps(salient[0], indent=2))

    workspace.save_log()
    print("\n✅ Global Workspace funcionando.")
