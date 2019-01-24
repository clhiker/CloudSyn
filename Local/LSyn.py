#!/usr/bin/python
# encoding=utf-8

import os
import socket
import configparser
import struct
import aes
import time
import filetree


# 客户端
class Client:
    def __init__(self):
        self.address = ()
        self.local_info = ''
        self.buff = 1024
        self.block_size = 1024
        self.getConfig()
        # 连接选项
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client_socket.connect(self.address)

        self.aes_local = aes.AESCrypto()
        self.file_tree = filetree.FileTree()
        self.file_tree.storeFilesLocal()

    def getConfig(self):
        config = configparser.ConfigParser()
        config.read('local.ini')
        ip = config.get('address', 'ip')
        port = int(config.get('address', 'port'))
        self.address = (ip, port)
        self.local_info = config.get('path', 'store_path')
        self.buff = int(config.get('spilt', 'buff'))
        self.block_size = int(config.get('spilt', 'block_size'))

    def send_files_info(self):
        self.client_socket.send(self.aes_local.encrypt_str('file_struct').encode())
        time.sleep(0.005)

        self.upload(self.local_info)

    def upload(self, filename):
        file_length = os.path.getsize(self.local_info)
        spilt_num = file_length // self.buff
        end_length = file_length - spilt_num * self.buff

        file_length_info = struct.pack('ii', spilt_num, end_length)
        self.client_socket.send(self.aes_local.encrypt_bin(file_length_info))

        with open(self.local_info, 'rb') as f:
            while True:
                line = f.read(self.buff)
                if not line:
                    break
                encrypt_line = self.aes_local.encrypt_bin(line)
                self.client_socket.send(encrypt_line)


if __name__ == '__main__':
    client = Client()
    client.send_files_info()

