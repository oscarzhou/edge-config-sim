import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

API_PORT = int(os.getenv("API_PORT", "8000"))
API_MESSAGE = os.getenv("API_MESSAGE", "hello")
CONFIG_VERSION = os.getenv("CONFIG_VERSION", "unset")

CONFIG_PATH = "/app/config/app-config.json"
LOG_PATH = "/app/logs/api.log"

def read_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"note": "config missing or invalid"}

def log_line(msg: str) -> None:
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/health", "/api/health"):
            cfg = read_config()
            body = {
                "ok": True,
                "api_message": API_MESSAGE,
                "config_version": CONFIG_VERSION,
                "config_file": cfg,
                "ts": int(time.time()),
            }
            log_line(f"[health] {body}")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write((json.dumps(body) + "\n").encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    print(f"API listening on :{API_PORT}")
    HTTPServer(("0.0.0.0", API_PORT), Handler).serve_forever()
