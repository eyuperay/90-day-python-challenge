#!/usr/bin/env python3
"""
Day 64 - Simple Web Server
Main entry point for the web server
"""

import sys
import os
import argparse
from simple_server import run_server


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Simple Web Server",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '-p', '--port',
        type=int,
        default=8000,
        help='Port number (default: 8000)'
    )
    
    parser.add_argument(
        '-b', '--bind',
        type=str,
        default='localhost',
        help='Bind address (default: localhost)'
    )
    
    parser.add_argument(
        '--host',
        action='store_true',
        help='Bind to 0.0.0.0 (all interfaces)'
    )
    
    args = parser.parse_args()
    
    # If --host is specified, bind to all interfaces
    bind_address = '0.0.0.0' if args.host else args.bind
    
    run_server(port=args.port, bind_address=bind_address)


if __name__ == "__main__":
    main()
