#!/usr/bin/env python3
"""
Chat Server - Multi-client chat server
"""

import socket
import threading
import datetime
import os
from typing import List, Dict


class ChatServer:
    """Multi-client chat server"""
    
    def __init__(self, host: str = 'localhost', port: int = 5001):
        self.host = host
        self.port = port
        self.clients: Dict[socket.socket, str] = {}
        self.nicknames: Dict[str, socket.socket] = {}
        self.running = False
        self.server_socket = None
        self.lock = threading.Lock()
        self.log_file = "logs/chat_server.log"
        
        os.makedirs("logs", exist_ok=True)
    
    def log(self, message: str):
        """Log message"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_msg + '\n')
    
    def broadcast(self, message: str, sender: socket.socket = None):
        """Broadcast message to all clients except sender"""
        with self.lock:
            for client in self.clients:
                if client != sender:
                    try:
                        client.send(message.encode('utf-8'))
                    except:
                        self.remove_client(client)
    
    def broadcast_all(self, message: str):
        """Broadcast message to all clients"""
        with self.lock:
            for client in self.clients:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    self.remove_client(client)
    
    def remove_client(self, client: socket.socket):
        """Remove client from server"""
        with self.lock:
            if client in self.clients:
                nickname = self.clients[client]
                del self.clients[client]
                if nickname in self.nicknames:
                    del self.nicknames[nickname]
                self.log(f"Client removed: {nickname}")
                self.broadcast_all(f"[SYSTEM] {nickname} has left the chat")
    
    def handle_client(self, client: socket.socket, address: tuple):
        """Handle client connection"""
        try:
            client.send("NICK".encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8').strip()
            
            if not nickname:
                client.send("Invalid nickname".encode('utf-8'))
                client.close()
                return
            
            with self.lock:
                if nickname in self.nicknames:
                    client.send("Nickname already taken".encode('utf-8'))
                    client.close()
                    return
                
                self.clients[client] = nickname
                self.nicknames[nickname] = client
            
            client.send(f"Welcome {nickname}!".encode('utf-8'))
            self.log(f"New client: {nickname} from {address}")
            self.broadcast_all(f"[SYSTEM] {nickname} has joined the chat")
            
            while self.running:
                try:
                    message = client.recv(1024).decode('utf-8')
                    if not message:
                        break
                    
                    if message.lower() == '/quit':
                        break
                    elif message.lower() == '/users':
                        with self.lock:
                            users = ", ".join(self.clients.values())
                        client.send(f"Users online: {users}".encode('utf-8'))
                    elif message.lower() == '/help':
                        help_text = """Chat Commands:
    /quit - Leave chat
    /users - Show online users
    /help - Show this help
    /msg <user> <message> - Send private message
    Just type your message to chat with everyone"""
                        client.send(help_text.encode('utf-8'))
                    elif message.startswith('/msg '):
                        parts = message.split(' ', 2)
                        if len(parts) >= 3:
                            target = parts[1]
                            msg = parts[2]
                            with self.lock:
                                if target in self.nicknames:
                                    target_client = self.nicknames[target]
                                    try:
                                        target_client.send(f"[PM from {nickname}] {msg}".encode('utf-8'))
                                        client.send(f"[PM to {target}] {msg}".encode('utf-8'))
                                    except:
                                        client.send(f"User {target} is offline".encode('utf-8'))
                                else:
                                    client.send(f"User {target} not found".encode('utf-8'))
                    else:
                        self.broadcast(f"[{nickname}] {message}", client)
                        
                except socket.error as e:
                    self.log(f"Socket error with {nickname}: {e}")
                    break
                except Exception as e:
                    self.log(f"Error with {nickname}: {e}")
                    break
                    
        except Exception as e:
            self.log(f"Error handling client {address}: {e}")
        finally:
            self.remove_client(client)
            client.close()
    
    def start(self):
        """Start the server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            self.log(f"Chat server started on {self.host}:{self.port}")
            print("="*60)
            print("CHAT SERVER")
            print("="*60)
            print(f"Host: {self.host}")
            print(f"Port: {self.port}")
            print("Press Ctrl+C to stop")
            print("="*60)
            
            while self.running:
                try:
                    client, address = self.server_socket.accept()
                    thread = threading.Thread(
                        target=self.handle_client,
                        args=(client, address)
                    )
                    thread.daemon = True
                    thread.start()
                    
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
    
    def stop(self):
        """Stop the server"""
        self.running = False
        
        with self.lock:
            for client in list(self.clients.keys()):
                try:
                    client.send("[SYSTEM] Server is shutting down".encode('utf-8'))
                    client.close()
                except:
                    pass
            self.clients.clear()
            self.nicknames.clear()
        
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        self.log("Chat server stopped")


def main():
    """Main entry point"""
    import sys
    
    host = 'localhost'
    port = 5001
    
    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print(f"Invalid port: {sys.argv[2]}")
            return
    
    server = ChatServer(host, port)
    server.start()


if __name__ == "__main__":
    main()
