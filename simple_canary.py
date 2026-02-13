#!/usr/bin/env python3
# simple_canary.py
# Minimal canary: creates decoy HTML and serves /token/<uuid> endpoint that logs hits.
import http.server, socketserver, socket, uuid, os, datetime, urllib.parse

PORT = 8080
TOKEN = str(uuid.uuid4())
TOKEN_PATH = f"/token/{TOKEN}"
DECOY_FILENAME = f"CANARY_{TOKEN[:8]}.html"
LOGFILE = "canary_hits.log"

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

class CanaryHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == TOKEN_PATH:
            ts = datetime.datetime.utcnow().isoformat() + "Z"
            client = self.client_address[0]
            ua = self.headers.get("User-Agent", "<none>")
            line = f"{ts}\tHIT\t{TOKEN}\t{client}\t{ua}\n"
            print(line.strip())
            with open(LOGFILE, "a", encoding="utf-8") as f:
                f.write(line)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<html><body><h2>Document opened</h2><p>Access recorded.</p></body></html>")
        else:
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

def create_decoy(host, port):
    link = f"http://{host}:{port}{TOKEN_PATH}"
    html = f"""<html><head><title>CONFIDENTIAL</title></head><body>
<h1>Confidential Report</h1>
<p><a href="{link}">Open Confidential Report</a></p>
</body></html>"""
    with open(DECOY_FILENAME, "w", encoding="utf-8") as f:
        f.write(html)
    return os.path.abspath(DECOY_FILENAME), link

def main():
    host = get_local_ip()
    decoy_path, link = create_decoy(host, PORT)
    print("Local IP (for LAN access):", host)
    print("Decoy file:", decoy_path)
    print("Token URL:", link)
    print("Starting server on port", PORT, "- press Ctrl-C to stop")
    os.chdir(os.path.dirname(decoy_path) or ".")
    with socketserver.TCPServer(("", PORT), CanaryHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped.")

if __name__ == "__main__":
    main()
