"""
🛠️ Melanora Failsafe Dashboard Server
Serve a versão compilada (dist) do Dashboard caso o npm/Vite falhe.
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 8000
DASHBOARD_DIST = Path(__file__).parent.parent / "dashboard" / "dist"



def start_failsafe():
    if not DASHBOARD_DIST.exists():
        print(f"❌ Erro: Pasta 'dist' não encontrada em {DASHBOARD_DIST}")
        print("💡 Execute 'npm run build' se possível ou verifique a instalação.")
        return

    os.chdir(DASHBOARD_DIST)
    with socketserver.ThreadingTCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
        print(f"🚀 Dashboard de Contingência Ativo em: http://localhost:{PORT}")
        print("⚠️  Nota: Esta é a versão estática (sem Hot Reload).")
        httpd.serve_forever()

if __name__ == "__main__":
    start_failsafe()
