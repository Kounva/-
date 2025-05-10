#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
局域网聊天程序 - 客户端
作者: [你的名字] 
版本: 1.0
"""
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog

class ChatClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False
        
        # 获取用户名 - 使用临时Tkinter窗口
        temp_root = tk.Tk()
        temp_root.withdraw()
        self.username = simpledialog.askstring("用户名", "请输入你的用户名:", parent=temp_root)
        temp_root.destroy()  # 立即销毁临时窗口
        
        if not self.username:
            self.username = "匿名用户"
            
        self.client_name = socket.gethostbyname(socket.gethostname())
        self.running = False
        
        # 创建GUI界面
        self.root = tk.Tk()
        self.root.title(f"聊天客户端 - {self.client_name}")
        
        # 聊天记录显示区域
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)
        
        # 消息输入框
        self.msg_entry = tk.Entry(self.root)
        self.msg_entry.pack(padx=10, pady=5, fill=tk.X)
        self.msg_entry.bind("<Return>", self.send_message)
        
        # 发送按钮
        self.send_btn = tk.Button(self.root, text="发送", command=self.send_message)
        self.send_btn.pack(pady=5)
        
    def start(self):
        try:
            self.client.connect((self.host, self.port))
            # 首先发送用户名给服务器
            self.client.send(f"/username {self.username}".encode('utf-8'))
            self.display_message(f"已连接到服务器 {self.host}:{self.port}")
            self.display_message(f"你的用户名是: {self.username}")
            
            self.running = True
            receive_thread = threading.Thread(target=self.receive)
            receive_thread.daemon = True
            receive_thread.start()
            
            self.root.mainloop()
            
        except Exception as e:
            self.display_message(f"连接错误: {e}")
            self.client.close()
            
    def display_message(self, message):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
            
    def receive(self):
        while self.running:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if not message:
                    break
                self.display_message(message)
            except:
                self.display_message("\n与服务器断开连接")
                self.running = False
                self.client.close()
                break
                
    def send_message(self, event=None):
        message = self.msg_entry.get()
        if message:
            try:
                self.client.send(message.encode('utf-8'))
                self.display_message(f"{self.username}: {message}")
                self.msg_entry.delete(0, tk.END)
            except:
                self.display_message("发送失败")
                self.running = False

if __name__ == "__main__":
    client = ChatClient()
    client.start()