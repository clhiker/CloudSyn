#!/usr/bin/python
# encoding=utf-8

import socket
import configparser
import os
import time


import aes
import filetree
import HashCode
import load


# 客户端
class Client:
    def __init__(self):
        self.address = ()
        self.local_path = ''
        self.home_path = ''
        self.buff = 1024
        self.block_size = 1024
        self.getConfig()
        # 连接选项
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client_socket.connect(self.address)

        self.aes_local = aes.AESCrypto()
        self.file_tree = filetree.FileTree()
        self.file_tree.storeFilesLocal()

        self.hash_generator = HashCode.MD5()

        self.load_generator = load.Load(self.buff)
        self.load_generator.setClient(self.client_socket)

    def getConfig(self):
        config = configparser.ConfigParser()
        config.read('local.ini')
        ip = config.get('address', 'ip')
        port = int(config.get('address', 'port'))
        self.address = (ip, port)
        self.local_path = config.get('path', 'store_path')
        self.home_path = config.get('path', 'home_path')
        
        self.buff = int(config.get('spilt', 'buff'))
        self.block_size = int(config.get('spilt', 'block_size'))

    def sendFilesInfo(self):
        self.client_socket.send(self.aes_local.encrypt_str('file_struct').encode())
        time.sleep(0.005)

        self.load_generator.upload(self.local_path)

    def waitCheck(self):
        print('check')
        check_info = self.aes_local.decrypt_str(self.client_socket.recv(self.buff).decode())

        if check_info == 'syn':
            self.load_generator.download(self.local_path)
            self.synFiles()

    def synFiles(self):
        download_list = []
        try:            
            with open(self.local_path, 'r') as f:
                for line in f:
                    part_path = line.replace('\n', '')                    
                    download_list.append(part_path)
        except IOError:
            print('文件打开失败')
        
        for item in download_list:
            real_path = self.home_path + item

            self.client_socket.send(self.aes_local.encrypt_str('continue').encode())
            time.sleep(0.003)
            self.client_socket.send(self.aes_local.encrypt_str(item).encode())
            time.sleep(0.003)
            self.client_socket.recv(self.buff)

            print(real_path)
            self.load_generator.upload(real_path)
            # print('我在这等着')
            self.client_socket.recv(self.buff)
            # print('我走到这一步了')

        self.client_socket.send(self.aes_local.encrypt_str('stop').encode())
            

def main():
    client = Client()
    client.sendFilesInfo()
    client.waitCheck()

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('local.ini')
    time_stamp = int(config.get('config', 'time_stamp'))

    old_time = time.time()
    new_time = time.time()
    while True:
        new_time = time.time()
        if new_time - old_time > time_stamp:
            main()
            old_time = time.time()
        else:
            pass
