"""
CLI Logger Module
Provides command-line logging with colors, timestamps, and file output
"""

import datetime
import os
from pathlib import Path
from enum import Enum


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"


class Colors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright foreground colors
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'


class CLILogger:
    """Command-line logger with colored output and file logging"""
    
    def __init__(self, log_dir="logs", log_file="app.log", verbose=True):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / log_file
        self.verbose = verbose
        self.start_time = datetime.datetime.now()
        
    def _get_timestamp(self):
        """Get current timestamp"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _get_elapsed_time(self):
        """Get elapsed time since logger creation"""
        elapsed = datetime.datetime.now() - self.start_time
        minutes, seconds = divmod(int(elapsed.total_seconds()), 60)
        return f"{minutes}m {seconds}s"
    
    def _format_message(self, level: LogLevel, message: str) -> tuple:
        """Format message with timestamp and level"""
        timestamp = self._get_timestamp()
        
        # Colored output for terminal
        level_colors = {
            LogLevel.DEBUG: Colors.CYAN,
            LogLevel.INFO: Colors.BLUE,
            LogLevel.SUCCESS: Colors.GREEN,
            LogLevel.WARNING: Colors.YELLOW,
            LogLevel.ERROR: Colors.RED,
        }
        
        color = level_colors.get(level, Colors.WHITE)
        colored_level = f"{color}{level.value:8s}{Colors.RESET}"
        colored_message = f"{Colors.DIM}[{timestamp}]{Colors.RESET} {colored_level} {message}"
        
        # Plain text for file
        plain_message = f"[{timestamp}] [{level.value:8s}] {message}"
        
        return colored_message, plain_message
    
    def _write_to_file(self, message: str):
        """Write message to log file"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(message + '\n')
        except IOError as e:
            if self.verbose:
                print(f"Failed to write to log file: {e}")
    
    def debug(self, message: str):
        """Log debug message"""
        colored, plain = self._format_message(LogLevel.DEBUG, message)
        if self.verbose:
            print(colored)
        self._write_to_file(plain)
    
    def info(self, message: str):
        """Log info message"""
        colored, plain = self._format_message(LogLevel.INFO, message)
        if self.verbose:
            print(colored)
        self._write_to_file(plain)
    
    def success(self, message: str):
        """Log success message"""
        colored, plain = self._format_message(LogLevel.SUCCESS, message)
        if self.verbose:
            print(colored)
        self._write_to_file(plain)
    
    def warning(self, message: str):
        """Log warning message"""
        colored, plain = self._format_message(LogLevel.WARNING, message)
        if self.verbose:
            print(colored)
        self._write_to_file(plain)
    
    def error(self, message: str):
        """Log error message"""
        colored, plain = self._format_message(LogLevel.ERROR, message)
        if self.verbose:
            print(colored)
        self._write_to_file(plain)
    
    def print_header(self, title: str):
        """Print formatted header"""
        border = "=" * 60
        header = f"{Colors.BOLD}{Colors.BRIGHT_CYAN}{border}{Colors.RESET}\n"
        header += f"{Colors.BOLD}{Colors.BRIGHT_CYAN}{title:^60}{Colors.RESET}\n"
        header += f"{Colors.BOLD}{Colors.BRIGHT_CYAN}{border}{Colors.RESET}"
        
        if self.verbose:
            print(header)
    
    def print_section(self, title: str):
        """Print formatted section"""
        section = f"{Colors.BOLD}{Colors.BRIGHT_MAGENTA}→ {title}{Colors.RESET}"
        if self.verbose:
            print(section)
    
    def print_summary(self, items: dict):
        """Print summary of items"""
        if self.verbose:
            print(f"{Colors.BOLD}{Colors.BRIGHT_CYAN}Summary:{Colors.RESET}")
            for key, value in items.items():
                print(f"  {Colors.CYAN}●{Colors.RESET} {key}: {Colors.BRIGHT_WHITE}{value}{Colors.RESET}")
    
    def get_log_file_path(self):
        """Get the path to the log file"""
        return str(self.log_file)
    
    def clear_logs(self):
        """Clear all log files"""
        try:
            if self.log_file.exists():
                self.log_file.unlink()
                self.info(f"Logs cleared: {self.log_file}")
        except IOError as e:
            self.error(f"Failed to clear logs: {e}")


def create_logger(verbose=True, log_dir="logs", log_file="app.log"):
    """Factory function to create a logger instance"""
    return CLILogger(log_dir=log_dir, log_file=log_file, verbose=verbose)
