"""
🧪 Melanora: Verificador de Conexão Synaptica (NotebookLM)
Este script valida se o login foi bem sucedido e se o Melanora consegue 'estudar' seus notebooks.
"""

import json
import subprocess
import sys
from pathlib import Path

def run_test():
    print("--- 🧠 INICIANDO VERIFICAÇÃO DE CONEXÃO GROUNDED ---")
    
    # 1. Teste de Listagem
    print("[1/2] Verificando acesso aos notebooks...")
    cmd_list = ["npx", "-y", "@jacob-bd/notebooklm-mcp-cli", "list"]
    
    try:
        res = subprocess.run(cmd_list, capture_output=True, text=True, timeout=15)
        if res.returncode == 0:
            print("✅ SUCESSO: Consigo ver seus notebooks!")
            print("Notebooks Encontrados:")
            print(res.stdout)
        else:
            print("❌ FALHA: Não consegui listar os notebooks.")
            print("Motivo provável: Você ainda não fez o login ou a sessão expirou.")
            print("Ação: Execute 'npx -y @jacob-bd/notebooklm-mcp-cli login' no seu terminal.")
            return

        # 2. Teste de Consulta Grounded
        print("\n[2/2] Testando consulta de pesquisa (Grounded Query)...")
        cmd_query = ["npx", "-y", "@jacob-bd/notebooklm-mcp-cli", "query", "Resuma os objetivos da Melanora"]
        
        res_q = subprocess.run(cmd_query, capture_output=True, text=True, timeout=20)
        if res_q.returncode == 0:
            print("✅ SUCESSO: Recebi dados fundamentados do NotebookLM!")
            print("\n--- RESPOSTA DO SEU CÉREBRO EXTERNO ---")
            print(res_q.stdout)
        else:
            print("⚠️ AVISO: Listagem OK, mas a pesquisa falhou (pode ser falta de fontes no notebook).")

    except Exception as e:
        print(f"❌ ERRO CRÍTICO: {str(e)}")

if __name__ == "__main__":
    run_test()
