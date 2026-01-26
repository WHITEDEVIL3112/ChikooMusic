import os
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("PORT", 10000))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"ChikooMusic is running!")

def run():
    server = HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Web server running on 0.0.0.0:{PORT}")
    server.serve_forever()

if __name__ == "__main__":
    run()
