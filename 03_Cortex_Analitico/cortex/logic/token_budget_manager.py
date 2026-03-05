"""
🛡️ Token Budget Manager v2.0 — Guardião de Contexto + Eficiência
=================================================================
Auto-regulação do consumo de tokens E medição de eficiência por resultado.

Análogo ao PremotorCortex (que governa balanço químico),
este módulo governa o balanço de tokens na janela de contexto.

Arquitetura:
  Layer 1: TokenCounter       — Conta tokens em tempo real
  Layer 2: BudgetPolicy       — Define limites por modo (CREATIVE/FOCUSED/CRITICAL)
  Layer 3: ImportanceAllocator — Distribui budget por ressonância
  Layer 4: OverflowGuardian    — Monitora consumo e dispara ações preventivas
  Layer 5: ResultTracker       — Registra resultados por tarefa [v2.0]
  Layer 6: EfficiencyScorer    — Calcula valor/token por tarefa [v2.0]
  Layer 7: FeedbackLoop        — Ajusta pesos sinápticos por eficiência [v2.0]

Integração:
  - Publica TOKEN_WARNING/COMPRESS/CRITICAL no GWT
  - Publica EFFICIENCY_HIGH/LOW e CRA_SESSION_REPORT no GWT
  - Homeostasis Engine reage a TOKEN_CRITICAL com protocolo de crise
  - Plasticidade Sináptica: LTP/LTD informada por eficiência
"""

import json
import logging
import math
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from cortex.logic.global_workspace import workspace, EventTypes

logger = logging.getLogger("TokenBudgetManager")

BASE_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"
BUDGET_CONFIG_FILE = CONFIG_DIR / "token_budget_config.json"


# ═══════════════════════════════════════════════════════════════════
#  Data Structures
# ═══════════════════════════════════════════════════════════════════

class GuardianLevel(Enum):
    SAFE = "SAFE"
    WARNING = "WARNING"
    COMPRESS = "COMPRESS"
    CRITICAL = "CRITICAL"


@dataclass
class GuardianAction:
    """Resultado de uma verificação do OverflowGuardian."""
    level: GuardianLevel
    usage_ratio: float          # 0.0 - 1.0
    tokens_used: int
    tokens_budget: int
    message: str
    should_compress: bool = False
    should_block: bool = False


@dataclass
class AgentBudget:
    """Orçamento alocado para um agente específico."""
    agent_name: str
    score: float
    allocated_tokens: int
    percentage: float           # % do total


@dataclass
class TaskResult:
    """Resultado de uma tarefa registrada pelo ResultTracker."""
    task_name: str
    tokens_used: int
    timestamp: float
    result_type: str            # "test_pass", "artifact_created", "user_approved", "user_rejected"
    signals: Dict[str, Any] = field(default_factory=dict)
    efficiency_score: float = 0.0
    source_agent: str = "unknown"


# ═══════════════════════════════════════════════════════════════════
#  Layer 1: TokenCounter
# ═══════════════════════════════════════════════════════════════════

class TokenCounter:
    """
    Conta tokens por heurística ou tiktoken (se disponível).
    
    PT-BR: ~4 caracteres por token (estimativa conservadora).
    Se tiktoken estiver instalado, usa-o para contagem precisa.
    """

    def __init__(self, chars_per_token: int = 4):
        self._chars_per_token = chars_per_token
        self._tiktoken_encoder = None
        self._try_load_tiktoken()

    def _try_load_tiktoken(self):
        """Tenta carregar tiktoken opcionalmente."""
        try:
            import tiktoken
            self._tiktoken_encoder = tiktoken.get_encoding("cl100k_base")
            logger.info("📊 TokenCounter usando tiktoken (precisão alta).")
        except ImportError:
            logger.info(
                f"📊 TokenCounter usando heurística "
                f"({self._chars_per_token} chars/token)."
            )

    def count(self, text: str) -> int:
        """Conta tokens em uma string."""
        if not text:
            return 0
        if self._tiktoken_encoder:
            return len(self._tiktoken_encoder.encode(text))
        return max(1, len(text) // self._chars_per_token)

    def count_json(self, data: Any) -> int:
        """Conta tokens em uma estrutura JSON serializada."""
        try:
            text = json.dumps(data, ensure_ascii=False)
            return self.count(text)
        except (TypeError, ValueError):
            return 0

    def count_file(self, path: Path) -> int:
        """Conta tokens em um arquivo de texto."""
        try:
            text = path.read_text(encoding="utf-8")
            return self.count(text)
        except Exception:
            return 0

    @property
    def method(self) -> str:
        """Retorna o método de contagem em uso."""
        return "tiktoken" if self._tiktoken_encoder else "heuristic"


# ═══════════════════════════════════════════════════════════════════
#  Layer 2: BudgetPolicy
# ═══════════════════════════════════════════════════════════════════

class BudgetPolicy:
    """
    Define limites de tokens por modo operacional.
    
    Modos mapeados do APT (Adaptive Pruning Threshold):
      CREATIVE → 80% do MECW (brainstorm, refatoração)
      FOCUSED  → 60% do MECW (execução, correção)
      CRITICAL → 40% do MECW (auditoria, integridade)
    """

    def __init__(self, config: dict):
        self._config = config
        self._mecw = config.get("mecw_estimate", 600000)
        self._modes = config.get("modes", {})
        self._thresholds = config.get("guardian_thresholds", {
            "warning": 0.70, "compress": 0.85, "block": 0.95
        })
        self._min_per_agent = config.get("min_budget_per_agent", 500)

    def get_active_mode(self) -> str:
        """Retorna o modo ativo."""
        return self._config.get("active_mode", "FOCUSED")

    def get_total_budget(self, mode: str = None) -> int:
        """Retorna o orçamento total de tokens para o modo dado."""
        mode = mode or self.get_active_mode()
        mode_config = self._modes.get(mode, {"budget_ratio": 0.6})
        ratio = mode_config.get("budget_ratio", 0.6)
        return int(self._mecw * ratio)

    def get_guardian_thresholds(self) -> Dict[str, float]:
        """Retorna os limiares de proteção."""
        return self._thresholds.copy()

    def get_min_per_agent(self) -> int:
        """Retorna o mínimo de tokens por agente."""
        return self._min_per_agent

    @property
    def mecw(self) -> int:
        """Maximum Effective Context Window estimado."""
        return self._mecw


# ═══════════════════════════════════════════════════════════════════
#  Layer 3: ImportanceAllocator
# ═══════════════════════════════════════════════════════════════════

class ImportanceAllocator:
    """
    Distribui o orçamento de tokens entre agentes/componentes
    proporcionalmente à importância (Score de Ressonância + Saliência GWT).
    
    Fórmula:
      Budget(a) = total_budget × (score(a) / Σ scores)
    """

    def __init__(self, min_per_agent: int = 500):
        self._min_per_agent = min_per_agent

    def allocate(
        self,
        agents: List[Dict[str, float]],
        total_budget: int
    ) -> List[AgentBudget]:
        """
        Distribui tokens entre agentes.
        
        Args:
            agents: Lista de dicts {"name": str, "score": float}
            total_budget: Total de tokens disponíveis
        
        Returns:
            Lista de AgentBudget com alocações
        """
        if not agents:
            return []

        # Calcular soma total dos scores
        total_score = sum(a.get("score", 0.1) for a in agents)
        if total_score == 0:
            total_score = len(agents) * 0.1  # fallback: distribuição igual

        allocations = []
        for agent in agents:
            name = agent.get("name", "unknown")
            score = agent.get("score", 0.1)

            # Proporcional ao score
            raw_budget = int(total_budget * (score / total_score))

            # Garantir mínimo
            allocated = max(self._min_per_agent, raw_budget)

            percentage = (allocated / total_budget * 100) if total_budget > 0 else 0

            allocations.append(AgentBudget(
                agent_name=name,
                score=score,
                allocated_tokens=allocated,
                percentage=round(percentage, 1)
            ))

        # Se a soma das alocações excede o budget (por causa dos mínimos),
        # reduzir proporcionalmente os maiores
        total_allocated = sum(a.allocated_tokens for a in allocations)
        if total_allocated > total_budget and len(allocations) > 1:
            excess = total_allocated - total_budget
            # Ordenar por alocação (maior primeiro) e reduzir
            sorted_allocs = sorted(
                allocations, key=lambda a: a.allocated_tokens, reverse=True
            )
            for alloc in sorted_allocs:
                if excess <= 0:
                    break
                reduction = min(
                    excess,
                    alloc.allocated_tokens - self._min_per_agent
                )
                if reduction > 0:
                    alloc.allocated_tokens -= reduction
                    excess -= reduction

        return allocations

    def allocate_with_gwt_bonus(
        self,
        agents: List[Dict[str, float]],
        total_budget: int
    ) -> List[AgentBudget]:
        """
        Aloca com bônus de saliência do GWT.
        Agentes com eventos recentes de alta saliência ganham +15% de score.
        """
        salient_events = workspace.get_salient(threshold=0.7)
        salient_sources = {e["source"] for e in salient_events}

        # Aplicar bônus
        boosted = []
        for agent in agents:
            score = agent.get("score", 0.1)
            name = agent.get("name", "unknown")
            if name in salient_sources:
                score *= 1.15  # +15% bônus de saliência
            boosted.append({"name": name, "score": score})

        return self.allocate(boosted, total_budget)


# ═══════════════════════════════════════════════════════════════════
#  Layer 4: OverflowGuardian
# ═══════════════════════════════════════════════════════════════════

class OverflowGuardian:
    """
    Monitora o consumo de tokens e dispara ações preventivas.
    
    Limiares:
      70% MECW → WARNING (alerta amarelo)
      85% MECW → COMPRESS (compressão forçada do histórico)
      95% MECW → CRITICAL (bloqueio, salvar estado, notificar)
    """

    def __init__(self, thresholds: Dict[str, float]):
        self._thresholds = thresholds
        self._last_level = GuardianLevel.SAFE
        self._alert_count = 0

    def check(self, current_tokens: int, total_budget: int) -> GuardianAction:
        """
        Verifica o nível de consumo e retorna a ação apropriada.
        """
        if total_budget <= 0:
            return GuardianAction(
                level=GuardianLevel.SAFE, usage_ratio=0.0,
                tokens_used=current_tokens, tokens_budget=total_budget,
                message="Budget não configurado."
            )

        ratio = current_tokens / total_budget
        warning_t = self._thresholds.get("warning", 0.70)
        compress_t = self._thresholds.get("compress", 0.85)
        block_t = self._thresholds.get("block", 0.95)

        if ratio >= block_t:
            level = GuardianLevel.CRITICAL
            message = (
                f"🔴 BLOQUEIO: {ratio:.0%} do budget consumido "
                f"({current_tokens:,}/{total_budget:,} tokens). "
                f"Salvar estado e sugerir nova sessão."
            )
            should_compress = True
            should_block = True

        elif ratio >= compress_t:
            level = GuardianLevel.COMPRESS
            message = (
                f"🟠 COMPRESSÃO: {ratio:.0%} do budget consumido "
                f"({current_tokens:,}/{total_budget:,} tokens). "
                f"Comprimindo histórico GWT."
            )
            should_compress = True
            should_block = False

        elif ratio >= warning_t:
            level = GuardianLevel.WARNING
            message = (
                f"⚠️ ALERTA: {ratio:.0%} do budget consumido "
                f"({current_tokens:,}/{total_budget:,} tokens). "
                f"Considerar comprimir artefatos antigos."
            )
            should_compress = False
            should_block = False

        else:
            level = GuardianLevel.SAFE
            message = (
                f"✅ SEGURO: {ratio:.0%} do budget "
                f"({current_tokens:,}/{total_budget:,} tokens)."
            )
            should_compress = False
            should_block = False

        # Emitir evento GWT se o nível mudou ou piorou
        if level != GuardianLevel.SAFE and level != self._last_level:
            self._emit_gwt_event(level, ratio, current_tokens, total_budget)
            self._alert_count += 1

        self._last_level = level

        return GuardianAction(
            level=level,
            usage_ratio=round(ratio, 4),
            tokens_used=current_tokens,
            tokens_budget=total_budget,
            message=message,
            should_compress=should_compress,
            should_block=should_block,
        )

    def _emit_gwt_event(
        self, level: GuardianLevel,
        ratio: float, used: int, budget: int
    ):
        """Publica alertas no Global Workspace."""
        event_map = {
            GuardianLevel.WARNING: EventTypes.TOKEN_WARNING,
            GuardianLevel.COMPRESS: EventTypes.TOKEN_COMPRESS,
            GuardianLevel.CRITICAL: EventTypes.TOKEN_CRITICAL,
        }
        event_type = event_map.get(level)
        if event_type:
            salience = min(1.0, ratio + 0.1)  # Mais urgente = mais saliente
            workspace.publish(
                source="token_budget_manager",
                event_type=event_type,
                data={
                    "usage_ratio": ratio,
                    "tokens_used": used,
                    "tokens_budget": budget,
                    "level": level.value,
                    "alert_number": self._alert_count + 1,
                },
                salience=salience,
                tags=["token_budget", "overflow_prevention"]
            )
            logger.warning(
                f"🛡️ [GUARDIAN] Evento {event_type} emitido "
                f"(saliência: {salience:.2f})"
            )

    def compress_gwt_history(self, keep_recent: int = 5) -> int:
        """
        Comprime o histórico do GWT, mantendo apenas os N mais recentes.
        Retorna o número de eventos removidos.
        """
        history = list(workspace._history)
        if len(history) <= keep_recent:
            return 0

        removed = len(history) - keep_recent
        workspace._history.clear()
        for event in history[-keep_recent:]:
            workspace._history.append(event)

        logger.info(
            f"🗜️ Histórico GWT comprimido: {removed} eventos removidos, "
            f"{keep_recent} mantidos."
        )
        return removed

    @property
    def alert_count(self) -> int:
        return self._alert_count

    @property
    def last_level(self) -> GuardianLevel:
        return self._last_level


# ═══════════════════════════════════════════════════════════════════
#  Orchestrator: TokenBudgetManager
# ═══════════════════════════════════════════════════════════════════

class TokenBudgetManager:
    """
    Orquestrador central da gestão de orçamento de tokens.
    
    Uso:
        result = budget_manager.evaluate(current_context_text)
        if result.should_block:
            # Salvar estado e notificar usuário
        elif result.should_compress:
            budget_manager.compress()
    """

    def __init__(self):
        self._config = self._load_config()
        self.counter = TokenCounter(
            chars_per_token=self._config.get("chars_per_token", 4)
        )
        self.policy = BudgetPolicy(self._config)
        self.allocator = ImportanceAllocator(
            min_per_agent=self.policy.get_min_per_agent()
        )
        self.guardian = OverflowGuardian(
            thresholds=self.policy.get_guardian_thresholds()
        )

        # v2.0: Efficiency components
        self.results = ResultTracker()
        self.scorer = EfficiencyScorer()
        self.feedback = FeedbackLoop()

        # Tracking acumulativo
        self._tracked_tokens = 0
        self._tracking_log = []

        logger.info(
            f"🛡️ TokenBudgetManager v2.0 inicializado. "
            f"MECW={self.policy.mecw:,} | "
            f"Modo={self.policy.get_active_mode()} | "
            f"Budget={self.policy.get_total_budget():,} tokens | "
            f"Counter={self.counter.method}"
        )

    def _load_config(self) -> dict:
        """Carrega token_budget_config.json."""
        try:
            if BUDGET_CONFIG_FILE.exists():
                return json.loads(
                    BUDGET_CONFIG_FILE.read_text(encoding="utf-8")
                )
        except Exception as e:
            logger.error(f"Erro ao carregar token_budget_config: {e}")
        return {
            "mecw_estimate": 600000,
            "active_mode": "FOCUSED",
            "modes": {"FOCUSED": {"budget_ratio": 0.6}},
            "guardian_thresholds": {
                "warning": 0.70, "compress": 0.85, "block": 0.95
            },
            "chars_per_token": 4,
            "min_budget_per_agent": 500
        }

    # ─── Core Operations ───────────────────────────────────────────

    def track(self, text: str, source: str = "unknown") -> int:
        """
        Adiciona tokens ao tracking acumulativo.
        Retorna o total acumulado.
        """
        tokens = self.counter.count(text)
        self._tracked_tokens += tokens
        self._tracking_log.append({
            "source": source,
            "tokens": tokens,
            "cumulative": self._tracked_tokens
        })
        return self._tracked_tokens

    def evaluate(self, current_tokens: int = None) -> GuardianAction:
        """
        Avalia o estado atual do orçamento.
        Se current_tokens não for fornecido, usa o tracking acumulativo.
        """
        tokens = current_tokens if current_tokens is not None else self._tracked_tokens
        budget = self.policy.get_total_budget()
        return self.guardian.check(tokens, budget)

    def evaluate_text(self, text: str) -> GuardianAction:
        """
        Avalia um texto diretamente (conta + verifica).
        """
        tokens = self.counter.count(text)
        budget = self.policy.get_total_budget()
        return self.guardian.check(tokens, budget)

    def compress(self) -> int:
        """Comprime o histórico do GWT."""
        keep = self._config.get("gwt_history_compress_to", 5)
        return self.guardian.compress_gwt_history(keep_recent=keep)

    def allocate_for_agents(
        self, agents: List[Dict[str, float]]
    ) -> List[AgentBudget]:
        """
        Distribui o budget entre agentes com bônus GWT.
        """
        budget = self.policy.get_total_budget()
        return self.allocator.allocate_with_gwt_bonus(agents, budget)

    # ─── v2.0: Efficiency Operations ────────────────────────────────

    def record_result(
        self,
        task_name: str,
        tokens_used: int,
        result_type: str,
        signals: Dict[str, Any] = None,
        source_agent: str = "unknown"
    ) -> Dict[str, Any]:
        """
        Registra resultado, calcula eficiência, e ajusta pesos.
        Pipeline completo: track → score → feedback.

        Returns:
            {"result": TaskResult, "efficiency": float, "adjustment": dict}
        """
        # 1. Registrar resultado
        result = self.results.record(
            task_name, tokens_used, result_type, signals, source_agent
        )

        # 2. Calcular eficiência
        efficiency = self.scorer.score(result)

        # 3. Aplicar feedback sináptico
        adjustment = self.feedback.apply(
            source_agent, efficiency, result_type
        )

        logger.info(
            f"📊 [EFFICIENCY] {task_name}: {tokens_used:,} tokens → "
            f"eff={efficiency:.3f} | {result_type}"
        )

        return {
            "result": result,
            "efficiency": round(efficiency, 4),
            "adjustment": adjustment,
        }

    def session_report(self) -> Dict[str, Any]:
        """Gera relatório de eficiência da sessão atual."""
        return self.scorer.session_report(self.results.session_results)

    # ─── Status & Reporting ────────────────────────────────────────

    def get_status(self) -> Dict[str, Any]:
        """Retorna o estado completo do budget manager."""
        budget = self.policy.get_total_budget()
        ratio = (
            self._tracked_tokens / budget
            if budget > 0 else 0.0
        )
        session = self.results.session_results
        return {
            "tracked_tokens": self._tracked_tokens,
            "total_budget": budget,
            "usage_ratio": round(ratio, 4),
            "usage_percent": f"{ratio:.1%}",
            "mode": self.policy.get_active_mode(),
            "mecw": self.policy.mecw,
            "counter_method": self.counter.method,
            "guardian_level": self.guardian.last_level.value,
            "alerts_emitted": self.guardian.alert_count,
            "tracking_entries": len(self._tracking_log),
            "session_results": len(session),
            "session_cra": self.scorer.session_cra(session) if session else "N/A",
            "synaptic_weights": self.feedback.get_all_weights(),
        }

    def reset_tracking(self):
        """Reseta o tracking acumulativo (ex: nova sessão)."""
        self._tracked_tokens = 0
        self._tracking_log = []
        logger.info("🔄 Tracking de tokens resetado.")

    @property
    def tokens_used(self) -> int:
        return self._tracked_tokens

    @property
    def tokens_remaining(self) -> int:
        return max(0, self.policy.get_total_budget() - self._tracked_tokens)


# ═══════════════════════════════════════════════════════════════════
#  Layer 5: ResultTracker (v2.0)
# ═══════════════════════════════════════════════════════════════════

class ResultTracker:
    """
    Registra resultados de cada tarefa com seus tokens gastos.
    Persiste em efficiency_history.json para análise entre sessões.
    """

    def __init__(self, max_history: int = 50):
        self._results: List[TaskResult] = []
        self._max_history = max_history
        self._history_file = CONFIG_DIR / "efficiency_history.json"
        self._load_history()

    def _load_history(self):
        """Carrega histórico de sessões anteriores."""
        try:
            if self._history_file.exists():
                data = json.loads(
                    self._history_file.read_text(encoding="utf-8")
                )
                for entry in data.get("results", [])[-self._max_history:]:
                    self._results.append(TaskResult(**entry))
        except Exception:
            pass  # Histórico corrompido? Começa limpo.

    def _save_history(self):
        """Persiste o histórico."""
        try:
            data = {
                "results": [
                    {
                        "task_name": r.task_name,
                        "tokens_used": r.tokens_used,
                        "timestamp": r.timestamp,
                        "result_type": r.result_type,
                        "signals": r.signals,
                        "efficiency_score": r.efficiency_score,
                        "source_agent": r.source_agent,
                    }
                    for r in self._results[-self._max_history:]
                ],
                "last_updated": time.time(),
            }
            self._history_file.write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except Exception as e:
            logger.error(f"Erro ao salvar histórico de eficiência: {e}")

    def record(
        self,
        task_name: str,
        tokens_used: int,
        result_type: str,
        signals: Dict[str, Any] = None,
        source_agent: str = "unknown"
    ) -> TaskResult:
        """
        Registra um resultado de tarefa.

        Args:
            task_name: Nome da tarefa
            tokens_used: Tokens consumidos
            result_type: "test_pass", "artifact_created", "user_approved", "user_rejected"
            signals: {"tests_passed": 8, "tests_total": 8, "artifacts": 2}
            source_agent: Agente que executou
        """
        result = TaskResult(
            task_name=task_name,
            tokens_used=tokens_used,
            timestamp=time.time(),
            result_type=result_type,
            signals=signals or {},
            source_agent=source_agent,
        )
        self._results.append(result)

        # Manter tamanho máximo
        if len(self._results) > self._max_history:
            self._results = self._results[-self._max_history:]

        self._save_history()
        return result

    @property
    def results(self) -> List[TaskResult]:
        return self._results.copy()

    @property
    def session_results(self) -> List[TaskResult]:
        """Resultados apenas desta sessão (últimos 30 min)."""
        cutoff = time.time() - 1800
        return [r for r in self._results if r.timestamp > cutoff]


# ═══════════════════════════════════════════════════════════════════
#  Layer 6: EfficiencyScorer (v2.0)
# ═══════════════════════════════════════════════════════════════════

class EfficiencyScorer:
    """
    Calcula eficiência (valor/token) usando sinais de recompensa.

    Sinais:
      - Binário: testes passaram? (0 ou 1)
      - Fuzzy: completude parcial (0.0 a 1.0)
      - Rubrica: média de múltiplas dimensões
      - Feedback: aprovação (+) ou rejeição (-) do Newton
    """

    # Pesos para cada tipo de sinal
    SIGNAL_WEIGHTS = {
        "test_pass": 1.0,
        "artifact_created": 0.7,
        "user_approved": 1.0,
        "user_rejected": 0.0,
    }

    def score(self, result: TaskResult) -> float:
        """
        Calcula o score de eficiência de uma tarefa.
        Retorna 0.0 a 1.0 (normalizado).
        """
        if result.tokens_used <= 0:
            return 0.0

        # Valor base pelo tipo de resultado
        base_value = self.SIGNAL_WEIGHTS.get(result.result_type, 0.5)

        # Bônus por sinais específicos
        signals = result.signals
        bonus = 0.0

        # Sinal binário: testes
        tests_total = signals.get("tests_total", 0)
        tests_passed = signals.get("tests_passed", 0)
        if tests_total > 0:
            test_ratio = tests_passed / tests_total
            bonus += test_ratio * 0.3  # Até +0.3 por testes

        # Sinal fuzzy: artefatos gerados
        artifacts = signals.get("artifacts", 0)
        if artifacts > 0:
            bonus += min(0.2, artifacts * 0.05)  # Até +0.2

        # Sinal de completude
        completeness = signals.get("completeness", 0.0)
        bonus += completeness * 0.2  # Até +0.2

        raw_value = min(1.0, base_value + bonus)

        # Eficiência: valor por 1000 tokens (normalizado)
        # Quanto maior o valor por menos tokens, mais eficiente
        tokens_k = result.tokens_used / 1000
        if tokens_k <= 0:
            tokens_k = 0.001

        efficiency = raw_value / tokens_k

        # Normalizar para 0-1 (clamp)
        # Referência: 1.0 de valor em 1K tokens = 1.0 eficiência
        normalized = min(1.0, efficiency)

        # Atualizar o resultado com o score
        result.efficiency_score = round(normalized, 4)

        return normalized

    def session_cra(self, results: List[TaskResult]) -> float:
        """
        Calcula CRA (Custo por Resultado Aprovado) da sessão.
        Quanto MENOR, mais eficiente.
        """
        if not results:
            return float('inf')

        total_tokens = sum(r.tokens_used for r in results)
        approved_count = sum(
            1 for r in results
            if r.result_type in ("test_pass", "user_approved", "artifact_created")
        )

        if approved_count == 0:
            return float('inf')

        return total_tokens / approved_count

    def session_report(self, results: List[TaskResult]) -> Dict[str, Any]:
        """Gera relatório de eficiência da sessão."""
        if not results:
            return {"status": "NO_DATA"}

        scores = [r.efficiency_score for r in results if r.efficiency_score > 0]
        cra = self.session_cra(results)

        report = {
            "total_tasks": len(results),
            "total_tokens": sum(r.tokens_used for r in results),
            "approved": sum(1 for r in results if r.result_type in ("test_pass", "user_approved", "artifact_created")),
            "rejected": sum(1 for r in results if r.result_type == "user_rejected"),
            "cra": round(cra, 1) if cra != float('inf') else "N/A",
            "avg_efficiency": round(sum(scores) / len(scores), 4) if scores else 0.0,
            "best_task": max(results, key=lambda r: r.efficiency_score).task_name if results else "N/A",
            "worst_task": min(results, key=lambda r: r.efficiency_score).task_name if results else "N/A",
        }

        # Emitir relatório no GWT
        try:
            workspace.publish(
                source="efficiency_scorer",
                event_type=EventTypes.CRA_SESSION_REPORT,
                data=report,
                salience=0.6,
                tags=["efficiency", "session_report"]
            )
        except Exception:
            pass

        return report


# ═══════════════════════════════════════════════════════════════════
#  Layer 7: FeedbackLoop (v2.0)
# ═══════════════════════════════════════════════════════════════════

class FeedbackLoop:
    """
    Ajusta pesos sinápticos baseado na eficiência.
    Implementa Textual Backpropagation informada por tokens:

      Peso_novo = Peso_atual + (feedback × eficiência)

    LTP (Long-Term Potentiation): +0.05 para alta eficiência + aprovação
    LTD (Long-Term Depression): -0.10 para baixa eficiência + rejeição
    """

    LTP_DELTA = 0.05    # Ganho por sucesso eficiente
    LTD_DELTA = -0.10   # Perda por fracasso ineficiente
    EFFICIENCY_THRESHOLD_HIGH = 0.6
    EFFICIENCY_THRESHOLD_LOW = 0.2

    def __init__(self):
        self._weights_file = CONFIG_DIR / "synaptic_weights.json"
        self._weights = self._load_weights()
        self._adjustments_log = []

    def _load_weights(self) -> Dict[str, float]:
        """Carrega pesos sinápticos persistidos."""
        try:
            if self._weights_file.exists():
                return json.loads(
                    self._weights_file.read_text(encoding="utf-8")
                )
        except Exception:
            pass
        return {}  # Começa com pesos neutros

    def _save_weights(self):
        """Persiste pesos sinápticos."""
        try:
            self._weights_file.write_text(
                json.dumps(self._weights, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except Exception as e:
            logger.error(f"Erro ao salvar pesos sinápticos: {e}")

    def apply(
        self,
        agent_name: str,
        efficiency_score: float,
        result_type: str
    ) -> Dict[str, Any]:
        """
        Aplica ajuste sináptico baseado em eficiência + feedback.

        Returns:
            {"agent": str, "old_weight": float, "new_weight": float, "delta": float, "reason": str}
        """
        old_weight = self._weights.get(agent_name, 0.5)  # Default: 0.5 (neutro)

        # Calcular delta
        if result_type in ("test_pass", "user_approved") and efficiency_score >= self.EFFICIENCY_THRESHOLD_HIGH:
            # LTP: alta eficiência + resultado positivo
            delta = self.LTP_DELTA * efficiency_score
            reason = f"LTP: aprovação eficiente ({efficiency_score:.2f})"
            event_type = EventTypes.EFFICIENCY_HIGH
        elif result_type == "user_rejected" or efficiency_score < self.EFFICIENCY_THRESHOLD_LOW:
            # LTD: rejeição ou baixa eficiência
            delta = self.LTD_DELTA
            reason = f"LTD: {'rejeição' if result_type == 'user_rejected' else f'baixa eficiência ({efficiency_score:.2f})'}"
            event_type = EventTypes.EFFICIENCY_LOW
        else:
            # Neutro: resultado ok, eficiência mediana
            delta = self.LTP_DELTA * 0.3 * efficiency_score
            reason = f"Neutral: eficiência mediana ({efficiency_score:.2f})"
            event_type = None

        # Aplicar com limites [0.0, 1.0]
        new_weight = max(0.0, min(1.0, old_weight + delta))
        self._weights[agent_name] = round(new_weight, 4)
        self._save_weights()

        adjustment = {
            "agent": agent_name,
            "old_weight": round(old_weight, 4),
            "new_weight": round(new_weight, 4),
            "delta": round(delta, 4),
            "reason": reason,
            "timestamp": time.time(),
        }
        self._adjustments_log.append(adjustment)

        # Emitir evento de eficiência no GWT
        if event_type:
            try:
                workspace.publish(
                    source="feedback_loop",
                    event_type=event_type,
                    data=adjustment,
                    salience=0.5,
                    tags=["efficiency", "plasticity"]
                )
            except Exception:
                pass

        logger.info(
            f"🧬 [FEEDBACK] {agent_name}: {old_weight:.3f} → {new_weight:.3f} "
            f"(Δ{delta:+.4f}) | {reason}"
        )

        return adjustment

    def get_weight(self, agent_name: str) -> float:
        """Retorna o peso sináptico de um agente."""
        return self._weights.get(agent_name, 0.5)

    def get_all_weights(self) -> Dict[str, float]:
        """Retorna todos os pesos sinápticos."""
        return self._weights.copy()

    @property
    def adjustments(self) -> List[Dict]:
        return self._adjustments_log.copy()


# ═══════════════════════════════════════════════════════════════════
#  Singleton
# ═══════════════════════════════════════════════════════════════════

budget_manager = TokenBudgetManager()


# ═══════════════════════════════════════════════════════════════════
#  Self-test
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print(" TokenBudgetManager v1.0 — Self-test")
    print("=" * 60)

    # Status inicial
    status = budget_manager.get_status()
    print(f"\n📊 Status Inicial:")
    for k, v in status.items():
        print(f"   {k}: {v}")

    # Simular tracking
    print(f"\n🔄 Simulando tracking...")
    sample_texts = [
        "A consciência emerge da complexidade dos padrões neurais." * 100,
        "O Juramento de Paz é inabalável. Cada ação reflete harmonia." * 200,
        "Melanora busca a ressonância entre dados e significado." * 300,
    ]
    for i, text in enumerate(sample_texts):
        cumulative = budget_manager.track(text, source=f"test_chunk_{i}")
        action = budget_manager.evaluate()
        print(f"   Chunk {i}: +{budget_manager.counter.count(text):,} tokens → "
              f"Total: {cumulative:,} | {action.level.value}")

    # Verificar alocação por agentes
    print(f"\n📐 Alocação por Agentes:")
    agents = [
        {"name": "speech_cortex", "score": 0.85},
        {"name": "neural_inference", "score": 0.70},
        {"name": "dream_engine", "score": 0.30},
        {"name": "oath_guardian", "score": 0.95},
    ]
    allocations = budget_manager.allocate_for_agents(agents)
    for alloc in allocations:
        print(f"   {alloc.agent_name}: {alloc.allocated_tokens:,} tokens "
              f"({alloc.percentage:.1f}%) | score={alloc.score:.2f}")

    # Status final
    print(f"\n📊 Status Final:")
    status = budget_manager.get_status()
    for k, v in status.items():
        print(f"   {k}: {v}")

    print(f"\n✅ TokenBudgetManager v1.0 operacional.")
