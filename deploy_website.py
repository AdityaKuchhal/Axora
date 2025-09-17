#!/usr/bin/env python3
"""
Simple HTTP server for testing the website locally
"""
import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

def start_server(port=8000):
    """Start a simple HTTP server"""
    # Change to downloads directory
    os.chdir("downloads")
    
    # Create server
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    
    print(f"🌐 Starting web server on http://localhost:{port}")
    print("📁 Serving files from 'downloads' directory")
    print("🔗 Open your browser and go to the URL above")
    print("⏹️  Press Ctrl+C to stop the server")
    
    # Open browser
    webbrowser.open(f"http://localhost:{port}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.shutdown()

if __name__ == "__main__":
    start_server()



