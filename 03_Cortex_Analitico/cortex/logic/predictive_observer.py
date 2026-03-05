import json
import logging
import time
from pathlib import Path
from typing import Dict, Any

BASE_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"
MODEL_FILE = CONFIG_DIR / "expectation_model.json"

class PredictiveObserver:
    """
    Motor de Codificacao Preditiva (v2.0).
    Sugerido pelo principio da Minimizacao da Energia Livre.
    """
    _model = {}
    _logger = logging.getLogger("PredictiveObserver")

    @classmethod
    def load_model(cls):
        """Carrega o modelo de expectativas do disco."""
        try:
            if MODEL_FILE.exists():
                cls._model = json.loads(MODEL_FILE.read_text(encoding="utf-8"))
            else:
                cls._model = {}
        except Exception as e:
            cls._logger.error(f"Falha ao carregar expectation_model: {e}")

    @classmethod
    def save_model(cls):
        """Salva o modelo no disco."""
        try:
            MODEL_FILE.write_text(json.dumps(cls._model, indent=2), encoding="utf-8")
        except Exception as e:
            cls._logger.error(f"Falha ao salvar expectation_model: {e}")

    @classmethod
    def get_expectation(cls, module: str, function: str) -> Dict[str, Any]:
        """Retorna o que o sistema espera desta tarefa."""
        if not cls._model:
            cls.load_model()
        
        key = f"{module}.{function}"
        # Padrão se não houver registros: 50ms, status OK
        return cls._model.get(key, {"avg_ms": 50.0, "success_rate": 1.0, "samples": 0})

    @classmethod
    def calculate_surprise(cls, module: str, function: str, actual_ms: float, actual_status: str) -> float:
        """
        Calcula o nivel de 'Surpresa' (Erro de Predicao).
        0.0 = Esperado, 1.0+ = Muito Surpreendente.
        """
        exp = cls.get_expectation(module, function)
        
        # Surpresa baseada em tempo (Latencia inesperada)
        time_surprise = 0.0
        if actual_ms > exp["avg_ms"] * 2: # Mais do que o dobro do tempo medio
            time_surprise = (actual_ms / exp["avg_ms"]) - 1.0
            
        # Surpresa baseada em falha (Status inesperado)
        status_surprise = 0.0
        if actual_status == "ERROR" and exp["success_rate"] > 0.9:
            status_surprise = 2.0 # Erro em algo que costuma funcionar eh muito impactante

        total_surprise = time_surprise + status_surprise
        if total_surprise > 0:
            cls._logger.info(f"💡 Surpresa calculada para {module}.{function}: {total_surprise} (Time: {time_surprise}, Status: {status_surprise})")
        
        # Atualizar o modelo (Aprendizado)
        cls._update_metrics(module, function, actual_ms, actual_status)
        
        return round(total_surprise, 2)

    @classmethod
    def _update_metrics(cls, module: str, function: str, actual_ms: float, actual_status: str):
        """Atualiza medias moveis do modelo de expectativa."""
        key = f"{module}.{function}"
        exp = cls._model.get(key, {"avg_ms": actual_ms, "success_rate": 1.0, "samples": 0})
        
        samples = exp.get("samples", 0)
        # Media movel simples
        new_avg = (exp["avg_ms"] * samples + actual_ms) / (samples + 1)
        
        status_val = 1.0 if actual_status == "OK" else 0.0
        new_success_rate = (exp["success_rate"] * samples + status_val) / (samples + 1)
        
        cls._model[key] = {
            "avg_ms": round(new_avg, 2),
            "success_rate": round(new_success_rate, 3),
            "samples": samples + 1,
            "last_updated": time.time()
        }
        
        # Salva periodicamente ou a cada N amostras
        if (samples + 1) % 5 == 0:
            cls.save_model()
