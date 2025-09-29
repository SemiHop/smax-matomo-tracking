#!/usr/bin/env python3
"""
Production-Ready HTTPS Server for SMAX Matomo Tracking
With CORS support and better security
"""

import http.server
import ssl
import os
from http import HTTPStatus

PORT = 4443
CERT_FILE = "server.crt"
KEY_FILE = "server.key"

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP Handler with CORS headers for SMAX compatibility"""
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        
        # Security headers
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        
        # Cache control for JavaScript
        if self.path.endswith('.js'):
            self.send_header('Content-Type', 'application/javascript; charset=utf-8')
            self.send_header('Cache-Control', 'public, max-age=3600')
        
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle preflight requests"""
        self.send_response(HTTPStatus.OK)
        self.end_headers()
    
    def log_message(self, format, *args):
        """Custom log format"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def generate_self_signed_cert():
    """Generate a self-signed certificate"""
    if not os.path.exists(CERT_FILE) or not os.path.exists(KEY_FILE):
        print("🔐 Generating self-signed certificate...")
        cmd = (
            f'openssl req -new -x509 -keyout {KEY_FILE} -out {CERT_FILE} '
            f'-days 365 -nodes -subj "/CN=localhost" 2>/dev/null'
        )
        os.system(cmd)
        print(f"✅ Certificate generated: {CERT_FILE}, {KEY_FILE}")

def main():
    # Check if openssl is available
    if os.system('which openssl > /dev/null 2>&1') != 0:
        print("❌ Error: OpenSSL not found. Please install OpenSSL.")
        return
    
    # Generate certificate
    generate_self_signed_cert()
    
    # Create HTTPS server
    server_address = ('0.0.0.0', PORT)
    httpd = http.server.HTTPServer(server_address, CORSHTTPRequestHandler)
    
    # Configure SSL
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(CERT_FILE, KEY_FILE)
    httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    
    print(f"""
    ╔═══════════════════════════════════════════════════════════════╗
    ║            🚀 SMAX HTTPS Server Running                       ║
    ╚═══════════════════════════════════════════════════════════════╝
    
    📍 Server Address: https://0.0.0.0:{PORT}
    📂 Serving Directory: {os.getcwd()}
    
    📋 Your tracking script URL:
       https://localhost:{PORT}/smax-matomo-tracking.js
    
    🌐 For remote access, use your server IP:
       https://YOUR_SERVER_IP:{PORT}/smax-matomo-tracking.js
    
    ⚠️  Using self-signed certificate - browsers will show security warning
    
    🛑 Press Ctrl+C to stop
    """)
    
    # List available files
    js_files = [f for f in os.listdir('.') if f.endswith('.js')]
    if js_files:
        print("📄 Available JavaScript files:")
        for f in js_files:
            print(f"   • {f}")
    else:
        print("⚠️  No .js files found in current directory!")
    
    print("\n" + "="*65 + "\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user.")
        httpd.shutdown()

if __name__ == "__main__":
    main()