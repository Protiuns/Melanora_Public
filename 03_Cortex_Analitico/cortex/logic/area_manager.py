import json
import logging
from pathlib import Path
from typing import Dict, List

BASE_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"
POLICY_FILE = CONFIG_DIR / "section_policy.json"
REGISTRY_FILE = CONFIG_DIR / "specialists_registry.json"

class AreaManager:
    """
    Gere as macro-secoes do cerebro (Limbic Gating).
    Permite interromper areas inteiras sem colapsar a estrutura.
    """
    _policy = {}
    _registry = {}
    _logger = logging.getLogger("AreaManager")

    @classmethod
    def load_configs(cls):
        """Carrega as configuracoes de secoes e o registro de especialistas."""
        try:
            if POLICY_FILE.exists():
                cls._policy = json.loads(POLICY_FILE.read_text(encoding="utf-8"))
            if REGISTRY_FILE.exists():
                cls._registry = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
        except Exception as e:
            cls._logger.error(f"Erro ao carregar configuracoes do AreaManager: {e}")

    @classmethod
    def is_allowed(cls, module_name: str) -> bool:
        """Verifica se um modulo especifico pertence a uma secao ativa."""
        if not cls._policy or not cls._registry:
            cls.load_configs()

        # Se o modulo nao estiver no registro, assume que eh Utility e deixa passar por seguranca
        # ou bloqueia se quisermos ser rigidos. Por enquanto, deixa passar.
        if module_name not in cls._registry:
            return True

        module_layer = cls._registry[module_name].get("layer", "Utility")
        
        # Encontra a qual secao essa camada pertence
        for section_id, info in cls._policy.items():
            if module_layer in info.get("layers", []):
                status = info.get("status", "ACTIVE")
                if status in ["ACTIVE", "ALWAYS_ON"]:
                    return True
                else:
                    cls._logger.warning(f"🚫 Acesso negado: Modulo '{module_name}' pertence a secao '{section_id}' que esta '{status}'.")
                    return False

        return True

    @classmethod
    def set_section_status(cls, section_id: str, status: str):
        """Ativa ou desativa uma secao inteira."""
        if not cls._policy:
            cls.load_configs()
            
        if section_id in cls._policy:
            if cls._policy[section_id]["status"] == "ALWAYS_ON":
                cls._logger.error(f"Impossivel alterar status da secao VITAL: {section_id}")
                return False
            
            cls._policy[section_id]["status"] = status
            try:
                POLICY_FILE.write_text(json.dumps(cls._policy, indent=2), encoding="utf-8")
                return True
            except Exception as e:
                 cls._logger.error(f"Erro ao salvar policy: {e}")
        return False
