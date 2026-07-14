#!/usr/bin/env python3
"""
TCP Client - Simple socket client
"""

import socket
import sys


class TCPClient:
    """Simple TCP client"""
    
    def __init__(self, host: str = 'localhost', port: int = 5000):
        self.host = host
        self.port = port
        self.socket = None
    
    def connect(self) -> bool:
        """Connect to server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"Connected to {self.host}:{self.port}")
            return True
        except socket.error as e:
            print(f"Connection failed: {e}")
            return False
    
    def send_message(self, message: str) -> str:
        """Send message and receive response"""
        if not self.socket:
            return "Not connected"
        
        try:
            self.socket.send(message.encode('utf-8'))
            response = self.socket.recv(1024).decode('utf-8')
            return response
        except socket.error as e:
            return f"Error: {e}"
    
    def disconnect(self):
        """Disconnect from server"""
        if self.socket:
            self.socket.close()
            self.socket = None
            print("Disconnected")


def main():
    """Main entry point"""
    import sys
    
    host = 'localhost'
    port = 5000
    
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print(f"Invalid port: {sys.argv[2]}")
            return
    
    client = TCPClient(host, port)
    
    print("="*60)
    print("TCP CLIENT")
    print("="*60)
    
    if not client.connect():
        return
    
    print("\nType 'help' for commands, 'quit' to exit")
    print("-"*60)
    
    try:
        response = client.socket.recv(1024).decode('utf-8')
        print(response)
        
        while True:
            message = input("\n> ").strip()
            
            if not message:
                continue
            
            if message.lower() == 'quit':
                client.send_message(message)
                break
            
            response = client.send_message(message)
            print(response)
            
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.disconnect()
        print("Client terminated")


if __name__ == "__main__":
    main()
