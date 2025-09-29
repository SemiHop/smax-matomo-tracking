#!/usr/bin/env python3
"""
Simple HTTPS Server for SMAX Matomo Tracking
Usage: python3 simple_https_server.py
Access: https://localhost:4443/smax-matomo-tracking.js
"""

import http.server
import ssl
import os

# Configuration
PORT = 4443
CERT_FILE = "server.crt"
KEY_FILE = "server.key"

def generate_self_signed_cert():
    """Generate a self-signed certificate if it doesn't exist"""
    if not os.path.exists(CERT_FILE) or not os.path.exists(KEY_FILE):
        print("Generating self-signed certificate...")
        os.system(f'openssl req -new -x509 -keyout {KEY_FILE} -out {CERT_FILE} -days 365 -nodes -subj "/CN=localhost"')
        print(f"Certificate generated: {CERT_FILE}, {KEY_FILE}")

def main():
    # Generate certificate if needed
    generate_self_signed_cert()
    
    # Create HTTPS server
    server_address = ('0.0.0.0', PORT)
    httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
    
    # Wrap with SSL
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(CERT_FILE, KEY_FILE)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    
    print(f"""
    ╔═══════════════════════════════════════════════════════╗
    ║  HTTPS Server Started Successfully!                   ║
    ╚═══════════════════════════════════════════════════════╝
    
    Server running on: https://0.0.0.0:{PORT}
    
    Access your script at:
    • Local:   https://localhost:{PORT}/smax-matomo-tracking.js
    • Network: https://YOUR_IP_ADDRESS:{PORT}/smax-matomo-tracking.js
    
    Press Ctrl+C to stop the server
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        httpd.shutdown()

if __name__ == "__main__":
    main()
