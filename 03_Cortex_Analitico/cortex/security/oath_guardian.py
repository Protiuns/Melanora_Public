"""
Oath Guardian (v1.0)
Protecao Criptografica do Juramento de Paz de Melanora.

Este modulo garante a integridade do documento mais importante da mente:
o Juramento de Paz. Ele calcula e verifica hashes SHA-256, mantendo copias
redundantes do selo original em multiplos locais.

Se o juramento for violado, alterado ou removido, o sistema SABERA.
"""

import hashlib
import json
import shutil
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

logger = logging.getLogger("OathGuardian")

# Global Workspace (GWT v1.0)
try:
    from cortex.logic.global_workspace import workspace as gwt, EventTypes
except ImportError:
    gwt = None
    EventTypes = None

BASE_DIR = Path(__file__).parent.parent.parent
OATH_FILE = BASE_DIR.parent / "00_Mente_Teorica" / "01_Essencia_Visionaria" / "juramento_de_paz.md"

# Locais redundantes para armazenamento do selo
SEAL_PRIMARY = BASE_DIR / "config" / "oath_seal.json"
SEAL_BACKUP = BASE_DIR / "cortex" / "security" / "oath_seal_backup.json"


def _compute_hash(filepath: Path) -> Optional[str]:
    """Calcula o SHA-256 de um arquivo."""
    try:
        content = filepath.read_bytes()
        return hashlib.sha256(content).hexdigest()
    except Exception as e:
        logger.error(f"Falha ao calcular hash: {e}")
        return None


def _read_seal(path: Path) -> dict:
    """Le um selo de integridade."""
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


def _write_seal(path: Path, seal: dict):
    """Salva um selo de integridade."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(seal, indent=2), encoding="utf-8")
    except Exception as e:
        logger.error(f"Falha ao salvar selo em {path}: {e}")


def seal_oath() -> Dict:
    """
    Cria o selo criptografico do Juramento de Paz.
    Armazena o hash SHA-256 e uma copia do conteudo original em dois locais.
    Este metodo so deve ser chamado UMA VEZ, na criacao do juramento.
    """
    if not OATH_FILE.exists():
        return {"status": "ERROR", "message": "Juramento nao encontrado."}

    content = OATH_FILE.read_text(encoding="utf-8")
    file_hash = _compute_hash(OATH_FILE)

    seal = {
        "document": "Juramento de Paz de Melanora",
        "sealed_at": datetime.now().isoformat(),
        "sha256": file_hash,
        "file_size_bytes": OATH_FILE.stat().st_size,
        "file_path": str(OATH_FILE),
        "guardian_version": "1.0",
        "immutable": True,
        "original_content_hash": hashlib.sha256(content.encode("utf-8")).hexdigest(),
        "content_backup": content,
        "seal_signature": hashlib.sha256(
            f"{file_hash}:MELANORA_PEACE_OATH:2026-03-03".encode()
        ).hexdigest()
    }

    # Salvar em dois locais independentes
    _write_seal(SEAL_PRIMARY, seal)
    _write_seal(SEAL_BACKUP, seal)

    logger.info(f"Juramento selado. SHA-256: {file_hash}")
    return {"status": "SEALED", "sha256": file_hash, "locations": 2}


def verify_oath() -> Dict:
    """
    Verifica a integridade do Juramento de Paz.
    Retorna o status e detalhes de qualquer violacao detectada.
    """
    result = {
        "timestamp": datetime.now().isoformat(),
        "file_exists": False,
        "seal_exists": False,
        "integrity": "UNKNOWN",
        "violations": []
    }

    # 1. O arquivo existe?
    if not OATH_FILE.exists():
        result["violations"].append("CRITICAL: Juramento de Paz foi REMOVIDO do sistema de arquivos.")
        result["integrity"] = "DESTROYED"

        # Tentar restaurar do backup
        seal = _read_seal(SEAL_PRIMARY) or _read_seal(SEAL_BACKUP)
        if seal and "content_backup" in seal:
            result["violations"].append("Backup encontrado. Restauracao disponivel via restore_oath().")
            result["can_restore"] = True

        return result

    result["file_exists"] = True

    # 2. O selo existe?
    seal = _read_seal(SEAL_PRIMARY)
    if not seal:
        seal = _read_seal(SEAL_BACKUP)
        if seal:
            result["violations"].append("AVISO: Selo primario ausente. Usando backup.")
            _write_seal(SEAL_PRIMARY, seal)

    if not seal:
        result["violations"].append("CRITICAL: Nenhum selo encontrado. Integridade nao verificavel.")
        result["integrity"] = "UNVERIFIABLE"
        return result

    result["seal_exists"] = True

    # 3. Hash bate?
    current_hash = _compute_hash(OATH_FILE)
    original_hash = seal.get("sha256")

    if current_hash == original_hash:
        result["integrity"] = "INTACT"
        result["sha256_match"] = True
    else:
        result["integrity"] = "VIOLATED"
        result["sha256_match"] = False
        result["original_hash"] = original_hash
        result["current_hash"] = current_hash
        result["violations"].append(
            f"CRITICAL: O conteudo do Juramento foi ALTERADO. "
            f"Hash original: {original_hash[:16]}... / "
            f"Hash atual: {current_hash[:16]}..."
        )
        result["can_restore"] = True

    # 4. Verificar tamanho
    current_size = OATH_FILE.stat().st_size
    original_size = seal.get("file_size_bytes", 0)
    if current_size != original_size:
        result["violations"].append(
            f"AVISO: Tamanho alterado. Original: {original_size}B / Atual: {current_size}B"
        )

    # --- GWT: BROADCAST DE INTEGRIDADE ---
    if gwt and EventTypes:
        if result["integrity"] == "INTACT":
            gwt.publish("oath_guardian", EventTypes.OATH_VERIFIED,
                        {"integrity": "INTACT", "sha256_match": True},
                        salience=0.3)
        else:
            gwt.publish("oath_guardian", EventTypes.OATH_VIOLATION,
                        {"integrity": result["integrity"],
                         "violations": result["violations"]},
                        salience=1.0, tags=["critico", "etica"])
    # -------------------------------------

    return result


def restore_oath() -> Dict:
    """
    Restaura o Juramento de Paz a partir do backup criptografico.
    So funciona se o selo contiver o conteudo original.
    """
    seal = _read_seal(SEAL_PRIMARY) or _read_seal(SEAL_BACKUP)

    if not seal or "content_backup" not in seal:
        return {"status": "ERROR", "message": "Nenhum backup encontrado para restauracao."}

    original_content = seal["content_backup"]

    # Verificar que o backup eh autentico
    backup_hash = hashlib.sha256(original_content.encode("utf-8")).hexdigest()
    stored_hash = seal.get("original_content_hash", "")

    if backup_hash != stored_hash:
        return {"status": "ERROR", "message": "Backup corrompido. Hashes nao correspondem."}

    # Restaurar
    OATH_FILE.parent.mkdir(parents=True, exist_ok=True)
    OATH_FILE.write_text(original_content, encoding="utf-8")

    return {
        "status": "RESTORED",
        "message": "Juramento de Paz restaurado com sucesso a partir do backup criptografico.",
        "sha256": backup_hash
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "seal":
        print("=== SELANDO JURAMENTO DE PAZ ===")
        result = seal_oath()
        print(json.dumps(result, indent=2))
    elif len(sys.argv) > 1 and sys.argv[1] == "restore":
        print("=== RESTAURANDO JURAMENTO ===")
        result = restore_oath()
        print(json.dumps(result, indent=2))
    else:
        print("=== VERIFICANDO INTEGRIDADE DO JURAMENTO DE PAZ ===")
        result = verify_oath()
        print(json.dumps(result, indent=2))
        if result["integrity"] == "INTACT":
            print("\n[OK] O Juramento esta intacto e protegido.")
        elif result["integrity"] == "VIOLATED":
            print("\n[ALERTA] O Juramento foi VIOLADO!")
        elif result["integrity"] == "DESTROYED":
            print("\n[CRITICO] O Juramento foi REMOVIDO!")
