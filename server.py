"""
YouTube Privacy Downloader - Web Server
Uses only Python standard library - No external dependencies
"""

import http.server
import socketserver
import json
import urllib.parse
import os
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import mimetypes
from youtube_downloader import YouTubeDownloader


class DownloadRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Handle HTTP requests for the YouTube downloader"""
    
    def __init__(self, *args, **kwargs):
        self.downloader = YouTubeDownloader("downloads")
        super().__init__(*args, directory=".", **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        
        # API endpoint: Get video info
        if path == '/api/video-info':
            self.handle_video_info(query_params)
        
        # API endpoint: Get video formats
        elif path == '/api/formats':
            self.handle_formats(query_params)
        
        # API endpoint: Download video
        elif path == '/api/download':
            self.handle_download(query_params)
        
        # API endpoint: Privacy check
        elif path == '/api/privacy':
            self.handle_privacy()
        
        # API endpoint: Get download history
        elif path == '/api/history':
            self.handle_history()
        
        # Serve static files and index.html
        else:
            self.serve_static(path)
    
    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == '/api/submit-url':
            self.handle_submit_url(body)
        else:
            self.send_error(404)
    
    def handle_video_info(self, params):
        """Get video information from YouTube URL"""
        try:
            url = params.get('url', [''])[0]
            if not url:
                self.send_json_response({'error': 'URL parameter required'}, 400)
                return
            
            video_id = self.downloader.extract_video_id(url)
            if not video_id:
                self.send_json_response({'error': 'Invalid YouTube URL'}, 400)
                return
            
            info = self.downloader.get_video_info(video_id)
            self.send_json_response(info)
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def handle_formats(self, params):
        """Get available video formats"""
        try:
            video_id = params.get('video_id', [''])[0]
            formats = self.downloader.get_available_formats(video_id)
            self.send_json_response({'formats': formats})
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def handle_download(self, params):
        """Download video"""
        try:
            video_id = params.get('video_id', [''])[0]
            title = params.get('title', ['Video'])[0]
            
            if not video_id:
                self.send_json_response({'error': 'video_id parameter required'}, 400)
                return
            
            result = self.downloader.simulate_download(video_id, title)
            self.send_json_response(result)
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def handle_privacy(self):
        """Get privacy information"""
        try:
            info = self.downloader.privacy_check()
            self.send_json_response(info)
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def handle_history(self):
        """Get download history"""
        try:
            history = []
            downloads_path = Path("downloads")
            if downloads_path.exists():
                for file in downloads_path.glob("*.json"):
                    with open(file, 'r') as f:
                        history.append(json.load(f))
            self.send_json_response({'history': history})
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def handle_submit_url(self, body):
        """Handle URL submission"""
        try:
            data = json.loads(body)
            url = data.get('url', '')
            
            video_id = self.downloader.extract_video_id(url)
            if not video_id:
                self.send_json_response({'error': 'Invalid YouTube URL'}, 400)
                return
            
            info = self.downloader.get_video_info(video_id)
            info['video_id'] = video_id
            self.send_json_response(info)
        except json.JSONDecodeError:
            self.send_json_response({'error': 'Invalid JSON'}, 400)
        except Exception as e:
            self.send_json_response({'error': str(e)}, 500)
    
    def serve_static(self, path):
        """Serve static files or index.html"""
        if path == '/' or path == '':
            self.serve_index()
        elif path.startswith('/static/'):
            self.serve_file(path)
        else:
            self.send_error(404)
    
    def serve_index(self):
        """Serve the main index.html page"""
        try:
            with open('templates/index.html', 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "index.html not found")
    
    def serve_file(self, path):
        """Serve static files"""
        try:
            file_path = path.lstrip('/')
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                content_type, _ = mimetypes.guess_type(file_path)
                if content_type is None:
                    content_type = 'application/octet-stream'
                
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404)
        except Exception as e:
            self.send_error(500, str(e))
    
    def send_json_response(self, data, status=200):
        """Send JSON response"""
        response_data = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', len(response_data))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(response_data)
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        return


def run_server(host='localhost', port=8000, verbose=False):
    """Run the web server"""
    handler = DownloadRequestHandler
    
    with socketserver.TCPServer((host, port), handler) as httpd:
        if verbose:
            print(f"✓ Server started on http://{host}:{port}")
            print(f"✓ Open your browser to access the application")
            print(f"✓ Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            if verbose:
                print("\n✓ Server stopped")
            pass


if __name__ == '__main__':
    run_server(verbose=True)
