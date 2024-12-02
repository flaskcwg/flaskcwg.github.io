import socket
import http.server
import socketserver

def get_server_address():
    """Returns the server's IP address and port."""
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip, 8000

def run_server():
    """Runs the HTTP server."""
    ip, port = get_server_address()
    handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving on: {ip}:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down server...")

if __name__ == "__main__":
    run_server()
