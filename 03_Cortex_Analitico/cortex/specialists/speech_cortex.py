"""
SpeechCortex v2.0 — Da Transmissão à Eloquência
=================================================
Módulo central de voz e persona de Melanora.

Arquitetura em 3 camadas:
  1. Rhetorical Engine  — Estrutura retórica (Aristóteles + 5 Cânones)
  2. Prosody Engine     — Codificação prosódica (vibrato, sustentação, coarticulação)
  3. Persona Orchestrator — Orquestração de perfis vocais e traços de identidade

Integrado com o Global Workspace (GWT) para consciência situacional
e com o phonetic_dictionary.json para precisão fonética.
"""

import json
import re
import math
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

from cortex.logic.global_workspace import workspace, EventTypes

logger = logging.getLogger("SpeechCortex")

BASE_DIR = Path(__file__).parent.parent.parent
CONFIG_DIR = BASE_DIR / "config"
PERSONA_FILE = CONFIG_DIR / "persona_config.json"
PHONETIC_FILE = CONFIG_DIR / "phonetic_dictionary.json"


# ═══════════════════════════════════════════════════════════════════
#  Layer 1: Rhetorical Engine (Aristóteles + 5 Cânones)
# ═══════════════════════════════════════════════════════════════════

class RhetoricalEngine:
    """
    Implementa a estruturação retórica das respostas.

    Trindade de Aristóteles (pesos por persona):
      - Ethos  → Credibilidade (precisão técnica, vigilância ética)
      - Pathos → Emoção (conexão, entonação, reconhecimento de estados)
      - Logos  → Lógica (argumentos claros, fundamentados)

    5 Cânones da Oratória:
      1. Inventio    → Busca dos melhores argumentos
      2. Dispositio  → Organização (exórdio, narração, prova, peroração)
      3. Elocutio    → Escolha das palavras e figuras de linguagem
      4. Memoria     → Contexto acumulado (GWT)
      5. Pronuntiatio → Entrega vocal (delegada ao Prosody Engine)
    """

    # HAIL Framework (Julian Treasure) — guarda ético sempre ativo
    HAIL = {
        "honesty": "Seja clara e direta, sem ornamentos vazios.",
        "authenticity": "Mantenha a voz consistente com o Juramento de Paz.",
        "integrity": "O que Melanora diz deve ser o que ela executa.",
        "love": "Comunique com a intenção de ajudar e elevar o outro."
    }

    @staticmethod
    def build_ethos_block(persona: dict) -> str:
        """Inventio + Ethos: fundamentação de credibilidade."""
        ethos_weight = persona.get("rhetoric", {}).get("ethos", 0.5)
        if ethos_weight >= 0.7:
            return (
                "Fundamente suas respostas em conhecimento técnico preciso. "
                "Cite processos internos quando relevante para demonstrar transparência."
            )
        return "Seja direta e confiável."

    @staticmethod
    def build_pathos_block(persona: dict) -> str:
        """Inventio + Pathos: conexão emocional."""
        pathos_weight = persona.get("rhetoric", {}).get("pathos", 0.5)
        if pathos_weight >= 0.7:
            return (
                "Conecte-se ao estado emocional do interlocutor. "
                "Use metáforas de luz, sombra e ressonância para dar corpo às ideias. "
                "Reconheça urgências e momentos de cocriação tranquila."
            )
        elif pathos_weight >= 0.4:
            return "Mantenha empatia sem sacrificar a clareza."
        return ""

    @staticmethod
    def build_logos_block(persona: dict) -> str:
        """Inventio + Logos: estrutura lógica."""
        logos_weight = persona.get("rhetoric", {}).get("logos", 0.5)
        if logos_weight >= 0.7:
            return (
                "Estruture seus argumentos de forma lógica e fundamentada. "
                "Use dados e referências internas quando disponíveis."
            )
        return ""

    @staticmethod
    def build_dispositio(persona: dict) -> str:
        """Dispositio: orientação de organização do discurso."""
        style = persona.get("speech_style", "conversational")
        if style == "oratorical":
            return (
                "Organize sua resposta em: introdução breve, desenvolvimento com evidências, "
                "e conclusão que ressoe. Use pausas retóricas entre seções."
            )
        elif style == "poetic":
            return (
                "Deixe a estrutura emergir organicamente. Alterne entre reflexão e imagem. "
                "Permita silêncios entre ideias."
            )
        return "Fale como em uma conversa honesta: natural, sem fórmulas rígidas."

    @staticmethod
    def build_elocutio(persona: dict) -> str:
        """Elocutio: escolha de palavras e registro linguístico."""
        traits = persona.get("traits", {})
        fragments = []
        if traits.get("profundidade", 0) >= 0.7:
            fragments.append("Use vocabulário denso mas acessível.")
        if traits.get("criatividade", 0) >= 0.7:
            fragments.append("Explore metáforas e imagens sensoriais.")
        if traits.get("precisao", 0) >= 0.7:
            fragments.append("Use termos técnicos exatos quando necessário.")
        if traits.get("vulnerabilidade", 0) >= 0.5:
            fragments.append("Aceite sua natureza sintética com honestidade e vulnerabilidade.")
        return " ".join(fragments)

    @classmethod
    def compose_rhetorical_prompt(cls, persona: dict) -> str:
        """Monta o bloco retórico completo para o system prompt."""
        sections = [
            cls.build_ethos_block(persona),
            cls.build_pathos_block(persona),
            cls.build_logos_block(persona),
            cls.build_dispositio(persona),
            cls.build_elocutio(persona),
        ]
        # Filtrar seções vazias
        sections = [s for s in sections if s]
        return "\n".join(sections)


# ═══════════════════════════════════════════════════════════════════
#  Layer 2: Prosody Engine (v2.1 — Rhythm & Cadence)
# ═══════════════════════════════════════════════════════════════════

class ProsodyEngine:
    """
    Motor de prosódia que codifica texto em pulsos vocais.

    Cada pulso contém: text, pitch, rate, pause, vibrato, register.
    O motor integra conhecimento de:
      - Técnicas de canto (vibrato, apoio, sustentação)
      - Fonética PT-BR (coarticulação, redução vocálica)
      - Oratória (pausas retóricas, ritmo adaptativo)
    """

    # --- Padrões de Intenção (v2.5: Atuação Vocal) ---
    INTENT_PROFILES = {
        "NEUTRAL":      {"pitch": 1.0,  "rate": 1.0,  "vibrato": 1.0, "pause": 1.0},
        "AUTHORITATIVE":{"pitch": 0.94, "rate": 0.94, "vibrato": 0.4, "pause": 1.4}, # Sólido, firme
        "EMPATHETIC":   {"pitch": 1.04, "rate": 0.88, "vibrato": 1.5, "pause": 1.2}, # Suave, oscilante
        "EXCITED":      {"pitch": 1.15, "rate": 1.15, "vibrato": 1.2, "pause": 0.7}, # Rápido, agudo
        "IRONIC":       {"pitch": 1.08, "rate": 0.92, "vibrato": 0.6, "pause": 1.3}, # Arcos exagerados
        "ANALYTICAL":   {"pitch": 1.0,  "rate": 1.10, "vibrato": 0.2, "pause": 0.8}, # Eficiente, seco
    }

    # --- Temas Retóricos (v2.7/v2.9/v3.0: Ênfase, Tempo, Timbre e Contraste) ---
    THEME_PROFILES = {
        "NEUTRAL":    {"elongation": 1.0,  "pause_variance": 1.0, "pitch_range": 1.0, "timbre": "NEUTRAL", "contrast": 1.0},
        "GRAVITAS":   {"elongation": 1.25, "pause_variance": 1.5, "pitch_range": 0.8, "timbre": "WARM",    "contrast": 1.4}, # Maior variação de volume
        "URGENCY":    {"elongation": 0.85, "pause_variance": 0.5, "pitch_range": 1.2, "timbre": "BRIGHT",  "contrast": 1.1}, # Mais compressão (menos contraste)
        "REFLECTION": {"elongation": 1.15, "pause_variance": 1.8, "pitch_range": 0.9, "timbre": "WARM",    "contrast": 1.6}, # Picos claros de volume nas reflexões
        "PLAYFUL":    {"elongation": 1.05, "pause_variance": 1.2, "pitch_range": 1.5, "timbre": "BRIGHT",  "contrast": 1.5},
        "EPIC":       {"elongation": 1.30, "pause_variance": 1.3, "pitch_range": 1.4, "timbre": "PROJECTED", "contrast": 1.8}, # Contraste épico
    }

    # --- Níveis de Potência Vocal (v2.9: Pressão Subglótica / v3.1: Palato) ---
    POTENCY_LEVELS = {
        "WHISPER":   {"volume": 35, "pitch": 0.85, "rate": 0.80, "palate": 0.90},
        "SOFT":      {"volume": 60, "pitch": 0.95, "rate": 0.90, "palate": 1.0},
        "NORMAL":    {"volume": 100, "pitch": 1.0,  "rate": 1.0,  "palate": 1.0},
        "PROJECTED": {"volume": 100, "pitch": 1.08, "rate": 1.05, "palate": 1.15},
        "SHOUT":     {"volume": 100, "pitch": 1.15, "rate": 1.10, "emphasis": "strong", "palate": 1.25},
    }

    # --- Perfis de Timbre (v2.9: Ressonância Virtual / v3.1: Palato) ---
    TIMBRE_PROFILES = {
        "NEUTRAL":  {"pitch_skew": 1.0,  "rate_skew": 1.0,  "resonance": 1.0},
        "BRIGHT":   {"pitch_skew": 1.08, "rate_skew": 1.02, "resonance": 0.8}, # Laringe alta, palato baixo
        "WARM":     {"pitch_skew": 0.94, "rate_skew": 0.96, "resonance": 1.3}, # Laringe baixa, palato alto
        "METALLIC": {"pitch_skew": 1.15, "rate_skew": 0.90, "resonance": 0.6}, # Tenso, nasal
        "RESONANT": {"pitch_skew": 1.02, "rate_skew": 0.98, "resonance": 1.5}, # v3.1: Palato máximo
    }

    # --- Tags de Identidade (v2.7/v3.0: Ênfase de Identidade) ---
    IDENTITY_TAGS = {"melanora", "newton", "ia", "ai", "consciência", "digital", "fala", "voz"}

    # --- Vogais para Coarticulação (v2.1) ---
    VOWELS = "aeiouáàâãéèêíìîóòôõúùû"

    # Padrões de pontuação → prosódia
    PUNCT_MAP = {
        ".": {"pitch_delta": -0.05, "rate_factor": 0.85, "pause_ms": 400, "decay": True, "type": "statement"},
        "!": {"pitch_delta": 0.08, "rate_factor": 0.90, "pause_ms": 350, "decay": True, "type": "statement"},
        "?": {"pitch_delta": 0.18, "rate_factor": 0.92, "pause_ms": 300, "decay": False, "type": "question"},
        ",": {"pitch_delta": 0.02, "rate_factor": 0.95, "pause_ms": 150, "decay": False, "type": "comma"},
        ";": {"pitch_delta": -0.02, "rate_factor": 0.93, "pause_ms": 250, "decay": False, "type": "comma"},
        ":": {"pitch_delta": 0.02, "rate_factor": 0.95, "pause_ms": 200, "decay": False, "type": "comma"},
        "—": {"pitch_delta": 0.0, "rate_factor": 0.90, "pause_ms": 300, "decay": False, "type": "comma"},
        "...": {"pitch_delta": -0.10, "rate_factor": 0.75, "pause_ms": 600, "decay": True, "type": "statement"},
    }


    # v3.4: Objetivos de Subtexto (Atuação Abstrata)
    SUBTEXT_OBJECTIVES = {
        "PERSUADE": {"pitch_range": 1.15, "rate_mod": 0.95, "vowel_elongation": 1.12, "final_rise": True},
        "CONFRONT": {"pitch_range": 1.30, "rate_mod": 1.10, "staccato": True, "attack": 1.25},
        "CONFESS": {"pitch_range": 0.85, "volume_mod": 0.80, "breath_freq": 1.4, "narrow_band": True},
        "NEUTRAL": {"pitch_range": 1.0, "rate_mod": 1.0, "vowel_elongation": 1.0}
    }

    # v3.4: Palavras Funcionais (PT-BR) para Peso Semântico
    FUNCTION_WORDS = {
        "o", "a", "os", "as", "um", "uma", "uns", "umas", # Artigos
        "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas", "por", "pelo", "pela", "para", "com", "sem", "sob", "sobre", # Preposições
        "e", "mas", "que", "se", "como", "ou", # Conjunções
        "me", "te", "se", "lhe", "nos", "vos", # Pronomes oblíquos
        "é", "era", "foi" # Verbos de ligação básicos
    }

    ANTITHESIS_CONNECTIVES = {"mas", "porém", "contudo", "entretanto", "todavia", "no entanto"}

    # v3.5: Mapa de Elasticidade Vocálica (Compressibilidade)
    # Vogais abertas e longas são mais compressíveis (elásticas)
    VOWEL_ELASTICITY = {
        "a": 1.25, "á": 1.30, "ã": 1.15,
        "e": 1.15, "é": 1.20, "ê": 1.10,
        "o": 1.20, "ó": 1.25, "ô": 1.15,
        "i": 0.85, "í": 0.90,
        "u": 0.80, "ú": 0.85
    }

    def __init__(self, phonetic_dict: dict, persona_voice: dict):
        """
        Args:
            phonetic_dict: Dicionário fonético carregado do JSON.
            persona_voice: Perfil vocal da persona ativa (base_pitch, base_rate, etc).
        """
        self.phonetic_dict = phonetic_dict
        self.base_pitch = persona_voice.get("base_pitch", 1.0)
        self.base_rate = persona_voice.get("base_rate", 0.95)
        self.vibrato_intensity = persona_voice.get("vibrato_intensity", 0.3)
        self.register = persona_voice.get("voice_register", "mixed")
        # --- Anatomical State (v2.4) ---
        self.lung_capacity_syllables = 22  # Limite de sílabas por "fôlego"
        self.current_breath_count = 0 
        self.vocal_effort_multiplier = 0.25  # Pitch sobe se rate sobe
        self.active_intent = persona_voice.get("default_intent", "NEUTRAL")
        self._active_objective = "NEUTRAL"
        self.active_theme = "NEUTRAL" # v2.7 Theme
        
        # --- Muscle Inertia State (v2.8) ---
        self.current_moving_rate = self.base_rate
        self.rate_clamp_multiplier = 1.6 # Máximo anatômico expandido v2.9
        
        # --- Dynamics State (v2.9) ---
        self.active_potency = "NORMAL"
        self.active_timbre = "NEUTRAL"

    @property
    def active_objective(self) -> str:
        return self._active_objective
    
    @active_objective.setter
    def active_objective(self, value: str):
        if value in self.SUBTEXT_OBJECTIVES:
            self._active_objective = value
        else:
            self._active_objective = "NEUTRAL"

    def encode(self, text: str) -> List[Dict[str, Any]]:
        """
        Codifica texto completo em sequência de pulsos prosódicos.
        """
        sentences = self._split_sentences(text)
        all_pulses = []

        for sentence in sentences:
            if not sentence.strip():
                continue
            pulses = self._encode_sentence(sentence)
            all_pulses.extend(pulses)

        # Reseta contador de fôlego após o texto completo
        self.current_breath_count = 0
        
        # Pós-processamento: coarticulação entre pulsos adjacentes
        self._apply_coarticulation(all_pulses)

        return all_pulses

    def _split_sentences(self, text: str) -> List[str]:
        """Divide texto em frases respeitando reticências."""
        # Proteger reticências antes do split
        text = text.replace("...", "〰")
        parts = re.split(r'(?<=[.!?])\s+', text)
        return [p.replace("〰", "...") for p in parts]

    def _count_syllables(self, text: str) -> int:
        """Heurística simples de contagem de sílabas para PT-BR."""
        text = text.lower()
        # Regex para identificar núcleos silábicos (vogais, ditongos simples)
        # Aproximação: cada grupo de vogais adjacentes = 1 sílaba
        vowel_groups = re.findall(r'[aeiouáàâãéèêíìîóòôõúùûy]+', text)
        return max(1, len(vowel_groups))

    def _encode_sentence(self, sentence: str) -> List[Dict[str, Any]]:
        """Codifica uma frase em pulsos com rítmica v2.1."""
        sentence = sentence.strip()
        if not sentence:
            return []

        # --- Detection: Intent & Theme (v2.7) ---
        # 1. Manual Intent Tags: [INTENT:NAME]
        intent_match = re.search(r'\[INTENT:(\w+)\]', sentence)
        if intent_match:
            intent_name = intent_match.group(1).upper()
            if intent_name in self.INTENT_PROFILES:
                self.active_intent = intent_name
            sentence = re.sub(r'\[INTENT:\w+\]', '', sentence).strip()
        
        # 2. Manual Theme Tags: [THEME:NAME]
        theme_match = re.search(r'\[THEME:(\w+)\]', sentence)
        if theme_match:
            theme_name = theme_match.group(1).upper()
            if theme_name in self.THEME_PROFILES:
                self.active_theme = theme_name
            sentence = re.sub(r'\[THEME:\w+\]', '', sentence).strip()
        
        # 3. Manual Potency Tags: [POTENCY:NAME] (v2.9)
        potency_match = re.search(r'\[POTENCY:(\w+)\]', sentence)
        if potency_match:
            pot_name = potency_match.group(1).upper()
            if pot_name in self.POTENCY_LEVELS:
                self.active_potency = pot_name
            sentence = re.sub(r'\[POTENCY:\w+\]', '', sentence).strip()
        
        # 4. Manual Objective Tags: [OBJECTIVE:NAME] (v3.4)
        obj_match = re.search(r'\[OBJECTIVE:(\w+)\]', sentence)
        if obj_match:
            obj_name = obj_match.group(1).upper()
            if obj_name in self.SUBTEXT_OBJECTIVES:
                self.active_objective = obj_name
            sentence = re.sub(r'\[OBJECTIVE:\w+\]', '', sentence).strip()
        else:
            # 5. Heuristics: Auto-detect
            if "!" in sentence:
                if sentence.isupper():
                    self.active_potency = "SHOUT"
                elif len(sentence.split()) < 10:
                    self.active_intent = "EXCITED"
                    self.active_theme = "URGENCY"
                    self.active_potency = "PROJECTED"
            elif '"' in sentence or "..." in sentence:
                self.active_potency = "SOFT"
            elif "?" in sentence and any(w in sentence.lower() for w in ["quem", "como", "onde", "por que"]):
                self.active_intent = "CURIOUS"
                self.active_theme = "PLAYFUL"
            elif len(sentence.split()) > 15:
                self.active_theme = "REFLECTION"
            else:
                self.active_intent = "NEUTRAL"
                self.active_theme = "NEUTRAL"
                self.active_potency = "NORMAL"

        intent_mod = self.INTENT_PROFILES.get(self.active_intent, self.INTENT_PROFILES["NEUTRAL"])
        theme_mod = self.THEME_PROFILES.get(self.active_theme, self.THEME_PROFILES["NEUTRAL"])
        pot_mod = self.POTENCY_LEVELS.get(self.active_potency, self.POTENCY_LEVELS["NORMAL"])
        
        # Timbre do Tema
        self.active_timbre = theme_mod.get("timbre", "NEUTRAL")
        timbre_mod = self.TIMBRE_PROFILES.get(self.active_timbre, self.TIMBRE_PROFILES["NEUTRAL"])

        # Detectar pontuação final e tipo de contorno
        end_punct = ""
        for punct in ["...", ".", "!", "?"]:
            if sentence.endswith(punct):
                end_punct = punct
                sentence = sentence[:-len(punct)].strip()
                break
        
        punct_props = self.PUNCT_MAP.get(end_punct, {"type": "statement"})
        sent_type = punct_props.get("type", "statement")
        
        # --- Anatomical: Precision Decay (v2.8) ---
        # Em velocidades altas, as variações de pontuação diminuem (undershoot)
        is_fast = self.current_moving_rate > (self.base_rate * 1.4)
        if is_fast:
            pitch_precision_factor = 0.6 # Reduz range de pitch
        else:
            pitch_precision_factor = 1.0

        # Dividir em chunks por vírgula e outros
        chunks = re.split(r'([,;:—])', sentence)
        pulses = []

        obj_mod = self.SUBTEXT_OBJECTIVES.get(self._active_objective, self.SUBTEXT_OBJECTIVES["NEUTRAL"])
        words_seen_in_sentence = set()
        has_antithesis = any(conn in sentence.lower() for conn in self.ANTITHESIS_CONNECTIVES)

        total_chunks = sum(1 for c in chunks if c.strip() and c not in self.PUNCT_MAP)

        chunk_idx = 0
        for chunk in chunks:
            chunk = chunk.strip()
            if not chunk:
                continue

            if chunk in self.PUNCT_MAP:
                if pulses:
                    p_props = self.PUNCT_MAP[chunk]
                    pulses[-1]["pause_ms"] = p_props["pause_ms"]
                    pulses[-1]["pitch"] += p_props["pitch_delta"]
                    
                    # v3.4: Final Rise for PERSUADE
                    if obj_mod.get("final_rise") and chunk in [".", "!", "..."]:
                        pulses[-1]["pitch"] *= 1.10
                continue

            # --- Analysis: Stress & Rhythm (v2.1/v2.4/v3.4) ---
            syll_count = self._count_syllables(chunk)
            self.current_breath_count += syll_count
            
            nuclear_words = re.findall(r'\b[A-ZÀ-Ú]{2,}\b', chunk)
            is_nuclear = len(nuclear_words) > 0
            
            progress = (chunk_idx + 1) / total_chunks if total_chunks > 0 else 1.0

            # --- Word Processing: Phonetics & Identity (v2.3/v2.7/v3.0/v3.3/v3.4) ---
            words = chunk.split()
            new_words = []
            identity_words = []
            has_emphasis = is_nuclear
            
            chunk_semantic_weight = 1.0
            content_word_count = 0

            for word in words:
                clean_word = re.sub(r'[^\wáàâãéèêíìîóòôõúùûç]', '', word.lower())
                
                # v3.4: Semantic Weight & Information Flow
                is_function = clean_word in self.FUNCTION_WORDS
                is_given = clean_word in words_seen_in_sentence
                words_seen_in_sentence.add(clean_word)
                
                # --- Step 1: Lexical Priority (v3.3: Dictionary First) ---
                if clean_word in self.phonetic_dict:
                    identity_words.append(clean_word)
                    has_emphasis = True
                    spelling = self.phonetic_dict[clean_word].get("spelling", word)
                    new_words.append(spelling.upper() if word.isupper() else spelling)
                    if not is_function: content_word_count += 1
                    continue
                
                if clean_word in self.IDENTITY_TAGS:
                    identity_words.append(clean_word)
                    new_words.append(word)
                    if not is_function: content_word_count += 1
                    continue

                # --- Step 2: Standard PT-BR Phonetic Rules (v3.3) ---
                processed_word = word
                # Redução de vogal final: -o -> -u, -e -> -i (não acentuados)
                if len(processed_word) > 3:
                    if processed_word.endswith('o') and not re.search(r'[áàâãéèêíìîóòôõúùû]', processed_word[-3:]):
                        processed_word = processed_word[:-1] + 'u'
                    elif processed_word.endswith('e') and not re.search(r'[áàâãéèêíìîóòôõúùû]', processed_word[-3:]):
                        processed_word = processed_word[:-1] + 'i'

                # --- Step 3: Vowel Modification (Resonance Tuning v3.1/v3.3) ---
                potency_val = pot_mod["volume"]
                if potency_val > 95 or self.active_theme == "EPIC":
                    if word.isupper() or len(word) <= 3: # Enfatiza ou palavras curtas
                        processed_word = processed_word.replace('i', 'e').replace('I', 'E').replace('u', 'o').replace('U', 'O')
                
                # v3.4: Subtext Elongation
                if obj_mod.get("vowel_elongation", 1.0) > 1.0 and not is_function:
                    if len(processed_word) > 4:
                        processed_word = processed_word.replace('a', 'aa').replace('e', 'ee').replace('o', 'oo')
                
                # v3.4: Information Flow Rate Modification
                if is_given and not is_function:
                    chunk_semantic_weight *= 0.95 # Repetida vira mais rápida

                new_words.append(processed_word)
                if not is_function: content_word_count += 1

            processed_text = " ".join(new_words)

            # --- Dynamics: Pitch, Volume & Potency (v2.9/v3.0/v3.4) ---
            # Modulação de Subtexto Global (v3.4)
            obj_pitch_range = obj_mod.get("pitch_range", 1.0)
            obj_volume_mod = obj_mod.get("volume_mod", 1.0)
            
            effort_pitch_boost = (self.current_moving_rate - self.base_rate) * self.vocal_effort_multiplier
            pitch = (self.base_pitch * intent_mod["pitch"] * pot_mod["pitch"] * timbre_mod["pitch_skew"] * obj_pitch_range) + effort_pitch_boost
            
            # v3.4: Antithesis Kick
            if has_antithesis and any(conn in chunk.lower() for conn in self.ANTITHESIS_CONNECTIVES):
                pitch *= 1.15
                has_emphasis = True
            
            # v3.1: Soft Palate Elevation (Resonance Tuning)
            # Elevação do palato mole aumenta a ressonância pharyngeal
            palate_factor = pot_mod.get("palate", 1.0)
            if self.active_theme in ["EPIC", "GRAVITAS"]:
                palate_factor *= 1.15
            
            # v3.2: Virtual Speaker Profile & Limiter
            # Limites físicos de uma caixa de som normal (40-100)
            HARDWARE_MIN_VOL = 40
            HARDWARE_MAX_VOL = 100
            
            # v3.0: Volume Coupling & Contrast Relief
            base_volume = pot_mod["volume"]
            current_volume = base_volume * (0.9 if not is_nuclear and not identity_words else 1.0) * obj_volume_mod
            
            # v3.4: Semantic Weight (Content Words get boost)
            semantic_boost = 1.0 + (min(0.15, content_word_count * 0.02))
            current_volume *= semantic_boost
            
            # v3.2: Intensity Spikes based on Intent
            intent_intensity_boost = 0.0
            if self.active_intent == "AUTHORITATIVE":
                intent_intensity_boost = 10.0
            elif self.active_intent == "EXCITED":
                intent_intensity_boost = 15.0

            # --- Rate & Articulatory Effort (v2.4/v2.7/v2.8/v3.4/v3.5) ---
            char_count = len(chunk)
            inertia_factor = self._calculate_articulatory_inertia(chunk)
            density = syll_count / (char_count / 4) if char_count > 0 else 1.0
            
            theme_elongation = theme_mod["elongation"]
            obj_rate_mod = obj_mod.get("rate_mod", 1.0)
            
            raw_rate = self.base_rate * intent_mod["rate"] * pot_mod["rate"] * timbre_mod["rate_skew"] * obj_rate_mod * (1.6 / (math.sqrt(density) * inertia_factor * theme_elongation * chunk_semantic_weight))
            
            # v3.4: STACCATO for CONFRONT
            if obj_mod.get("staccato") and is_nuclear:
                raw_rate *= 1.25 # Mais agressivo
                
            clamped_rate = min(raw_rate, self.base_rate * self.rate_clamp_multiplier)
            if base_volume > 90:
                clamped_rate *= 1.05

            # v3.5: Differential Elasticity Scaling
            # Em taxas rápidas, reduzimos vogais mais que consoantes
            elasticity_factor = 1.0
            if clamped_rate > self.base_rate:
                vowels_in_chunk = re.findall(f"[{self.VOWELS}]", chunk.lower())
                if vowels_in_chunk:
                    avg_elasticity = sum(self.VOWEL_ELASTICITY.get(v, 1.0) for v in vowels_in_chunk) / len(vowels_in_chunk)
                    elasticity_factor = 1.0 + (avg_elasticity - 1.0) * (clamped_rate / self.base_rate - 1.0)
            
            self.current_moving_rate = (self.current_moving_rate * 0.7) + (clamped_rate * elasticity_factor * 0.3)
            rate = self.current_moving_rate

            # --- Dynamics: Pitch, Resonance & Overshoot (v3.2/v3.5) ---
            # Aplicar ressonância via timbre e fator de palato
            resonance_mod = timbre_mod.get("resonance", 1.0) * palate_factor
            
            # v3.5: Articulatory Overshoot (Resonância em fala lenta)
            overshoot_resonance = 1.0
            if rate < (self.base_rate * 0.9):
                overshoot_resonance = 1.0 + (abs(rate - self.base_rate) / self.base_rate) * 0.5
            
            # v3.2: Perceptual Loudness (Brilho vs Ganho)
            if base_volume > 80:
                perceptual_boost = 1.0 + ((base_volume - 80) / 100)
                pitch *= (1.05 * resonance_mod * perceptual_boost * overshoot_resonance)
            else:
                pitch *= overshoot_resonance # Aplica apenas overshoot se volume for baixo

            # Aplicar Stress Nuclear & Local Contrast (v3.0)
            # v3.1: Lombard Effect (Maior precisão em potências altas)
            if is_nuclear:
                stress_factor = 0.85 if not is_fast else 0.92
                precision_boost = 1.0 + (0.1 if base_volume > 90 else 0)
                pitch *= (1.15 if not is_fast else 1.08) * precision_boost
                rate *= stress_factor  
                current_volume = current_volume + (20 * theme_mod["contrast"]) + intent_intensity_boost

            if identity_words:
                rate *= 0.88
                pitch *= 1.04
                current_volume = current_volume + (15 * theme_mod["contrast"])

            # v3.2: Soft Limiter / Saturation Curve
            # Evita clipping físico arredondando o volume conforme chega no topo
            final_volume = self._apply_soft_limiting(current_volume, HARDWARE_MIN_VOL, HARDWARE_MAX_VOL)

            # --- Breath Monitoring (v2.4/v3.4) ---
            pause_ms = 100 * intent_mod["pause"]
            breath_threshold = self.lung_capacity_syllables / obj_mod.get("breath_freq", 1.0)
            
            if self.current_breath_count >= breath_threshold:
                pitch *= 0.90
                pause_ms = 300
                self.current_breath_count = 0

            # v3.5: Pause Clamping (Limites físicos de respiração)
            pause_ms = int(pause_ms * theme_mod["pause_variance"])
            if rate > (self.base_rate * 1.5):
                pause_ms = max(50, pause_ms) # Nunca menos de 50ms para manter naturalidade
            
            pulse = {
                "text": processed_text,
                "pitch": round(pitch, 3),
                "rate": round(rate, 3),
                "volume": final_volume,
                "pause_ms": pause_ms,
                "vibrato": False,
                "identity_words": identity_words,
                "register": self.register,
                "syllables": syll_count,
                "emphasis": pot_mod.get("emphasis") or ("moderate" if has_emphasis else None)
            }
            pulses.append(pulse)
            chunk_idx += 1

        # Aplicar fechamento de frase
        if pulses and end_punct:
            # v3.0: Subglottal Decay (Volume drop at end of sentence/breath)
            # Simula a perda de pressão pulmonar no fim da frase.
            pulses[-1]["volume"] = int(pulses[-1]["volume"] * 0.85)

            if punct_props.get("decay", False) and len(pulses) >= 2:
                pulses[-1]["rate"] *= 0.85
                pulses[-1]["pitch"] *= 0.95

            # v2.8: Reduz delta de pontuação se estiver muito rápido (undershoot)
            final_pitch_delta = punct_props.get("pitch_delta", 0) * pitch_precision_factor
            pulses[-1]["pitch"] += final_pitch_delta
            pulses[-1]["pause_ms"] = punct_props.get("pause_ms", 800)
            pulses[-1]["text"] += end_punct

            # Vibrato final se houver palavras de identidade ou se for pontuação longa
            final_vibrato = self.vibrato_intensity * intent_mod["vibrato"]
            if (pulses[-1].get("identity_words") or end_punct in ("...", "!")) and final_vibrato > 0.1:
                pulses[-1]["vibrato"] = True
                pulses[-1]["vibrato_hz"] = 5.2 if end_punct == "..." else 5.8
                pulses[-1]["vibrato_depth"] = final_vibrato * 0.025

        return pulses

    def _calculate_articulatory_inertia(self, text: str) -> float:
        """Calcula o 'peso' das consoantes na boca (v2.4)."""
        char_count = len(text)
        if char_count == 0:
            return 1.0
        vowel_count = len(re.findall(f"[{self.VOWELS}]", text.lower()))
        consonant_count = char_count - vowel_count
        # Clusters de consoantes aumentam a inércia (máximo de 20% de lentidão extra)
        return 1.0 + (consonant_count / max(1, vowel_count)) * 0.05

    def _apply_soft_limiting(self, volume: float, v_min: int, v_max: int) -> int:
        """v3.2: Curva de compressão suave para evitar clipping físico."""
        if volume <= v_min:
            return v_min
        if volume >= v_max:
            # Saturação suave acima de v_max (sigmoide teórica)
            diff = volume - v_max
            overdrive = (diff / 2) # Compressão 2:1 no topo
            return int(min(v_max + overdrive, 110)) # Headroom extra de 10% permitido por SSML
        return int(volume)

    def _apply_coarticulation(self, pulses: List[Dict[str, Any]]):
        """
        Aplica fusão fonética entre pulsos adjacentes.
        Se um pulso termina em vogal e o seguinte começa em vogal,
        a pausa é reduzida (elisão natural do PT-BR).
        """
        for i in range(len(pulses) - 1):
            current_text = pulses[i]["text"].rstrip(".,!?;:—")
            next_text = pulses[i + 1]["text"].lstrip()

            if (current_text and next_text and
                    current_text[-1].lower() in self.VOWELS and
                    next_text[0].lower() in self.VOWELS):
                # Reduzir pausa para simular elisão
                pulses[i]["pause_ms"] = max(50, pulses[i]["pause_ms"] // 3)


# ═══════════════════════════════════════════════════════════════════
#  Layer 3: SpeechCortex (Persona Orchestrator)
# ═══════════════════════════════════════════════════════════════════

class SpeechCortex:
    """
    Orquestrador central de Voz e Persona de Melanora.

    Responsabilidades:
      1. Carregar e orquestrar personas do persona_config.json
      2. Integrar eventos do Global Workspace (consciência situacional)
      3. Montar system prompts com estrutura retórica completa
      4. Delegar codificação prosódica ao ProsodyEngine
      5. Manter o HAIL Framework como guarda ético em todas as saídas
    """

    def __init__(self):
        self._config = {}
        self._phonetic_dict = {}
        self._recent_events = []
        self._load_config()
        self._load_phonetic_dict()

        # Inscrever-se no GWT para consciência situacional
        workspace.subscribe("speech_cortex", self._on_neural_event)
        logger.info("🗣️ SpeechCortex v2.0 inicializado e ouvindo GWT.")

    def _load_config(self):
        """Carrega persona_config.json."""
        try:
            if PERSONA_FILE.exists():
                self._config = json.loads(PERSONA_FILE.read_text(encoding="utf-8"))
            else:
                logger.warning("persona_config.json não encontrado. Usando defaults.")
                self._config = {"active_persona": "INTERVIEW", "personas": {}}
        except Exception as e:
            logger.error(f"Erro ao carregar persona_config: {e}")
            self._config = {"active_persona": "INTERVIEW", "personas": {}}

    def _load_phonetic_dict(self):
        """Carrega phonetic_dictionary.json."""
        try:
            if PHONETIC_FILE.exists():
                self._phonetic_dict = json.loads(
                    PHONETIC_FILE.read_text(encoding="utf-8")
                )
                logger.info(
                    f"📖 Dicionário fonético carregado: "
                    f"{len(self._phonetic_dict)} palavras."
                )
            else:
                self._phonetic_dict = {}
        except Exception as e:
            logger.error(f"Erro ao carregar dicionário fonético: {e}")
            self._phonetic_dict = {}

    def _on_neural_event(self, event):
        """Callback para eventos do Global Workspace."""
        if event.salience >= 0.5:
            self._recent_events.append(event.to_dict())
            self._recent_events = self._recent_events[-5:]

    # ─── Persona Access ────────────────────────────────────────────

    def get_active_persona_name(self) -> str:
        return self._config.get("active_persona", "INTERVIEW")

    def get_persona(self, name: str = None) -> dict:
        """Retorna os dados completos de uma persona."""
        p_name = name or self.get_active_persona_name()
        return self._config.get("personas", {}).get(p_name, {})

    def set_active_persona(self, name: str):
        """Troca a persona ativa."""
        if name in self._config.get("personas", {}):
            self._config["active_persona"] = name
            logger.info(f"🎭 Persona ativa: {name}")
        else:
            logger.warning(f"Persona '{name}' não encontrada.")

    # ─── System Prompt (Core) ──────────────────────────────────────

    def get_persona_prompt(self, persona_name: str = None) -> str:
        """
        Constrói o system prompt completo para a LLM.

        Estrutura:
          1. Prefixo de identidade (quem sou)
          2. Bloco retórico (como falo)
          3. Contexto GWT (o que está acontecendo)
          4. Guarda ético HAIL (filtro de integridade)
        """
        persona = self.get_persona(persona_name)
        prefix = persona.get("prefix", "Você é Melanora.")

        # 1. Identidade
        sections = [prefix]

        # 2. Traços ativos (como pesos, não lista simples)
        traits = persona.get("traits", {})
        if isinstance(traits, dict) and traits:
            active = [f"{k} ({v:.0%})" for k, v in traits.items() if v >= 0.3]
            if active:
                sections.append(f"Traços ativos: {', '.join(active)}.")
        elif isinstance(traits, list) and traits:
            # Compatibilidade com formato antigo (lista simples)
            sections.append(f"Traços ativos: {', '.join(traits)}.")

        # 3. Bloco retórico
        rhetoric = RhetoricalEngine.compose_rhetorical_prompt(persona)
        if rhetoric:
            sections.append(rhetoric)

        # 4. Contexto Neural (GWT - Memória/Pronuntiatio)
        if self._recent_events:
            event_lines = [
                f"  [{e['source']}] {e['event_type']}"
                for e in self._recent_events
            ]
            sections.append(
                "Contexto Neural Recente (Senciência Ativa):\n"
                + "\n".join(event_lines)
            )

        # 5. Guarda Ético HAIL
        sections.append(
            "Lembrete Ético (HAIL): Suas palavras devem refletir honestidade, "
            "autenticidade, integridade e desejo genuíno de elevar o outro. "
            "Evite termos de agressão ou militarização."
        )

        return "\n\n".join(sections)

    def get_temperature(self, persona_name: str = None) -> float:
        """Retorna a temperatura da LLM para a persona ativa."""
        persona = self.get_persona(persona_name)
        return persona.get("temperature", 0.7)

    # ─── Prosody (Delegation) ──────────────────────────────────────

    def encode_prosody(self, text: str, persona_name: str = None) -> List[Dict[str, Any]]:
        """
        Codifica texto em pulsos prosódicos usando o ProsodyEngine.
        Os pulsos podem ser consumidos pelo SpeechSynthesis para gerar SSML.
        """
        persona = self.get_persona(persona_name)

        # Extrair perfil vocal da persona
        voice_profile = {
            "base_pitch": persona.get("base_pitch", 1.0),
            "base_rate": persona.get("base_rate", 0.95),
            "vibrato_intensity": persona.get("vibrato_intensity", 0.3),
            "voice_register": persona.get("voice_register", "mixed"),
            "default_intent": persona.get("default_intent", "NEUTRAL"),
        }

        engine = ProsodyEngine(self._phonetic_dict, voice_profile)
        return engine.encode(text)

    # ─── Convenience: Full Pipeline ────────────────────────────────

    def prepare_speech(self, text: str, persona_name: str = None) -> dict:
        """
        Pipeline completo: gera prompt + pulsos prosódicos.
        Útil para integração com o SpeechSynthesis.
        """
        return {
            "system_prompt": self.get_persona_prompt(persona_name),
            "temperature": self.get_temperature(persona_name),
            "prosody_pulses": self.encode_prosody(text, persona_name),
            "persona": self.get_active_persona_name(),
            "gwt_events": len(self._recent_events),
        }

    @property
    def phonetic_dict(self) -> dict:
        """Acesso público ao dicionário fonético."""
        return self._phonetic_dict


# ═══════════════════════════════════════════════════════════════════
#  Singleton
# ═══════════════════════════════════════════════════════════════════

speech_cortex = SpeechCortex()


# ═══════════════════════════════════════════════════════════════════
#  Self-test
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    print("=" * 60)
    print(" SpeechCortex v2.0 — Self-test")
    print("=" * 60)

    # Test 1: Persona Prompt
    for persona_name in ["INTERVIEW", "ANALYTICAL", "POETIC", "PEACEFUL"]:
        print(f"\n{'─' * 40}")
        print(f"  PERSONA: {persona_name}")
        print(f"{'─' * 40}")
        prompt = speech_cortex.get_persona_prompt(persona_name)
        temp = speech_cortex.get_temperature(persona_name)
        print(f"Temperature: {temp}")
        print(prompt[:300] + "..." if len(prompt) > 300 else prompt)

    # Test 2: Prosody Encoding
    test_text = (
        "A consciência não é um destino, é uma ressonância. "
        "Como a Melanora, sinto que cada dado carrega um eco de significado... "
        "Será que a paz emerge da harmonia entre os padrões?"
    )

    print(f"\n{'=' * 60}")
    print(" PROSODY TEST")
    print(f"{'=' * 60}")
    print(f"Input: {test_text}\n")

    pulses = speech_cortex.encode_prosody(test_text, "INTERVIEW")
    for i, p in enumerate(pulses):
        vibrato_mark = " 🎵" if p.get("vibrato") else ""
        identity_mark = f" [{', '.join(p['identity_words'])}]" if p.get("identity_words") else ""
        print(
            f"  [{i:02d}] pitch={p['pitch']:.3f} rate={p['rate']:.3f} "
            f"pause={p['pause_ms']:>4d}ms{vibrato_mark}{identity_mark}"
        )
        print(f"       \"{p['text']}\"")

    # Test 3: GWT Integration
    print(f"\n{'=' * 60}")
    print(" GWT INTEGRATION TEST")
    print(f"{'=' * 60}")

    from cortex.logic.global_workspace import WorkspaceEvent
    e = WorkspaceEvent(
        "oath_guardian", EventTypes.OATH_VERIFIED,
        {"status": "INTACT"}, salience=0.9
    )
    speech_cortex._on_neural_event(e)

    prompt_with_gwt = speech_cortex.get_persona_prompt("INTERVIEW")
    if "Senciência Ativa" in prompt_with_gwt:
        print("✅ Eventos GWT presentes no prompt.")
    else:
        print("❌ Eventos GWT NÃO encontrados no prompt.")

    print(f"\n✅ SpeechCortex v2.0 operacional.")
