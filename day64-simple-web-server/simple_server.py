"""
Simple Web Server Module
Custom HTTP server with logging and routing
"""

import http.server
import socketserver
import os
import datetime
import urllib.parse
import json
from typing import Dict, Any


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom HTTP request handler with additional features
    """
    
    def __init__(self, *args, **kwargs):
        self.log_file = "logs/access.log"
        super().__init__(*args, **kwargs)
    
    def log_message(self, format: str, *args):
        """Override log_message to write to file"""
        # Log to console
        super().log_message(format, *args)
        
        # Log to file
        try:
            os.makedirs("logs", exist_ok=True)
            with open(self.log_file, 'a', encoding='utf-8') as f:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                message = format % args
                f.write(f"[{timestamp}] {self.address_string()} - {message}\n")
        except Exception as e:
            print(f"Log write error: {e}")
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Log request
        self.log_message(f"GET {self.path}")
        
        # Route handling
        if path == '/':
            self.serve_file('static/index.html', 'text/html')
        elif path == '/style.css':
            self.serve_file('static/style.css', 'text/css')
        elif path == '/script.js':
            self.serve_file('static/script.js', 'application/javascript')
        elif path == '/api/time':
            self.serve_json({'time': datetime.datetime.now().isoformat()})
        elif path == '/api/info':
            self.serve_json({
                'server': 'Python SimpleHTTPServer',
                'version': '1.0.0',
                'python_version': os.sys.version,
                'platform': os.sys.platform
            })
        elif path == '/api/headers':
            headers = dict(self.headers)
            self.serve_json({'headers': headers})
        else:
            # Try to serve static file
            try:
                if path.startswith('/static/'):
                    file_path = path[1:]  # Remove leading slash
                    self.serve_file(file_path, self.guess_type(file_path))
                else:
                    self.send_error(404, f"File not found: {path}")
            except Exception as e:
                self.send_error(500, f"Internal server error: {e}")
    
    def serve_file(self, filepath: str, content_type: str):
        """Serve a static file"""
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
            
        except FileNotFoundError:
            self.send_error(404, f"File not found: {filepath}")
        except Exception as e:
            self.send_error(500, f"Error reading file: {e}")
    
    def serve_json(self, data: Dict[str, Any]):
        """Serve JSON response"""
        json_data = json.dumps(data, indent=2)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(json_data))
        self.end_headers()
        self.wfile.write(json_data.encode('utf-8'))
    
    def guess_type(self, path: str) -> str:
        """Guess content type based on file extension"""
        extension_map = {
            '.html': 'text/html',
            '.htm': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.json': 'application/json',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.ico': 'image/x-icon',
            '.txt': 'text/plain',
            '.xml': 'application/xml',
            '.pdf': 'application/pdf',
        }
        
        ext = os.path.splitext(path)[1].lower()
        return extension_map.get(ext, 'application/octet-stream')


def run_server(port: int = 8000, bind_address: str = 'localhost'):
    """
    Run the web server
    
    Args:
        port: Port number (default: 8000)
        bind_address: Bind address (default: localhost)
    """
    handler = CustomHTTPRequestHandler
    
    try:
        with socketserver.TCPServer((bind_address, port), handler) as httpd:
            print("="*60)
            print("SIMPLE WEB SERVER")
            print("="*60)
            print(f"Server running at: http://{bind_address}:{port}")
            print(f"Local: http://localhost:{port}")
            print(f"Network: http://{bind_address}:{port}")
            print("="*60)
            print("Press Ctrl+C to stop the server")
            print("="*60)
            
            # Change to the directory where the script is located
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n" + "="*60)
        print("Server stopped by user")
        print("="*60)
    except OSError as e:
        if e.errno == 10048:  # Port already in use on Windows
            print(f"Error: Port {port} is already in use.")
            print(f"Try a different port: python server.py --port 8080")
        else:
            print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
