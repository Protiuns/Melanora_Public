"""
🛡️ Melanora Security Nexus (Public v1.0)
Implements 'Data Immunity' and 'Execution Barrier' for the public version.
"""

import os
import re

class SecurityNexus:
    # Dangerous patterns and commands
    BANNED_COMMANDS = ["rm -rf", "format", "del /s", "mkfs", "shutdown"]
    SECRET_PATTERNS = [
        r'sk-[a-zA-Z0-9]{48}',  # OpenAI
        r'AIza[a-zA-Z0-9_\\-]{35}', # Google Cloud
        r'[0-9a-f]{32}',        # Generic MD5/Hex secrets
        r'password\s*[:=]\s*[^\s]+', # Passwords
    ]

    @staticmethod
    def sanitize_content(text: str) -> str:
        """Redacts secrets and sensitive patterns from text."""
        if not isinstance(text, str):
            return text
            
        sanitized = text
        for pattern in SecurityNexus.SECRET_PATTERNS:
            sanitized = re.sub(pattern, "[REDACTED_SECRET]", sanitized, flags=re.IGNORECASE)
        return sanitized

    @staticmethod
    def validate_command(command: str) -> bool:
        """Validates if a command is safe to execute."""
        cmd_lower = command.lower()
        for banned in SecurityNexus.BANNED_COMMANDS:
            if banned in cmd_lower:
                return False
        return True

    @staticmethod
    def get_safe_secret(env_key: str) -> str:
        """Retrieves a secret from environment variables only."""
        return os.getenv(env_key, "")

# Global instance
security_nexus = SecurityNexus()
