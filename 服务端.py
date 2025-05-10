#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
局域网聊天程序 - 服务端
作者: [你的名字]
版本: 1.0
"""
import socket
import threading

class ChatServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        
    def start(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f"服务器已启动，监听 {self.host}:{self.port}")
        
        while True:
            client, address = self.server.accept()
            client_name = address[0]
            self.clients[client] = client_name
            print(f"{client_name} 已连接")
            
            thread = threading.Thread(
                target=self.handle_client,
                args=(client,)
            )
            thread.start()
            
    def handle_client(self, client):
        client_ip, client_port = client.getpeername()
        client_name = f"{client_ip}:{client_port}"  # 默认使用IP:端口
        
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if not message:
                    break
                    
                # 处理用户名设置
                if message.startswith("/username "):
                    client_name = message[9:]  # 获取用户名
                    self.clients[client] = client_name
                    print(f"用户 {client_name} (IP: {client_ip}) 已连接")
                    continue
                    
                formatted_msg = f"{client_name} (IP: {client_ip})> {message}"
                print(formatted_msg)
                self.broadcast(formatted_msg, client)
                
            except:
                print(f"用户 {client_name} (IP: {client_ip}) 已断开连接")
                del self.clients[client]
                client.close()
                break
                
    def broadcast(self, message, sender):
        for client in self.clients:
            if client != sender:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    continue

if __name__ == "__main__":
    server = ChatServer()
    server.start()