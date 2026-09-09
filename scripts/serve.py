"""Loopback-only preview; request bodies are never logged or saved."""
import argparse
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from koi import ROOT, render_request

class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def do_POST(self):
        allowed = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
        if self.headers.get("Host") not in allowed or self.headers.get("Origin") not in {None, *('http://' + h for h in allowed)}:
            self.send_error(403)
            return
        if self.path != "/api/render":
            self.send_error(404)
            return
        if self.headers.get_content_type() != "application/json":
            self.send_error(415)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 16384:
                raise ValueError("请求体大小不合法")
            result = render_request(json.loads(self.rfile.read(length)))
            code = 200
        except (ValueError, TypeError, UnicodeError) as error:
            result, code = {"error": str(error)}, 400
        body = json.dumps(result, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

def make_server(port=4317):
    return ThreadingHTTPServer(("127.0.0.1", port), partial(Handler, directory=str(ROOT / "wireframes")))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=4317)
    args = parser.parse_args()
    with make_server(args.port) as server:
        print(f"Koi StyleKit: http://127.0.0.1:{server.server_port}/", flush=True)
        server.serve_forever()
