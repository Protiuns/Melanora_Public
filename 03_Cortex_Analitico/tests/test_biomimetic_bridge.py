"""
Script de teste para validar o comportamento biomimético do Neural Bridge.
Envia comandos simulados para o `neural_bridge.py` via linha de comando.
"""
import subprocess
import time
import os
import json

bridge_script = r"c:\Users\Newton\Meu Drive\1. Projetos\Melanora\03_Cortex_Analitico\neural_bridge.py"

print("--- Teste 1: Comando Familiar e Simples ---")
# Deve passar sem Dilema
subprocess.run(["python", bridge_script, "--enqueue", "vision_module", "scan_screen", '{"confidence": 0.9}'])
time.sleep(1)

print("\n--- Teste 2: Comando Estranho e Complexo (Dilema Cognitivo) ---")
# Deve gerar baixa confiança heurística devido a "unknown" e módulo estranho
complex_params = json.dumps({
    "action": "unknown_override",
    "param1": "uma string excessivamente longa para causar estranheza " * 10,
    "param2": "undefined"
})
subprocess.run(["python", bridge_script, "--enqueue", "alien_foreign_module", "do_something", complex_params])

print("\nVerifique os logs em 03_Cortex_Analitico/logs/ para confirmar o ⚠️ DILEMA COGNITIVO.")
