"""
MELANORA MASTER CONTROL (v1.0)
O Comando Central para a Mente Fisica.
Integra Inicializacao, Monitoramento, Refino e Encerramento.
"""

import os
import sys
import subprocess
import time
import argparse
import json
from pathlib import Path

import sys
from pathlib import Path

# Adiciona o root no sys.path para garantir que o core_topology seja achado
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path: sys.path.append(str(ROOT))

from core_topology import NeuralTopology

# Configuracao de Caminhos Dinâmicos
PYTHON_EXE = NeuralTopology.get_capacity_path("Python")
CORTEX_DIR = NeuralTopology.get_area_path("COGNITIVE")
BRIDGE_PY = CORTEX_DIR / "neural_bridge.py"
API_PY = CORTEX_DIR / "dashboard_api.py"
AFL_PY = CORTEX_DIR / "scripts" / "afl_feedback_loop.py"

def run_command(cmd, detach=False):
    """Executa um comando no sistema."""
    try:
        if detach:
            # Roda em background (sem janela no Windows)
            DETACHED_PROCESS = 0x00000008
            subprocess.Popen(cmd, creationflags=DETACHED_PROCESS, close_fds=True)
        else:
            # Abre uma nova janela de terminal para o processo (evita bloquear o loop)
            subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        return True
    except Exception as e:
        print(f"[ERRO] Falha ao executar comando {cmd}: {e}")
        return False

def start_mind(silent=False, staggered=True):
    """Inicia os processos neurais com sequenciamento opcional."""
    print(f"[MIND] Ativando Mente Fisica (Modo {'Sequencial' if staggered else 'Flash'})...")
    
    # 1. Higienizacao
    clean_locks()
    
    # GRUPO 1: CORE (Sistema Nervoso Central)
    print("[1/3] Grupo CORE: Ativando Neural Bridge...")
    run_command([str(PYTHON_EXE), str(BRIDGE_PY), "--start"], detach=silent)
    
    if staggered:
        print("  ... estabilizando sinapses (2s) ...")
        time.sleep(2)

    # GRUPO 2: INFRA (Interfaces e Telemetria)
    print("[2/3] Grupo INFRA: Ativando Dashboard API...")
    run_command([str(PYTHON_EXE), str(API_PY)], detach=True)
    
    if staggered:
        print("  ... sincronizando fluxos (2s) ...")
        time.sleep(2)

    # GRUPO 3: VIGILANCIA (Integridade e Seguranca)
    watchdog = CORTEX_DIR / "process_integrity" / "run_watchdog_loop.bat"
    if watchdog.exists():
        print("[3/3] Grupo VIGILANCIA: Ativando Auditor de Integridade...")
        subprocess.Popen([str(watchdog)], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    
    dashboard_url = "http://localhost:5000" # Flask Dashboard Gateway
    print("\n[OK] Conexões estabelecidas com sucesso.")
    
    if not silent:
        print(f"[PREMIUM_HUB] Ativando Interface v5.0 em {dashboard_url}...")
        import webbrowser
        time.sleep(2)
        webbrowser.open(dashboard_url)
        print("Operacao continua ativa. Use --stop para encerrar.")

def stop_mind():
    """Encerra todos os processos neurais."""
    print("[STOP] Encerrando conexoes neurais...")
    
    # Comandos de encerramento via PowerShell (mais robusto no Windows)
    ps_cmd = (
        "Get-Process | Where-Object { "
        "$_.CommandLine -like '*neural_bridge.py*' -or "
        "$_.CommandLine -like '*dashboard_api.py*' -or "
        "$_.CommandLine -like '*dashboard_failsafe.py*' -or "
        "$_.ProcessName -eq 'ollama' -or "
        "$_.ProcessName -eq 'node' "
        "} | Stop-Process -Force"
    )
    subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True)
    
    # Limpeza manual de locks por garantia
    clean_locks()
    print("[INFO] Mente Fisica em repouso.")

def clean_locks():
    """Remove arquivos de trava (.lock)."""
    config_dir = CORTEX_DIR / "config"
    if config_dir.exists():
        for lock in config_dir.glob("*.lock"):
            try: lock.unlink()
            except: pass

def show_status():
    """Consulta o status via Neural Bridge."""
    run_command([str(PYTHON_EXE), str(BRIDGE_PY), "--status"])

def run_refine():
    """Executa o ciclo de aprendizado AFL."""
    print("[AFL] Iniciando Ciclo de Refino Neural (AFL)...")
    run_command([str(PYTHON_EXE), str(AFL_PY)])

def main():
    parser = argparse.ArgumentParser(description="Melanora Master Control")
    parser.add_argument("action", choices=["start", "stop", "status", "refine", "restart"], help="Acao a executar")
    parser.add_argument("--silent", action="store_true", help="Inicia em modo silencioso (background)")
    
    args = parser.parse_args()
    
    if args.action == "start":
        start_mind(args.silent)
    elif args.action == "stop":
        stop_mind()
    elif args.action == "status":
        show_status()
    elif args.action == "refine":
        run_refine()
    elif args.action == "restart":
        print("[RESTART] Reiniciando Ciclo Neural...")
        stop_mind()
        # Aguarda os processos limparem da memoria
        time.sleep(3)
        start_mind(args.silent)

if __name__ == "__main__":
    main()
