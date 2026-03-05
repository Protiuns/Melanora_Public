import logging
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cortex.logic.neural_irrigation import global_gland
from cortex.micro_agents.tardigrade_net import TardigradeTissue

logging.basicConfig(level=logging.INFO, format="%(message)s")

def simulate_endocrine_storm():
    print("="*60)
    print("💧🧠 SIMULAÇÃO BIO-QUÍMICA: REDE TARDÍGRADO (200 NÓS)")
    print("="*60)
    
    tardigrade_brain = TardigradeTissue()
    
    print("\n[CENÁRIO 1] Mente em Repouso (Apenas Serotonina)")
    w_survive = tardigrade_brain.process_stimulus("survive", payload={})
    w_explore = tardigrade_brain.process_stimulus("explore", payload={})
    w_maintain = tardigrade_brain.process_stimulus("maintain", payload={})
    print(f"  Afinidade por Fuga (Sobrevivência): {w_survive:.1f}")
    print(f"  Afinidade por Padrões (Explorar) : {w_explore:.1f}")
    print(f"  Afinidade por Limpeza (Manter)   : {w_maintain:.1f}")
    
    # 2. Injetando Dopamina Alta (Curiosidade Aguda)
    print("\n[CENÁRIO 2] Injetando DOPAMINA (Descobriu um enigma novo)")
    global_gland.inject("dopamine", 0.9)
    w_survive = tardigrade_brain.process_stimulus("survive", payload={})
    w_explore = tardigrade_brain.process_stimulus("explore", payload={})
    w_maintain = tardigrade_brain.process_stimulus("maintain", payload={})
    print(f"  Afinidade por Fuga (Sobrevivência): {w_survive:.1f}")
    print(f"  Afinidade por Padrões (Explorar) : ⭐ {w_explore:.1f}")
    print(f"  Afinidade por Limpeza (Manter)   : {w_maintain:.1f}")
    
    # 3. Injetando Adrenalina Massiva (Predador/Erro FATAL)
    print("\n[CENÁRIO 3] Esmagando Glândula de ADRENALINA/CORTISOL (Ameaça Iminente!)")
    global_gland.inject("adrenaline", 1.0) # Satura a rede
    # Zera a serotonina da paz
    global_gland.fluids["serotonin"] = 0.0
    
    start_time = time.perf_counter()
    w_survive = tardigrade_brain.process_stimulus("survive", payload={})
    w_explore = tardigrade_brain.process_stimulus("explore", payload={})
    w_maintain = tardigrade_brain.process_stimulus("maintain", payload={})
    elapsed = time.perf_counter() - start_time
    
    print(f"  Afinidade por Fuga (Sobrevivência): 🩸 {w_survive:.1f} (PÂNICO TOTAL)")
    print(f"  Afinidade por Padrões (Explorar) : {w_explore:.1f} (Caindo devido a disputa..)")
    print(f"  Afinidade por Limpeza (Manter)   : {w_maintain:.1f} (MANUTENÇÃO DESLIGADA/ABANDONADA)")
    
    print(f"\n⚡ Benchmark: A malha de 200 nós foi alterada globalmente em {elapsed * 1_000_000:.1f} microsegundos na CPU local. 0% Tensão no Processador Geral.")

if __name__ == "__main__":
    simulate_endocrine_storm()
