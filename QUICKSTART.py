#!/usr/bin/env python3
"""
Quick Start Guide - PrivateTube
This script provides helpful information to get started
"""

import sys
from pathlib import Path


def print_quick_start():
    """Print quick start guide"""
    print("\n" + "="*60)
    print(" PRIVATETUBE - QUICK START GUIDE ".center(60, "="))
    print("="*60 + "\n")
    
    print("📦 WHAT YOU HAVE:")
    print("-" * 60)
    print("✓ YouTube Privacy Downloader")
    print("✓ Beautiful Netflix-style Web UI")
    print("✓ Rich CLI with colored logging")
    print("✓ Built with Python standard library only")
    print("✓ Zero external dependencies")
    print("\n")
    
    print("🚀 HOW TO START:")
    print("-" * 60)
    print("\n1. BASIC START (Recommended):")
    print("   $ python app.py\n")
    print("   This will:")
    print("   • Start the web server on http://localhost:8000")
    print("   • Automatically open your browser")
    print("   • Show rich CLI logging\n")
    
    print("2. CUSTOM PORT:")
    print("   $ python app.py --port 3000\n")
    
    print("3. NETWORK ACCESS:")
    print("   $ python app.py --host 0.0.0.0\n")
    print("   Then access from other machines at:")
    print("   http://YOUR-MACHINE-IP:8000\n")
    
    print("4. WITHOUT BROWSER:")
    print("   $ python app.py --no-browser\n")
    
    print("5. QUIET MODE:")
    print("   $ python app.py --quiet\n")
    
    print("6. SHOW HELP:")
    print("   $ python app.py --help\n\n")
    
    print("🎯 QUICK USAGE:")
    print("-" * 60)
    print("1. Paste a YouTube URL")
    print("2. Click 'Fetch Info' to get video details")
    print("3. Select video quality")
    print("4. Click 'Download'")
    print("5. Check History for downloads\n")
    
    print("📁 FILES CREATED AUTOMATICALLY:")
    print("-" * 60)
    print("downloads/        → Downloaded videos")
    print("logs/app.log      → Application logs\n")
    
    print("🔒 PRIVACY GUARANTEE:")
    print("-" * 60)
    print("✓ All processing happens on YOUR computer")
    print("✓ No data collection or tracking")
    print("✓ No external dependencies")
    print("✓ Logs stored locally only\n")
    
    print("❓ HELP:")
    print("-" * 60)
    print("• Full docs: cat README.md")
    print("• CLI help:  python app.py --help")
    print("• Version:   python app.py --version\n")
    
    print("="*60)
    print("Ready to download? Run: python app.py".center(60))
    print("="*60 + "\n")


if __name__ == '__main__':
    print_quick_start()
