"""
🧠💻 Melanora Hybrid Brain — Setup Script
Instala dependências e configura o Córtex Analítico.
"""

import subprocess
import sys
import os
import json
from pathlib import Path

# ============================================================
# 1. DEPENDÊNCIAS
# ============================================================

REQUIRED_PACKAGES = [
    "psutil",       # Hardware profiling (CPU, RAM, Disk)
    "numpy",        # Cálculos matemáticos de alta performance
]

OPTIONAL_PACKAGES = [
    "opencv-python",  # Visão computacional (Fase 3)
    "watchdog",       # Monitoramento de arquivos (Fase 3)
    "mss",            # Captura de tela ultra-rápida (Fase 11)
    "pillow",         # Processamento de imagem e OCR (Fase 11)
    "sounddevice",    # Captura de áudio local (Fase 12)
    "scipy",          # Processamento de sinal e FFT (Fase 12)
    "pydub",          # Manipulação de arquivos de áudio (Fase 12)
]


def install_packages(packages: list[str], optional: bool = False):
    """Instala pacotes via pip."""
    label = "opcionais" if optional else "obrigatórios"
    print(f"\n⚡ Instalando pacotes {label}...")
    
    for pkg in packages:
        try:
            print(f"  📦 {pkg}...", end=" ")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pkg, "--quiet"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print("✅")
        except subprocess.CalledProcessError:
            if optional:
                print(f"⚠️ (opcional, pode instalar depois)")
            else:
                print(f"❌ ERRO — pacote obrigatório!")
                return False
    return True


# ============================================================
# 2. ESTRUTURA DE DIRETÓRIOS
# ============================================================

def create_directories():
    """Cria a estrutura de pastas do Córtex Analítico."""
    base = Path(__file__).parent
    
    dirs = [
        base / "config",
        base / "cortex",
        base / "cortex" / "advanced",
        base / "logs",
    ]
    
    print("\n🏗️ Criando estrutura de diretórios...")
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"  📁 {d.relative_to(base)}")
    
    # Criar __init__.py para importações
    for d in [base / "cortex", base / "cortex" / "advanced"]:
        init = d / "__init__.py"
        if not init.exists():
            init.write_text('"""Melanora Córtex Analítico"""\n')
    
    return True


# ============================================================
# 3. CONFIGURAÇÃO INICIAL
# ============================================================

def create_initial_configs():
    """Cria configurações iniciais (serão atualizadas pelo hardware_profiler)."""
    base = Path(__file__).parent / "config"
    
    configs = {
        "daemon_config.json": {
            "version": "1.0",
            "mode": "LLM_ONLY",  # Será atualizado para HYBRID quando ativado
            "auto_start": False,
            "log_level": "INFO",
            "max_concurrent_tasks": 2,
            "check_interval_ms": 100,
            "safety": {
                "max_cpu_percent": 50,
                "max_ram_percent": 70,
                "timeout_per_task_s": 30
            }
        },
        "neural_state.json": {
            "mode": "LLM_ONLY",
            "cortex_criativo": "ACTIVE",
            "cortex_analitico": "INACTIVE",
            "ciclo_atual": 0,
            "fase": "IDLE",
            "agentes_pico": [],
            "energia_media": 0.1,
            "timestamp": None
        },
        "task_queue.json": {
            "queue": [],
            "processed": 0,
            "errors": 0
        },
        "results_buffer.json": {
            "pending": [],
            "last_result": None
        }
    }
    
    print("\n⚙️ Criando configurações iniciais...")
    for filename, data in configs.items():
        filepath = base / filename
        filepath.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        print(f"  📄 {filename}")
    
    return True


# ============================================================
# 4. MAIN
# ============================================================

def main():
    print("=" * 60)
    print("🧠💻 MELANORA HYBRID BRAIN — Setup")
    print("=" * 60)
    print(f"\nPython: {sys.version}")
    print(f"Plataforma: {sys.platform}")
    
    # Passo 1: Dependências obrigatórias
    if not install_packages(REQUIRED_PACKAGES):
        print("\n⚠️ Algumas dependências obrigatórias falharam. O Córtex Analítico operará em modo reduzido (Standard Lib).")
    
    # Passo 2: Dependências opcionais
    install_packages(OPTIONAL_PACKAGES, optional=True)
    
    # Passo 3: Estrutura de diretórios
    create_directories()
    
    # Passo 4: Configurações
    create_initial_configs()
    
    # Passo 5: Hardware profiler
    print("\n🔍 Executando Hardware Profiler...")
    profiler_path = Path(__file__).parent / "hardware_profiler.py"
    if profiler_path.exists():
        subprocess.run([sys.executable, str(profiler_path)])
    else:
        print("  ⚠️ hardware_profiler.py não encontrado")
    
    print("\n" + "=" * 60)
    print("✅ SETUP COMPLETO!")
    print("=" * 60)
    print("\nPróximos passos:")
    print("  1. Execute: python hardware_profiler.py")
    print("  2. Execute: python neural_bridge.py --start")
    print("  3. Melanora agora pode operar em modo HYBRID 🧠💻⚡")
    
    return True


if __name__ == "__main__":
    main()
