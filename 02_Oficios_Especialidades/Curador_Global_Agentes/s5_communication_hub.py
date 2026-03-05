import logging
import json

# --- CONFIGURAÇÃO DE LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [S5-COMM-HUB] - %(levelname)s - %(message)s'
)

class CommunicationHub:
    """Sistema 5: Hub de Comunicação e Filtragem de Intenções"""
    def __init__(self, s2_orchestrator=None):
        logging.info("🗣️ S5 Comm Hub: Pronto para filtrar intenções.")
        self.s2 = s2_orchestrator
        self.fast_track_keywords = ["olá", "como vai", "quem é você", "status"]

    def process_input(self, user_input, user_gender="Masculino"):
        """Filtra a entrada do usuário e decide a trajetória"""
        logging.info(f"📥 Recebido: '{user_input}'")
        
        # 1. Via Rápida (Fast Response)
        if any(key in user_input.lower() for key in self.fast_track_keywords):
            return self.fast_response(user_input, user_gender)
        
        # 2. Interrupção Executiva
        if "pare" in user_input.lower() or "parar" in user_input.lower():
            return self.executive_interrupt()

        # 3. Filtragem de Intenção para S2
        return self.intent_filter(user_input)

    def fast_response(self, text, gender):
        """Responde diretamente sem sobrecarregar o sistema lógico"""
        honorific = "Senhor" if gender == "Masculino" else "Senhora"
        logging.info("⚡ S5: Via Rápida ativada.")
        return f"Olá, {honorific}! Eu sou o Sistema 5 da Melanora. Meus sistemas lógicos estão em standby, como posso ajudar?"

    def executive_interrupt(self):
        """Sinaliza parada imediata para os sistemas de execução"""
        logging.warning("⚠️ S5: INTERRUPÇÃO EXECUTIVA DISPARADA!")
        return {"signal": "STOP", "origin": "S5", "priority": "CRITICAL"}

    def intent_filter(self, text):
        """Destila linguagem natural em tokens lógicos para S2"""
        logging.info("🔮 S5: Destilando intenção para S2...")
        # Simulação de tradutor LLM leve
        logical_intent = {
            "action_type": "ORCHESTRATION",
            "raw_text": text,
            "logical_tokens": text.split(), # To be replaced by actual NLP
            "complexity": "HIGH"
        }
        return logical_intent

if __name__ == "__main__":
    s5 = CommunicationHub()
    print(s5.process_input("Olá, tudo bem?"))
    print(s5.process_input("Pare toda a execução agora!"))
    print(s5.process_input("Organize meus arquivos de estudo."))
