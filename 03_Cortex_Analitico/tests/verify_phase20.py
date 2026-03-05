import sys
from pathlib import Path

# Adicionar o caminho do projeto ao sys.path
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))

try:
    from cortex.specialists.dialogue_orchestrator import extract_unified_prompt
    
    print("--- [SIMULAÇÃO FASE 20: PONTE DE DIÁLOGO] ---")
    
    # Teste 1: Prompt Simples
    print("\n[TESTE 1] Prompt de Texto Simples...")
    res1 = extract_unified_prompt("Olá Melanora, como você está?")
    print(f"✔️ Resultado: {res1['intent']['final_prompt']}")
    
    # Teste 2: Prompt Contextual (Deisse)
    print("\n[TESTE 2] Prompt com Contexto Visual (Deisse)...")
    res2 = extract_unified_prompt(
        text="O que é isso aqui no código?", 
        vision_metadata={"active": True, "detected_focus": "erro no perception_engine.py"}
    )
    print(f"✔️ Resultado: {res2['intent']['final_prompt']}")
    
    # Teste 3: Prompt Multi-modal (Mic Ativo)
    print("\n[TESTE 3] Prompt com Microfone Ativo...")
    res3 = extract_unified_prompt(
        text="Executar auditoria agora.", 
        audio_metadata={"active": True}
    )
    print(f"✔️ Sensores Ativos: {res3['intent']['metadata']['sensors_active']}")
    
    print("\n--- [VERIFICAÇÃO CONCLUÍDA COM SUCESSO] ---")

except Exception as e:
    print(f"\n❌ ERRO NA VERIFICAÇÃO: {str(e)}")
    import traceback
    traceback.print_exc()
