#!/usr/bin/env python3
"""
PrivateTube - Main Entry Point
YouTube Privacy-Focused Downloader
Built from scratch with Python standard library only
"""

import sys
import argparse
import webbrowser
import time
from pathlib import Path
from cli_logger import create_logger
from server import run_server
from youtube_downloader import create_downloader


class PrivateTubeApp:
    """Main application controller"""
    
    def __init__(self, verbose=True):
        self.logger = create_logger(verbose=verbose)
        self.downloader = create_downloader()
        self.verbose = verbose
    
    def print_welcome(self):
        """Print welcome message"""
        self.logger.print_header("PrivateTube - YouTube Privacy Downloader")
        self.logger.print_section("Welcome to PrivateTube")
        
        if self.verbose:
            print()
            print(f"{self._color('CYAN')}Features:{self._color('RESET')}")
            print(f"  {self._color('GREEN')}✓{self._color('RESET')} 100% Private - No external dependencies")
            print(f"  {self._color('GREEN')}✓{self._color('RESET')} Built from scratch with Python stdlib")
            print(f"  {self._color('GREEN')}✓{self._color('RESET')} Beautiful Netflix-inspired UI")
            print(f"  {self._color('GREEN')}✓{self._color('RESET')} Command-line logging interface")
            print(f"  {self._color('GREEN')}✓{self._color('RESET')} Zero configuration needed")
            print()
    
    def print_startup_info(self, host, port):
        """Print startup information"""
        self.logger.print_section("Server Configuration")
        
        print()
        print(f"  {self._color('CYAN')}Server URL:{self._color('RESET')} http://{host}:{port}")
        print(f"  {self._color('CYAN')}Log File:{self._color('RESET')} {self.logger.get_log_file_path()}")
        print(f"  {self._color('CYAN')}Download Dir:{self._color('RESET')} {Path('downloads').absolute()}")
        print()
        
        self.logger.success(f"Server is running on http://{host}:{port}")
        self.logger.info(f"Log file: {self.logger.get_log_file_path()}")
        self.logger.info(f"Download directory: {Path('downloads').absolute()}")
    
    def print_instructions(self, host, port):
        """Print usage instructions"""
        self.logger.print_section("How to Use")
        
        print()
        print(f"  1. Open your browser to: {self._color('BRIGHT_CYAN')}http://{host}:{port}{self._color('RESET')}")
        print(f"  2. Paste a YouTube URL in the input field")
        print(f"  3. Click 'Fetch Info' to get video details")
        print(f"  4. Select quality and click 'Download'")
        print(f"  5. Check your download history below")
        print()
        print(f"  {self._color('YELLOW')}⚠ Press Ctrl+C to stop the server{self._color('RESET')}")
        print()
    
    def print_privacy_info(self):
        """Print privacy information"""
        self.logger.print_section("Privacy Guarantee")
        
        privacy = self.downloader.privacy_check()
        
        print()
        for key, value in privacy.items():
            if key != 'description':
                label = key.replace('_', ' ').title()
                print(f"  {self._color('GREEN')}●{self._color('RESET')} {label}: {value}")
        
        print()
        print(f"  {self._color('BRIGHT_CYAN')}{privacy['description']}{self._color('RESET')}")
        print()
    
    def _color(self, color_name):
        """Get ANSI color code"""
        colors = {
            'RESET': '\033[0m',
            'BOLD': '\033[1m',
            'DIM': '\033[2m',
            'CYAN': '\033[36m',
            'GREEN': '\033[32m',
            'YELLOW': '\033[33m',
            'BLUE': '\033[34m',
            'RED': '\033[31m',
            'BRIGHT_CYAN': '\033[96m',
        }
        return colors.get(color_name, '')
    
    def start_server(self, host='localhost', port=8000, open_browser=True):
        """Start the application server"""
        self.print_welcome()
        self.print_startup_info(host, port)
        self.print_privacy_info()
        self.print_instructions(host, port)
        
        # Open browser if requested
        if open_browser:
            self.logger.info("Opening browser...")
            try:
                webbrowser.open(f'http://{host}:{port}')
                time.sleep(1)
            except Exception as e:
                self.logger.warning(f"Could not open browser automatically: {e}")
        
        try:
            self.logger.info("Starting web server...")
            run_server(host=host, port=port, verbose=False)
        except KeyboardInterrupt:
            self.print_shutdown()
            self.logger.success("Server stopped successfully")
            sys.exit(0)
        except OSError as e:
            if "Address already in use" in str(e):
                self.logger.error(f"Port {port} is already in use")
                self.logger.info("Try using a different port with --port option")
                sys.exit(1)
            else:
                self.logger.error(f"Server error: {e}")
                sys.exit(1)
    
    def print_shutdown(self):
        """Print shutdown message"""
        print()
        self.logger.print_section("Shutting Down")
        print()
        self.logger.success("Thank you for using PrivateTube!")
        self.logger.info("All your data has been kept private and secure")
        print()
    
    def show_help(self):
        """Show detailed help message"""
        self.print_welcome()
        print()
        self.logger.print_section("Command Line Options")
        print()
        print("  --host HOST          Server host address (default: localhost)")
        print("  --port PORT          Server port (default: 8000)")
        print("  --no-browser         Don't open browser automatically")
        print("  --quiet              Suppress CLI output")
        print("  --help               Show this help message")
        print()
        self.logger.print_section("Examples")
        print()
        print("  # Start with default settings")
        print("  python app.py")
        print()
        print("  # Use custom port")
        print("  python app.py --port 3000")
        print()
        print("  # Make server accessible on network")
        print("  python app.py --host 0.0.0.0")
        print()
        print("  # Start without opening browser")
        print("  python app.py --no-browser")
        print()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        prog='PrivateTube',
        description='YouTube Privacy-Focused Downloader',
        add_help=False
    )
    
    parser.add_argument('--host', type=str, default='localhost',
                        help='Server host address (default: localhost)')
    parser.add_argument('--port', type=int, default=8000,
                        help='Server port (default: 8000)')
    parser.add_argument('--no-browser', action='store_true',
                        help='Don\'t open browser automatically')
    parser.add_argument('--quiet', action='store_true',
                        help='Suppress CLI output')
    parser.add_argument('--help', action='store_true',
                        help='Show help message')
    parser.add_argument('--version', action='store_true',
                        help='Show version information')
    
    args = parser.parse_args()
    
    # Create app instance
    app = PrivateTubeApp(verbose=not args.quiet)
    
    # Handle special commands
    if args.help:
        app.show_help()
        sys.exit(0)
    
    if args.version:
        app.logger.info("PrivateTube v1.0.0")
        app.logger.info("Privacy-focused YouTube downloader")
        sys.exit(0)
    
    # Validate port
    if args.port < 1024 or args.port > 65535:
        app.logger.error(f"Invalid port: {args.port}. Port must be between 1024 and 65535")
        sys.exit(1)
    
    # Start server
    app.start_server(
        host=args.host,
        port=args.port,
        open_browser=not args.no_browser
    )


if __name__ == '__main__':
    main()
