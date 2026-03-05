"""
🧪 Melanora Phase 13 Verification Script
Simula pulsação sensorial para validar a solidificação de Qualia.
"""

from cortex.logic.synthesis_engine import process_sensory_pulse, load_qualia
import time

def run_simulation():
    print("🚀 Iniciando Simulação de Solidificação Sensorial...")
    
    # Simular 10 pulsos de uma cor específica (#00FFAB - Verde Melanora)
    # Isso deve atingir o limiar de 70% e solidificar
    for i in range(10):
        print(f"  [Pulso {i+1}] Enviando 'Verde Melanora'...")
        res = process_sensory_pulse("VISION", {"color": "#00FFAB", "harmony": "HIGH"})
        if res["status"] == "SOLIDIFYING":
            print(f"  ✨ Padrão Detectado: {res['patterns']}")
            
    # Verificar registro
    data = load_qualia()
    stable = data.get("stable_qualia", {})
    
    if "VISION_color" in stable:
        print("\n✅ SUCESSO: Qualia 'VISION_color' solidificada com sucesso!")
        print(f"   Valor: {stable['VISION_color']['value']}")
        print(f"   Coerência: {stable['VISION_color']['coherence']:.2%}")
    else:
        print("\n❌ FALHA: Qualia não foi solidificada. Verifique a lógica de buffer.")

if __name__ == "__main__":
    run_simulation()
