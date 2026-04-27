from http.server import BaseHTTPRequestHandler, HTTPServer
import redis

cache = redis.Redis(host="redis", port=6379, decode_responses=True)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        hits = cache.incr("hits")
        self.send_response(200)
        self.end_headers()
        self.wfile.write(f"Hello from Compose. Hits: {hits}\n".encode())

server = HTTPServer(("0.0.0.0", 8000), Handler)
print("Server running on port 8000")
server.serve_forever()
