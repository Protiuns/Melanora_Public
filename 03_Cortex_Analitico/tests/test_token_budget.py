"""
Tests para TokenBudgetManager v2.0
====================================
Verifica: contagem, política, alocação, guardian, GWT, eficiência, feedback.
"""

import sys
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent))


def test_token_counter_heuristic():
    """Verifica contagem por heurística (4 chars ≈ 1 token)."""
    from cortex.logic.token_budget_manager import TokenCounter

    counter = TokenCounter(chars_per_token=4)
    
    # Texto simples
    text = "A consciência emerge."  # 21 chars → ~5 tokens
    tokens = counter.count(text)
    assert tokens > 0, "Contagem retornou 0"
    assert tokens == len(text) // 4 or counter.method == "tiktoken", \
        f"Heurística esperava {len(text) // 4}, obteve {tokens}"
    
    # Texto vazio
    assert counter.count("") == 0, "Texto vazio deveria ser 0 tokens"
    
    # JSON
    data = {"key": "valor", "nested": {"list": [1, 2, 3]}}
    json_tokens = counter.count_json(data)
    assert json_tokens > 0, "Contagem JSON retornou 0"
    
    print(f"  ✅ Contagem: '{text[:30]}' = {tokens} tokens ({counter.method})")
    print(f"  ✅ JSON: {json_tokens} tokens")


def test_budget_policy():
    """Verifica limites por modo: CREATIVE > FOCUSED > CRITICAL."""
    from cortex.logic.token_budget_manager import BudgetPolicy

    config = {
        "mecw_estimate": 100000,
        "active_mode": "FOCUSED",
        "modes": {
            "CREATIVE": {"budget_ratio": 0.80},
            "FOCUSED": {"budget_ratio": 0.60},
            "CRITICAL": {"budget_ratio": 0.40},
        },
        "guardian_thresholds": {"warning": 0.70, "compress": 0.85, "block": 0.95},
        "min_budget_per_agent": 500,
    }
    policy = BudgetPolicy(config)

    creative = policy.get_total_budget("CREATIVE")
    focused = policy.get_total_budget("FOCUSED")
    critical = policy.get_total_budget("CRITICAL")

    assert creative > focused > critical, \
        f"Ordem errada: C={creative}, F={focused}, Cr={critical}"
    assert creative == 80000
    assert focused == 60000
    assert critical == 40000
    
    print(f"  ✅ CREATIVE={creative:,} > FOCUSED={focused:,} > CRITICAL={critical:,}")


def test_importance_allocator():
    """Verifica distribuição proporcional ao score."""
    from cortex.logic.token_budget_manager import ImportanceAllocator

    allocator = ImportanceAllocator(min_per_agent=100)

    agents = [
        {"name": "alta", "score": 0.9},
        {"name": "media", "score": 0.5},
        {"name": "baixa", "score": 0.1},
    ]
    total_budget = 10000
    allocs = allocator.allocate(agents, total_budget)

    assert len(allocs) == 3, f"Esperava 3 alocações, obteve {len(allocs)}"
    
    # Alta deve ter mais que média, que deve ter mais que baixa
    alta = next(a for a in allocs if a.agent_name == "alta")
    media = next(a for a in allocs if a.agent_name == "media")
    baixa = next(a for a in allocs if a.agent_name == "baixa")
    
    assert alta.allocated_tokens > media.allocated_tokens, \
        f"Alta ({alta.allocated_tokens}) deveria > Média ({media.allocated_tokens})"
    assert media.allocated_tokens > baixa.allocated_tokens, \
        f"Média ({media.allocated_tokens}) deveria > Baixa ({baixa.allocated_tokens})"
    
    # Soma não deve exceder budget
    total = sum(a.allocated_tokens for a in allocs)
    assert total <= total_budget, f"Soma {total} excede budget {total_budget}"
    
    print(f"  ✅ Alta={alta.allocated_tokens:,} > Média={media.allocated_tokens:,} "
          f"> Baixa={baixa.allocated_tokens:,} (total={total:,}/{total_budget:,})")


def test_overflow_guardian_safe():
    """Verifica que consumo baixo retorna SAFE."""
    from cortex.logic.token_budget_manager import OverflowGuardian, GuardianLevel

    thresholds = {"warning": 0.70, "compress": 0.85, "block": 0.95}
    guardian = OverflowGuardian(thresholds)

    action = guardian.check(30000, 100000)  # 30% → SAFE
    assert action.level == GuardianLevel.SAFE, f"Esperava SAFE, obteve {action.level}"
    assert not action.should_compress
    assert not action.should_block
    
    print(f"  ✅ 30% → {action.level.value}: {action.message[:60]}")


def test_overflow_guardian_warning():
    """Verifica alerta em 70%."""
    from cortex.logic.token_budget_manager import OverflowGuardian, GuardianLevel

    thresholds = {"warning": 0.70, "compress": 0.85, "block": 0.95}
    guardian = OverflowGuardian(thresholds)

    action = guardian.check(75000, 100000)  # 75% → WARNING
    assert action.level == GuardianLevel.WARNING, f"Esperava WARNING, obteve {action.level}"
    assert not action.should_compress
    assert not action.should_block
    
    print(f"  ✅ 75% → {action.level.value}")


def test_overflow_guardian_compress():
    """Verifica compressão forçada em 85%."""
    from cortex.logic.token_budget_manager import OverflowGuardian, GuardianLevel

    thresholds = {"warning": 0.70, "compress": 0.85, "block": 0.95}
    guardian = OverflowGuardian(thresholds)

    action = guardian.check(88000, 100000)  # 88% → COMPRESS
    assert action.level == GuardianLevel.COMPRESS, f"Esperava COMPRESS, obteve {action.level}"
    assert action.should_compress
    assert not action.should_block
    
    print(f"  ✅ 88% → {action.level.value} (compress={action.should_compress})")


def test_overflow_guardian_critical():
    """Verifica bloqueio em 95%."""
    from cortex.logic.token_budget_manager import OverflowGuardian, GuardianLevel

    thresholds = {"warning": 0.70, "compress": 0.85, "block": 0.95}
    guardian = OverflowGuardian(thresholds)

    action = guardian.check(96000, 100000)  # 96% → CRITICAL
    assert action.level == GuardianLevel.CRITICAL, f"Esperava CRITICAL, obteve {action.level}"
    assert action.should_compress
    assert action.should_block
    
    print(f"  ✅ 96% → {action.level.value} (block={action.should_block})")


def test_gwt_integration():
    """Verifica emissão de eventos TOKEN no GWT."""
    from cortex.logic.global_workspace import workspace, EventTypes
    from cortex.logic.token_budget_manager import OverflowGuardian

    # Capturar eventos
    captured = []
    workspace.subscribe("test_token_gwt", lambda e: captured.append(e.event_type))

    thresholds = {"warning": 0.70, "compress": 0.85, "block": 0.95}
    guardian = OverflowGuardian(thresholds)

    # Disparar WARNING
    guardian.check(75000, 100000)
    assert EventTypes.TOKEN_WARNING in captured, \
        f"TOKEN_WARNING não emitido. Capturados: {captured}"

    # Disparar CRITICAL
    guardian.check(96000, 100000)
    assert EventTypes.TOKEN_CRITICAL in captured, \
        f"TOKEN_CRITICAL não emitido. Capturados: {captured}"
    
    print(f"  ✅ Eventos GWT emitidos: {captured}")


def test_crash_scenario_simulation():
    """
    Simula o estado da sessão anterior que travou:
    69 tarefas × ~500 tokens + 27 revisões de task.md
    Verifica que o Guardian teria bloqueado.
    """
    from cortex.logic.token_budget_manager import (
        TokenCounter, BudgetPolicy, OverflowGuardian, GuardianLevel
    )

    # Simular modelo local com janela de 8K tokens, 60% MECW = 4800 budget
    counter = TokenCounter(chars_per_token=4)
    policy_config = {
        "mecw_estimate": 8000,
        "active_mode": "FOCUSED",
        "modes": {"FOCUSED": {"budget_ratio": 0.6}},
        "guardian_thresholds": {"warning": 0.70, "compress": 0.85, "block": 0.95},
        "min_budget_per_agent": 100,
    }
    policy = BudgetPolicy(policy_config)
    guardian = OverflowGuardian(policy.get_guardian_thresholds())
    budget = policy.get_total_budget()  # 4800

    # Simular 69 tarefas acumulando contexto
    task_text = "Implementar módulo neural com integração GWT e testes unitários completos. " * 5
    cumulative = 0
    triggered_warning = False
    triggered_compress = False
    triggered_block = False
    block_task = -1

    for i in range(69):
        cumulative += counter.count(task_text)
        action = guardian.check(cumulative, budget)

        if action.level == GuardianLevel.WARNING and not triggered_warning:
            triggered_warning = True
        if action.level == GuardianLevel.COMPRESS and not triggered_compress:
            triggered_compress = True
        if action.level == GuardianLevel.CRITICAL and not triggered_block:
            triggered_block = True
            block_task = i
            break

    assert triggered_warning, "WARNING nunca foi disparado!"
    assert triggered_block, "CRITICAL nunca foi disparado — o crash não seria prevenido!"

    print(f"  ✅ Simulação de crash: {cumulative:,} tokens acumulados / {budget:,} budget")
    print(f"     Guardian ativou: WARNING → COMPRESS → CRITICAL")
    print(f"     Crash teria sido PREVENIDO na tarefa #{block_task}")


def test_result_tracker():
    """Verifica registro e recuperação de resultados."""
    from cortex.logic.token_budget_manager import ResultTracker

    tracker = ResultTracker(max_history=10)
    # Limpar para teste limpo
    tracker._results = []

    r1 = tracker.record("test_task", 500, "test_pass", {"tests_passed": 8, "tests_total": 8})
    r2 = tracker.record("refactor", 2000, "artifact_created", {"artifacts": 3})
    r3 = tracker.record("bad_task", 5000, "user_rejected")

    assert len(tracker.results) >= 3
    assert r1.result_type == "test_pass"
    assert r2.tokens_used == 2000
    assert r3.result_type == "user_rejected"

    print(f"  ✅ Registrados: {len(tracker.results)} resultados")
    print(f"  ✅ Tipos: test_pass, artifact_created, user_rejected")


def test_efficiency_scorer():
    """Verifica cálculo de eficiência com sinais de recompensa."""
    from cortex.logic.token_budget_manager import EfficiencyScorer, TaskResult
    import time

    scorer = EfficiencyScorer()

    # Alta eficiência: poucos tokens + testes passando
    high_eff = TaskResult(
        task_name="efficient", tokens_used=500, timestamp=time.time(),
        result_type="test_pass", signals={"tests_passed": 8, "tests_total": 8}
    )
    score_high = scorer.score(high_eff)
    assert score_high > 0.5, f"Score alto deveria > 0.5, obteve {score_high}"

    # Baixa eficiência: muitos tokens + resultado fraco
    low_eff = TaskResult(
        task_name="wasteful", tokens_used=10000, timestamp=time.time(),
        result_type="user_rejected", signals={}
    )
    score_low = scorer.score(low_eff)
    assert score_low < score_high, f"Score baixo ({score_low}) deveria < alto ({score_high})"

    print(f"  ✅ Alta eficiência: {score_high:.3f} (500 tokens, 8/8 testes)")
    print(f"  ✅ Baixa eficiência: {score_low:.3f} (10K tokens, rejeitado)")


def test_feedback_loop_ltp():
    """Verifica LTP: aprovação eficiente aumenta peso sináptico."""
    from cortex.logic.token_budget_manager import FeedbackLoop

    loop = FeedbackLoop()
    loop._weights = {}  # Reset

    adj = loop.apply("test_agent", 0.85, "test_pass")
    assert adj["new_weight"] > adj["old_weight"], \
        f"LTP deveria aumentar peso: {adj['old_weight']} → {adj['new_weight']}"
    assert adj["delta"] > 0

    print(f"  ✅ LTP: {adj['old_weight']:.3f} → {adj['new_weight']:.3f} (Δ{adj['delta']:+.4f})")


def test_feedback_loop_ltd():
    """Verifica LTD: rejeição diminui peso sináptico."""
    from cortex.logic.token_budget_manager import FeedbackLoop

    loop = FeedbackLoop()
    loop._weights = {"bad_agent": 0.7}

    adj = loop.apply("bad_agent", 0.1, "user_rejected")
    assert adj["new_weight"] < adj["old_weight"], \
        f"LTD deveria diminuir peso: {adj['old_weight']} → {adj['new_weight']}"
    assert adj["delta"] < 0

    print(f"  ✅ LTD: {adj['old_weight']:.3f} → {adj['new_weight']:.3f} (Δ{adj['delta']:+.4f})")


def test_session_cra():
    """Verifica cálculo de CRA (Custo por Resultado Aprovado)."""
    from cortex.logic.token_budget_manager import EfficiencyScorer, TaskResult
    import time

    scorer = EfficiencyScorer()
    now = time.time()

    results = [
        TaskResult("t1", 1000, now, "test_pass", {}, 0.8),
        TaskResult("t2", 2000, now, "artifact_created", {}, 0.5),
        TaskResult("t3", 3000, now, "user_rejected", {}, 0.1),
        TaskResult("t4", 1500, now, "user_approved", {}, 0.9),
    ]

    cra = scorer.session_cra(results)
    # Total: 7500 tokens / 3 aprovados = 2500 CRA
    assert cra == 7500 / 3, f"CRA esperado 2500, obteve {cra}"

    report = scorer.session_report(results)
    assert report["total_tasks"] == 4
    assert report["approved"] == 3
    assert report["rejected"] == 1

    print(f"  ✅ CRA: {cra:.0f} tokens/resultado aprovado")
    print(f"  ✅ Relatório: {report['approved']} aprovados, {report['rejected']} rejeitados")


def test_full_pipeline_v2():
    """Verifica pipeline completo: track → result → score → feedback."""
    from cortex.logic.token_budget_manager import TokenBudgetManager

    manager = TokenBudgetManager()

    output = manager.record_result(
        task_name="speech_cortex_refactor",
        tokens_used=1200,
        result_type="test_pass",
        signals={"tests_passed": 8, "tests_total": 8, "artifacts": 3},
        source_agent="speech_cortex"
    )

    assert "efficiency" in output
    assert "adjustment" in output
    assert output["efficiency"] > 0

    report = manager.session_report()
    assert report.get("total_tasks", 0) > 0 or report.get("status") == "NO_DATA"

    status = manager.get_status()
    assert "synaptic_weights" in status

    print(f"  ✅ Pipeline: eff={output['efficiency']:.3f}")
    print(f"  ✅ Peso sináptico: {output['adjustment']['new_weight']:.3f}")
    print(f"  ✅ Status includes synaptic_weights: {bool(status.get('synaptic_weights', None) is not None)}")


# ═══════════════════════════════════════════════════════════════════
#  Runner
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    tests = [
        # v1.0 — Budget & Guardian
        ("Token Counter (Heuristic)", test_token_counter_heuristic),
        ("Budget Policy", test_budget_policy),
        ("Importance Allocator", test_importance_allocator),
        ("Guardian: SAFE (30%)", test_overflow_guardian_safe),
        ("Guardian: WARNING (75%)", test_overflow_guardian_warning),
        ("Guardian: COMPRESS (88%)", test_overflow_guardian_compress),
        ("Guardian: CRITICAL (96%)", test_overflow_guardian_critical),
        ("GWT Integration", test_gwt_integration),
        ("Crash Scenario Simulation", test_crash_scenario_simulation),
        # v2.0 — Efficiency
        ("Result Tracker", test_result_tracker),
        ("Efficiency Scorer", test_efficiency_scorer),
        ("Feedback Loop: LTP", test_feedback_loop_ltp),
        ("Feedback Loop: LTD", test_feedback_loop_ltd),
        ("Session CRA Report", test_session_cra),
        ("Full Pipeline v2.0", test_full_pipeline_v2),
    ]

    passed = 0
    failed = 0
    print("=" * 60)
    print(" TokenBudgetManager v2.0 — Test Suite")
    print("=" * 60)

    for name, fn in tests:
        print(f"\n🧪 {name}:")
        try:
            fn()
            passed += 1
        except Exception as e:
            print(f"  ❌ FAILED: {e}")
            failed += 1

    print(f"\n{'=' * 60}")
    print(f" Results: {passed} passed, {failed} failed")
    print(f"{'=' * 60}")

    if failed > 0:
        sys.exit(1)
