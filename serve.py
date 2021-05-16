import socket
import http.server
import socketserver

# tasklist
# /IM py37.exe /F
# 
hostname = socket.gethostname()
PORT = 8000
IP = socket.gethostbyname(hostname)
print('serving on:', IP)

Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(('', PORT), Handler) as httpd:
    print('PORT:', PORT)
    httpd.serve_forever()

