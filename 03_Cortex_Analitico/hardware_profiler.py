"""
🔍 Melanora Hardware Profiler v1.1 (Zero-Dep)
Auto-detecta capacidades do computador sem dependências externas.
Gera machine_profile.json com limites recomendados.
"""

import json
import platform
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# ============================================================
# 1. DETECÇÃO DE HARDWARE (StdLib + OS Fallbacks)
# ============================================================

def run_ps(cmd: str) -> str:
    """Executa um comando PowerShell e retorna o output."""
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", cmd],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()
    except Exception:
        return ""

def detect_cpu() -> dict:
    """Detecta informações da CPU usando stdlib e WMIC."""
    logical = os.cpu_count() or 1
    name = platform.processor() or "Unknown"
    
    # Tentar pegar nome real no Windows
    if sys.platform == "win32":
        wmic_name = run_ps("(Get-CimInstance Win32_Processor).Name")
        if wmic_name: name = wmic_name

    return {
        "name": name,
        "architecture": platform.machine(),
        "logical_cores": logical,
        "physical_cores": logical // 2 if logical > 1 else 1, # Heurística simples
        "usage_percent": "N/A (needs psutil)"
    }

def detect_ram() -> dict:
    """Detecta informações da RAM usando PowerShell."""
    total_gb = 0
    available_gb = 0
    
    if sys.platform == "win32":
        try:
            # Total RAM em bytes
            total = run_ps("(Get-CimInstance Win32_PhysicalMemory | Measure-Object -Property Capacity -Sum).Sum")
            if total: total_gb = round(float(total) / (1024**3), 1)
            
            # Memória livre em KB
            free_kb = run_ps("(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory")
            if free_kb: available_gb = round(float(free_kb) / (1024**2), 1)
        except Exception:
            pass

    return {
        "total_gb": total_gb or "Unknown",
        "available_gb": available_gb or "Unknown",
        "used_percent": round((1 - (available_gb/total_gb))*100, 1) if (total_gb and available_gb) else "Unknown"
    }

def detect_gpu() -> dict:
    """Detecta GPU via PowerShell."""
    if sys.platform == "win32":
        try:
            res = run_ps("Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM | ConvertTo-Json")
            if res:
                data = json.loads(res)
                if isinstance(data, list): data = data[0]
                ram = data.get("AdapterRAM", 0)
                # AdapterRAM pode ser negativo ou grande em unsigned, simplificando:
                vram_gb = round(abs(float(ram)) / (1024**3), 1) if ram else 0
                return {
                    "name": data.get("Name", "Unknown"),
                    "vram_gb": vram_gb,
                    "detected_via": "WMI/PS"
                }
        except Exception:
            pass
    return {"name": "Not detected", "vram_gb": 0, "detected_via": "none"}

def classify_profile(cpu: dict, ram: dict, gpu: dict) -> dict:
    """Classifica o hardware."""
    cores = cpu["logical_cores"]
    ram_gb = ram.get("total_gb", 0) if isinstance(ram.get("total_gb"), (int, float)) else 0
    vram_gb = gpu.get("vram_gb", 0)

    score = 0
    score += min(cores / 16, 1.0) * 40
    score += min(ram_gb / 32, 1.0) * 30
    score += min(vram_gb / 8, 1.0) * 30

    if score < 30:
        perfil, freq_max, intensidad = "LOW", 50, 0.3
    elif score < 60:
        perfil, freq_max, intensidad = "MEDIUM", 200, 0.5
    else:
        perfil, freq_max, intensidad = "HIGH", 500, 0.7

    return {
        "perfil": perfil,
        "score": round(score, 1),
        "freq_max_hz": freq_max,
        "intensidade_padrao": intensidad,
        "wave_interval_ms": round(1000 / freq_max, 1)
    }

def generate_profile():
    print("🔍 Melanora Hardware Profiler v1.1 (Zero-Dep)")
    print("=" * 50)
    
    cpu = detect_cpu()
    ram = detect_ram()
    gpu = detect_gpu()
    profile_class = classify_profile(cpu, ram, gpu)
    
    profile = {
        "version": "1.1",
        "generated_at": datetime.now().isoformat(),
        "hardware": {"cpu": cpu, "ram": ram, "gpu": gpu},
        "profile": profile_class
    }
    
    out = Path(__file__).parent / "config" / "machine_profile.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(profile, indent=2, ensure_ascii=False))
    
    print(f"\n⚡ PERFIL: {profile_class['perfil']} (Score: {profile_class['score']})")
    print(f"📄 Salvo em: {out}")
    return profile

if __name__ == "__main__":
    generate_profile()
