#!/usr/bin/env python3
"""
Windows-Compatible HTTPS Server for SMAX Matomo Tracking
With CORS support and better security
"""

import http.server
import ssl
import os
import subprocess
import sys
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

def check_openssl():
    """Check if OpenSSL is available"""
    try:
        result = subprocess.run(['openssl', 'version'], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        print(f"✅ OpenSSL found: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: OpenSSL not found.")
        print("\nPlease install OpenSSL:")
        print("1. Download from: https://slproweb.com/products/Win32OpenSSL.html")
        print("2. Install 'Win64 OpenSSL v3.x.x Light'")
        print("3. Add to PATH: C:\\Program Files\\OpenSSL-Win64\\bin")
        print("\nOr install via Chocolatey: choco install openssl")
        return False

def generate_self_signed_cert():
    """Generate a self-signed certificate for Windows"""
    if not os.path.exists(CERT_FILE) or not os.path.exists(KEY_FILE):
        print("🔐 Generating self-signed certificate...")
        
        cmd = [
            'openssl', 'req', '-new', '-x509',
            '-keyout', KEY_FILE,
            '-out', CERT_FILE,
            '-days', '365',
            '-nodes',
            '-subj', '/CN=localhost'
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ Certificate generated: {CERT_FILE}, {KEY_FILE}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error generating certificate: {e}")
            sys.exit(1)

def get_local_ip():
    """Get local IP address"""
    import socket
    try:
        # Create a socket to determine the local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "Unable to determine"

def main():
    # Check OpenSSL
    if not check_openssl():
        input("\nPress Enter to exit...")
        return
    
    # Generate certificate
    generate_self_signed_cert()
    
    # Get local IP
    local_ip = get_local_ip()
    
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
    
    📋 Access URLs:
       Local:    https://localhost:{PORT}/smax-thy-matomo-tracking.js
       Network:  https://{local_ip}:{PORT}/smax-thy-matomo-tracking.js
    
    ⚠️  Using self-signed certificate - browsers will show security warning
    
    🛑 Press Ctrl+C to stop the server
    """)
    
    # List available files
    js_files = [f for f in os.listdir('.') if f.endswith('.js')]
    if js_files:
        print("📄 Available JavaScript files:")
        for f in js_files:
            print(f"   • {f}")
        print()
    else:
        print("⚠️  No .js files found in current directory!")
        print()
    
    print("="*65)
    print()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user.")
        httpd.shutdown()

if __name__ == "__main__":
    main()
