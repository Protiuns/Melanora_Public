"""
🎙️ Melanora Interview Server
Serve a página de entrevista e faz proxy para o Ollama (resolve CORS).
"""
import http.server
import json
import urllib.request
import urllib.error
import os

PORT = 8888
OLLAMA_URL = "http://localhost:11434"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class InterviewHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_POST(self):
        if self.path.startswith("/api/"):
            # Proxy para o Ollama
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            target_url = f"{OLLAMA_URL}{self.path}"
            
            try:
                req = urllib.request.Request(
                    target_url,
                    data=body,
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=60) as resp:
                    response_data = resp.read()
                    
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(response_data)
            except urllib.error.URLError as e:
                self.send_response(502)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                error_msg = json.dumps({"error": f"Ollama offline: {str(e)}"})
                self.wfile.write(error_msg.encode())
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                error_msg = json.dumps({"error": str(e)})
                self.wfile.write(error_msg.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        msg = format % args
        if "/api/" in msg:
            print(f"🧠 [PROXY] {msg}")
        elif ".html" in msg or ".js" in msg or ".css" in msg:
            print(f"📄 [FILE]  {msg}")

if __name__ == "__main__":
    server = http.server.HTTPServer(("", PORT), InterviewHandler)
    print(f"")
    print(f"  🎙️  Melanora Interview Server")
    print(f"  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"  📡  http://localhost:{PORT}/entrevista_voz.html")
    print(f"  🧠  Proxy Ollama: {OLLAMA_URL}")
    print(f"  ⏹️   Ctrl+C para parar")
    print(f"")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor encerrado.")
        server.shutdown()
