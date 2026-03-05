import re
import os

class SecurityNexus:
    """
    O Nexo de Segurança é o sistema imunológico da Melanora.
    Responsável por Data Immunity (sanitização) e Execution Barrier (gating).
    """
    
    # Padrões para detecção de segredos (API Keys, etc)
    SECRET_PATTERNS = [
        r"(?i)api_key[\s:=]+['\"]?([a-zA-Z0-9_\-]{20,})['\"]?",
        r"(?i)secret[\s:=]+['\"]?([a-zA-Z0-9_\-]{20,})['\"]?",
        r"(?i)password[\s:=]+['\"]?([a-zA-Z0-9_\-]{8,})['\"]?",
        r"AIza[0-9A-Za-z\\-_]{35}", # Google API Key
        r"sk-[a-zA-Z0-9]{48}",      # OpenAI API Key
    ]
    
    # Comandos proibidos na barreira de execução
    FORBIDDEN_COMMANDS = [
        "rm -rf", "format", "del /s", "mkfs", "dd if=", "shutdown", "reboot"
    ]
    
    @classmethod
    def sanitize_content(cls, content: str) -> str:
        """
        Data Immunity: Remove segredos do conteúdo antes da exportação ou log.
        """
        sanitized = content
        for pattern in cls.SECRET_PATTERNS:
            sanitized = re.sub(pattern, lambda m: m.group(0).replace(m.group(1), "[PROTECTED_SECRET]") if len(m.groups()) > 0 else "[PROTECTED_SECRET]", sanitized)
        return sanitized
    
    @classmethod
    def validate_command(cls, command: str) -> bool:
        """
        Execution Barrier: Verifica se o comando motor é seguro para execução local.
        """
        cmd_lower = command.lower()
        for forbidden in cls.FORBIDDEN_COMMANDS:
            if forbidden in cmd_lower:
                return False
        return True

    @classmethod
    def get_safe_secret(cls, key_name: str) -> str:
        """
        Secret Layer: Recupera chaves apenas de variáveis de ambiente.
        """
        return os.environ.get(key_name, "[NOT_CONFIGURED]")
