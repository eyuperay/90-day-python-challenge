#!/usr/bin/env python3
"""
TCP Server - Simple socket server
"""

import socket
import threading
import datetime
import os
from typing import List, Dict


class TCPServer:
    """Simple TCP server with multi-client support"""
    
    def __init__(self, host: str = 'localhost', port: int = 5000):
        self.host = host
        self.port = port
        self.clients: List[socket.socket] = []
        self.client_addresses: Dict[socket.socket, str] = {}
        self.running = False
        self.server_socket = None
        self.log_file = "logs/server.log"
        
        os.makedirs("logs", exist_ok=True)
    
    def log(self, message: str):
        """Log message to file and console"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_msg + '\n')
    
    def start(self):
        """Start the server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            self.log(f"Server started on {self.host}:{self.port}")
            print("="*60)
            print("TCP SERVER")
            print("="*60)
            print(f"Host: {self.host}")
            print(f"Port: {self.port}")
            print("Press Ctrl+C to stop")
            print("="*60)
            
            while self.running:
                try:
                    client_socket, address = self.server_socket.accept()
                    self.clients.append(client_socket)
                    self.client_addresses[client_socket] = f"{address[0]}:{address[1]}"
                    
                    self.log(f"New client connected: {address}")
                    
                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.error as e:
                    if self.running:
                        self.log(f"Socket error: {e}")
                except Exception as e:
                    if self.running:
                        self.log(f"Error: {e}")
                        
        except KeyboardInterrupt:
            self.log("Server stopped by user")
        except Exception as e:
            self.log(f"Server error: {e}")
        finally:
            self.stop()
    
    def handle_client(self, client_socket: socket.socket, address: tuple):
        """Handle client connection"""
        try:
            client_socket.settimeout(60)
            client_ip = f"{address[0]}:{address[1]}"
            
            welcome = "Welcome to the TCP Server!\nType 'quit' to disconnect.\n"
            client_socket.send(welcome.encode('utf-8'))
            
            while self.running:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    
                    message = data.decode('utf-8').strip()
                    self.log(f"Received from {client_ip}: {message}")
                    
                    if message.lower() == 'quit':
                        response = "Goodbye!"
                        client_socket.send(response.encode('utf-8'))
                        break
                    elif message.lower() == 'time':
                        response = f"Server time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                        client_socket.send(response.encode('utf-8'))
                    elif message.lower() == 'echo':
                        response = "Echo: Type something to echo back"
                        client_socket.send(response.encode('utf-8'))
                    elif message.lower() == 'help':
                        response = """Available commands:
    time - Show server time
    echo - Echo your messages
    help - Show this help
    quit - Disconnect"""
                        client_socket.send(response.encode('utf-8'))
                    else:
                        response = f"Server says: {message}"
                        client_socket.send(response.encode('utf-8'))
                        
                except socket.timeout:
                    client_socket.send(b'')
                except socket.error as e:
                    self.log(f"Socket error with {client_ip}: {e}")
                    break
                    
        except Exception as e:
            self.log(f"Error handling client {address}: {e}")
        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            if client_socket in self.client_addresses:
                del self.client_addresses[client_socket]
            client_socket.close()
            self.log(f"Client disconnected: {address}")
    
    def stop(self):
        """Stop the server"""
        self.running = False
        
        for client in self.clients[:]:
            try:
                client.close()
            except:
                pass
        self.clients.clear()
        self.client_addresses.clear()
        
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        self.log("Server stopped")


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
    
    server = TCPServer(host, port)
    server.start()


if __name__ == "__main__":
    main()
