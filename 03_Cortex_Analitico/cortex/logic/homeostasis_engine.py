"""
🌊 Melanora Homeostasis Engine (v1.0)
Motor de Equilíbrio Interno e Reação Ambiental.
Traduz estados de simbiose (Flow/Caos) em ações físicas e estéticas.
"""

import os
import json
import time
from pathlib import Path

class HomeostasisEngine:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.config_dir = self.base_dir / "config"
        self.state_file = self.config_dir / "neural_state.json"
        self.homeostasis_log = self.base_dir / "logs" / "homeostasis.log"

        # Inscrever-se no GWT para reagir a crises de token
        try:
            from cortex.logic.global_workspace import workspace, EventTypes
            workspace.subscribe(
                "homeostasis_engine",
                self._on_token_critical,
                event_types=[EventTypes.TOKEN_CRITICAL]
            )
        except Exception:
            pass  # GWT pode não estar disponível em testes isolados

    def apply_state_changes(self, mode):
        """Aplica mudanças no ambiente baseadas no modo de simbiose."""
        if mode == "FLOW":
            return self._enter_flow()
        elif mode == "CHAOS":
            return self._enter_chaos()
        else:
            return self._return_to_normal()

    def _enter_flow(self):
        """Ações para o estado de foco profundo."""
        actions = [
            "Otimizando latência de rede neural para foco",
            "Reduzindo verbosidade de logs secundários",
            "Ativando espectro de cor Ametista (Dashboard)"
        ]
        self._log_homeostasis("FLOW_MODE_ACTIVE", actions)
        return {"actions": actions, "theme_hint": "DEEP_PURPLE"}

    def _enter_chaos(self):
        """Ações para o estado de alta pressão/interação desordenada."""
        actions = [
            "Ativando mecanismos de resfriamento térmico (simulado)",
            "Priorizando processos de segurança e integridade",
            "Alerta visual: Entropia Crítica"
        ]
        self._log_homeostasis("CHAOS_MODE_ACTIVE", actions)
        return {"actions": actions, "theme_hint": "NEURAL_RED"}

    def _return_to_normal(self):
        """Ações para o estado estável."""
        return {"actions": ["Monitorando pulso estável"], "theme_hint": "DEFAULT_GREEN"}

    def _log_homeostasis(self, event, actions):
        timestamp = time.ctime()
        log_entry = f"[{timestamp}] {event}: {', '.join(actions)}\n"
        try:
            with open(self.homeostasis_log, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception:
            pass  # Log dir may not exist in tests

    def _on_token_critical(self, event):
        """Callback GWT: reage a crise de tokens com protocolo de caos."""
        self._enter_chaos()
        self._log_homeostasis(
            "TOKEN_CRITICAL_RESPONSE",
            [
                f"Overflow iminente: {event.data.get('usage_ratio', 0):.0%}",
                "Protocolo de crise ativado via GWT",
                "Sugere-se nova sessão"
            ]
        )

def run_homeostasis_check():
    """Função invocada pelo bridge ou API."""
    try:
        with open(Path(__file__).parent.parent.parent / "config" / "neural_state.json", "r") as f:
            state = json.load(f)
        
        mode = state.get("symbiotic_mode", "NORMAL")
        engine = HomeostasisEngine()
        return engine.apply_state_changes(mode)
    except:
        return {"status": "ERROR"}

if __name__ == "__main__":
    print("🌊 Testando Homeostasis Engine...")
    res = run_homeostasis_check()
    print(res)
