#!/usr/bin/env python3
"""
Chat Client - Multi-client chat client
"""

import socket
import threading
import sys


class ChatClient:
    """Chat client for multi-user chat"""
    
    def __init__(self, host: str = 'localhost', port: int = 5001):
        self.host = host
        self.port = port
        self.socket = None
        self.nickname = None
        self.running = False
    
    def connect(self) -> bool:
        """Connect to server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            
            self.nickname = input("Enter your nickname: ").strip()
            if not self.nickname:
                print("Nickname cannot be empty")
                return False
            
            self.socket.send(self.nickname.encode('utf-8'))
            
            response = self.socket.recv(1024).decode('utf-8')
            if "Welcome" not in response and "Nickname" not in response:
                print(f"Error: {response}")
                return False
            
            print(response)
            self.running = True
            
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            return True
            
        except socket.error as e:
            print(f"Connection failed: {e}")
            return False
    
    def receive_messages(self):
        """Receive messages from server"""
        while self.running:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"\n{message}")
                print("> ", end="", flush=True)
            except socket.error:
                break
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
        
        self.running = False
    
    def send_message(self, message: str):
        """Send message to server"""
        if not self.socket:
            return
        
        try:
            self.socket.send(message.encode('utf-8'))
        except socket.error as e:
            print(f"Error sending message: {e}")
            self.running = False
    
    def disconnect(self):
        """Disconnect from server"""
        self.running = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
        print("Disconnected")


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
    
    client = ChatClient(host, port)
    
    print("="*60)
    print("CHAT CLIENT")
    print("="*60)
    
    if not client.connect():
        return
    
    print("\nType /help for commands, /quit to exit")
    print("-"*60)
    
    try:
        while client.running:
            message = input("> ").strip()
            if not message:
                continue
            
            if message.lower() == '/quit':
                client.send_message(message)
                break
            
            client.send_message(message)
            
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.disconnect()
        print("Chat client terminated")


if __name__ == "__main__":
    main()
