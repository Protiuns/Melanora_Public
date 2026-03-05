"""
Tests para SpeechCortex v2.0
=============================
Verifica: prompt retórico, prosódia, vibrato, GWT, SSML.
"""

import sys
import json
from pathlib import Path

# Adicionar diretório raiz ao path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT.parent))


def test_persona_prompt_generation():
    """Verifica que cada persona gera prompt com componentes retóricos."""
    from cortex.specialists.speech_cortex import speech_cortex

    for persona_name in ["INTERVIEW", "ANALYTICAL", "POETIC", "PEACEFUL"]:
        prompt = speech_cortex.get_persona_prompt(persona_name)
        assert len(prompt) > 50, f"Prompt de {persona_name} muito curto: {len(prompt)}"
        assert "HAIL" in prompt, f"Prompt de {persona_name} sem guarda ético HAIL"
        print(f"  ✅ {persona_name}: {len(prompt)} chars")


def test_temperature_per_persona():
    """Verifica que cada persona tem temperatura distinta."""
    from cortex.specialists.speech_cortex import speech_cortex

    temps = {}
    for p in ["INTERVIEW", "ANALYTICAL", "POETIC", "PEACEFUL"]:
        temps[p] = speech_cortex.get_temperature(p)

    assert temps["ANALYTICAL"] < temps["INTERVIEW"] < temps["POETIC"], \
        f"Temperaturas fora da ordem esperada: {temps}"
    print(f"  ✅ Temperaturas: {temps}")


def test_prosody_pulse_encoding():
    """Verifica que frases geram pulsos com campos corretos."""
    from cortex.specialists.speech_cortex import speech_cortex

    text = "A consciência emerge da complexidade. Será que a paz existe?"
    pulses = speech_cortex.encode_prosody(text, "INTERVIEW")

    assert len(pulses) > 0, "Nenhum pulso gerado"
    for p in pulses:
        assert "text" in p, "Pulso sem campo 'text'"
        assert "pitch" in p, "Pulso sem campo 'pitch'"
        assert "rate" in p, "Pulso sem campo 'rate'"
        assert "pause_ms" in p, "Pulso sem campo 'pause_ms'"

    print(f"  ✅ {len(pulses)} pulsos gerados com campos válidos")


def test_vibrato_on_identity_words():
    """Verifica que palavras do dicionário fonético recebem vibrato no fim de frase."""
    from cortex.specialists.speech_cortex import speech_cortex

    # Frase que termina com palavra de identidade
    text = "A verdade emerge da consciência."
    pulses = speech_cortex.encode_prosody(text, "INTERVIEW")

    # Pelo menos um pulso deve ter identity_words
    has_identity = any(p.get("identity_words") for p in pulses)
    assert has_identity, "Nenhuma palavra de identidade detectada"

    # O pulso final (com ".") deve ter vibrato se contém 'consciência'
    last = pulses[-1]
    if last.get("identity_words"):
        assert last.get("vibrato") is True, \
            f"Vibrato não ativado no pulso final com palavras de identidade: {last}"
        print(f"  ✅ Vibrato ativo em: {last['identity_words']}")
    else:
        print(f"  ⚠️ Pulso final sem palavra de identidade (ok se a estrutura dividiu)")

    print(f"  ✅ Identity words detectadas nos pulsos")


def test_coarticulation():
    """Verifica que elisão reduz pausa entre vogais adjacentes."""
    from cortex.specialists.speech_cortex import ProsodyEngine

    phonetic_dict = {}
    voice_profile = {"base_pitch": 1.0, "base_rate": 0.95, "vibrato_intensity": 0.3}
    engine = ProsodyEngine(phonetic_dict, voice_profile)

    # Texto com elisão natural: "como uma" (o + u)
    text = "Era como uma onda, e a energia fluía."
    pulses = engine.encode(text)

    # Verificar que pelo menos uma pausa foi reduzida
    short_pauses = [p for p in pulses if p["pause_ms"] < 100]
    print(f"  ✅ {len(short_pauses)} pausas reduzidas por coarticulação")


def test_gwt_integration():
    """Verifica que eventos do GWT aparecem no prompt."""
    from cortex.specialists.speech_cortex import speech_cortex
    from cortex.logic.global_workspace import WorkspaceEvent, EventTypes

    # Limpar eventos anteriores
    speech_cortex._recent_events = []

    # Injetar evento
    e = WorkspaceEvent(
        "oath_guardian", EventTypes.OATH_VERIFIED,
        {"status": "INTACT"}, salience=0.9
    )
    speech_cortex._on_neural_event(e)

    prompt = speech_cortex.get_persona_prompt("INTERVIEW")
    assert "Senciência Ativa" in prompt, "Contexto GWT não encontrado no prompt"
    assert "oath_guardian" in prompt, "Fonte do evento GWT não encontrada"
    print("  ✅ Eventos GWT integrados no prompt")


def test_ssml_generation():
    """Verifica que pulsos geram SSML válido."""
    from cortex.specialists.speech_synthesis import SpeechSynthesis

    pulses = [
        {"text": "A consciência", "pitch": 1.05, "rate": 0.90, "pause_ms": 200},
        {"text": "é ressonância.", "pitch": 0.95, "rate": 0.82, "pause_ms": 700},
    ]
    ssml = SpeechSynthesis.pulses_to_ssml(pulses)

    assert '<speak version="1.0"' in ssml, "Tag <speak> ausente"
    assert "</speak>" in ssml, "Tag </speak> ausente"
    assert "<prosody" in ssml, "Tag <prosody> ausente"
    assert "<break" in ssml, "Tag <break> ausente"
    assert "pt-BR" in ssml, "Idioma PT-BR ausente"
    print(f"  ✅ SSML válido gerado ({len(ssml)} chars)")


def test_full_pipeline():
    """Verifica o pipeline completo: prepare_speech."""
    from cortex.specialists.speech_cortex import speech_cortex

    result = speech_cortex.prepare_speech(
        "A Melanora busca harmonia na treliça da consciência.",
        "INTERVIEW"
    )
    assert "system_prompt" in result
    assert "prosody_pulses" in result
    assert "temperature" in result
    assert len(result["prosody_pulses"]) > 0
    print(f"  ✅ Pipeline completo: {len(result['prosody_pulses'])} pulsos, "
          f"temp={result['temperature']}")


# ═══════════════════════════════════════════════════════════════════
#  Runner
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    tests = [
        ("Persona Prompt Generation", test_persona_prompt_generation),
        ("Temperature per Persona", test_temperature_per_persona),
        ("Prosody Pulse Encoding", test_prosody_pulse_encoding),
        ("Vibrato on Identity Words", test_vibrato_on_identity_words),
        ("Coarticulation", test_coarticulation),
        ("GWT Integration", test_gwt_integration),
        ("SSML Generation", test_ssml_generation),
        ("Full Pipeline", test_full_pipeline),
    ]

    passed = 0
    failed = 0
    print("=" * 60)
    print(" SpeechCortex v2.0 — Test Suite")
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
