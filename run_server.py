"""PatentPilot Demo 本地 Web 服务（标准库实现，无需 Streamlit）。"""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT_DIR = Path(__file__).resolve().parent
WEB_DIR = ROOT_DIR / "web"
sys.path.insert(0, str(ROOT_DIR))

from src.services.analyzer import PatentAnalyzer  # noqa: E402

HOST = "127.0.0.1"
PORT = 8502


class DemoHandler(BaseHTTPRequestHandler):
    analyzer = PatentAnalyzer()

    def log_message(self, format: str, *args) -> None:
        print(f"[PatentPilot] {self.address_string()} - {format % args}")

    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path, content_type: str) -> None:
        if not path.exists():
            self.send_error(404, "Not Found")
            return
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            self._send_file(WEB_DIR / "index.html", "text/html; charset=utf-8")
            return
        self.send_error(404, "Not Found")

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/api/analyze":
            self.send_error(404, "Not Found")
            return

        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8")
        try:
            payload = json.loads(raw)
            mode = payload.get("mode")
            content = (payload.get("content") or "").strip()
            if not content:
                self._send_json(400, {"error": "内容不能为空"})
                return

            if mode == "idea":
                result = self.analyzer.analyze_idea(content)
            elif mode == "research":
                result = self.analyzer.analyze_research(content)
            else:
                self._send_json(400, {"error": "未知模式"})
                return

            self._send_json(200, result)
        except Exception as exc:
            self._send_json(500, {"error": str(exc)})


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), DemoHandler)
    url = f"http://{HOST}:{PORT}"
    print(f"PatentPilot Demo running at {url}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.server_close()


if __name__ == "__main__":
    main()
