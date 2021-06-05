import socket
import http.server
import socketserver

# tasklist
# /IM py37.exe /F
# 
hostname = socket.gethostname()
PORT = 8000
IP = socket.gethostbyname(hostname)

Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(('', PORT), Handler) as httpd:
    print(f"Serving on: {IP}:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down serve.py...")

