import sys
import os

# Adiciona o diretório raiz ao path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cortex.security.security_nexus import SecurityNexus
from cortex.system_2.behavior_tree_manager import NodeStatus, SecurityGuard, Action

def test_security_sanitization():
    print("Iniciando teste de Sanitização (Data Immunity)...")
    content = "Minha chave é api_key=AIzaSyA1234567890BCDEF e meu segredo é 'sk-abcdef1234567890abcdef1234567890abcdef1234567890'"
    sanitized = SecurityNexus.sanitize_content(content)
    print(f"Original: {content}")
    print(f"Sanitizado: {sanitized}")
    assert "[PROTECTED_SECRET]" in sanitized
    print("✅ Teste de Sanitização passou!\n")

def test_security_barrier():
    print("Iniciando teste de Barreira de Execução...")
    safe_cmd = "git status"
    unsafe_cmd = "rm -rf /"
    
    assert SecurityNexus.validate_command(safe_cmd) == True
    assert SecurityNexus.validate_command(unsafe_cmd) == False
    print(f"Comando Seguro ({safe_cmd}): Permitido")
    print(f"Comando Inseguro ({unsafe_cmd}): Bloqueado")
    print("✅ Teste de Barreira passou!\n")

def test_security_guard_decorator():
    print("Iniciando teste do Decorador SecurityGuard...")
    context = {"target_command": "rm -rf /"}
    
    # Simula uma ação que o guarda deveria bloquear
    mock_action = Action("DeleteAll", lambda ctx: NodeStatus.SUCCESS)
    guard = SecurityGuard("Shield", mock_action)
    
    status = guard.tick(context)
    print(f"Status resultante para comando inseguro: {status}")
    assert status == NodeStatus.FAILURE
    print("✅ Teste do Decorador passou!\n")

if __name__ == "__main__":
    try:
        test_security_sanitization()
        test_security_barrier()
        test_security_guard_decorator()
        print("🎉 TODOS OS TESTES DE SEGURANÇA PASSARAM!")
    except Exception as e:
        print(f"❌ Falha nos testes: {e}")
        sys.exit(1)
