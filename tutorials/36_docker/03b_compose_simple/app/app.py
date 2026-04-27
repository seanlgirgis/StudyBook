from http.server import BaseHTTPRequestHandler, HTTPServer
import redis

r = redis.Redis(host='redis', port=6379)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        r.incr('hits')
        hits = r.get('hits').decode()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(f"Hello! Hits: {hits}".encode())

server = HTTPServer(('0.0.0.0', 8000), Handler)
print("Server running on port 8000")
server.serve_forever()
