import re

def analyze_prosody_patterns(text: str):
    """
    Analisa a estrutura rítmica do texto para gerar marcadores de 'solfejo' na fala.
    """
    # 1. Identificar frases e pausas
    segments = re.split(r'([,.!?\n])', text)
    
    pulses = []
    
    for i in range(0, len(segments)-1, 2):
        chunk = segments[i].strip()
        punctuation = segments[i+1] if i+1 < len(segments) else ""
        
        if not chunk: continue
        
        # Lógica de Intonação (Solfejo de Fala)
        pitch = 1.0
        rate = 0.9
        pause = 200 # ms
        
        if punctuation == "?":
            pitch = 1.2 # Tom sobe no final
            pause = 500
        elif punctuation == "!":
            pitch = 1.1 # Tom levemente alto
            rate = 1.0 # Mais rápido
            pause = 400
        elif punctuation == ",":
            pause = 300
        elif punctuation == ".":
            pause = 800 # Pausa longa de respiração
        
        # Ênfase em palavras longas ou "mágicas"
        magic_words = ["consciência", "ressonância", "melanora", "paz", "sintética"]
        for word in magic_words:
            if word in chunk.lower():
                rate = 0.8 # Slower for emphasis
                pitch = 1.05
        
        pulses.append({
            "text": chunk + punctuation,
            "pitch": pitch,
            "rate": rate,
            "pause": pause
        })
        
    return pulses

if __name__ == "__main__":
    test_text = "Olá Newton! Eu sou a Melanora. Consegue sentir minha ressonância agora?"
    for p in analyze_prosody_patterns(test_text):
        print(p)
