# -*- coding: utf-8 -*-
import socket
import time
import configparser
import threading
import os
import aes
import struct


class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = ()
        self.max_supported_devices = 3
        self.buff = 1024
        self.home_path = ''
        self.store_path = ''

        # 读取配置文件
        self.readConfig()

        # 绑定地址
        self.server_socket.bind(self.address)
        # 最多三台设备
        self.server_socket.listen(int(self.max_supported_devices))

        self.aes_remote = aes.AESCrypto()

        self.download_list = []

    # 读取配置信息
    def readConfig(self):
        config = configparser.ConfigParser()
        config.read('remote.ini')
        ip = config.get('socket_config', 'ip')
        port = config.get('socket_config', 'port')
        
        self.address = (ip, int(port))
        self.max_supported_devices = config.get('socket_config', 'max_supported_devices')

        self.buff = int(config.get('socket_config', 'buff'))
        
        self.home_path = config.get('path', 'home_path')

        self.store_path = config.get('path', 'store_path')

    def receiveFilesInfo(self, client):
        self.download(client, self.store_path)
        self.readFileStruct()

    # 检查文件目录结构信息
    def readFileStruct(self):

        count = 0
        item_type = ''
        name = ''
        up_path = self.home_path
        flag = False
        with open(self.store_path, 'r') as f:
            for line in f:
                if count == 0:
                    name = line[:line.rfind('\n')]
                if count == 1:
                    item_type = line[:line.rfind('\n')]

                    if item_type == 'dir':
                        self.checkDir(up_path, name)
                        up_path = up_path + os.sep + name
                        flag = True
                    else:
                        self.checkFile(up_path, name)

                    count = 0
                count += 1

    def addFile(self, up_path, name):
        path = up_path + os.sep + name
        path = path.replace(self.home_path, '')
        self.download_list.append(('file', path))

    def checkFile(self, up_path, name):
        files_list = os.listdir(up_path)
        if name not in files_list:
            path = up_path + os.sep + name
            path = path.replace(self.home_path, '')
            self.download_list.append(('file', path))

    def checkDir(self, up_path, name):
        files_list = os.listdir(up_path)
        if name not in files_list:
            path = up_path + os.sep + name
            path = path.replace(self.home_path, '')
            self.download_list.append(('dir', path))


    def download(self, client, filename):
        if os.path.exists(filename):
            os.remove(filename)
        file_length_info = self.aes_remote.decrypt_bin(client.recv(self.buff))
        (spilt_num, end_length) = struct.unpack('ii', file_length_info)

        line = b''
        count = 0
        while True:
            line += client.recv(self.buff)
            spilt_line = line[:self.buff]
            line = line[self.buff:]
            decrypt_line = self.aes_remote.decrypt_bin(spilt_line)

            try:
                if count == spilt_num:
                    decrypt_line = decrypt_line[:end_length]
                    with open(filename, 'ab') as f:
                        f.write(decrypt_line)
                    break
                else:
                    with open(filename, 'ab') as f:
                        f.write(decrypt_line)
            except IOError as error:
                print('File error:' + str(error))
            count += 1

    def receiveState(self, client, receive_info):
        # 目录信息
        if receive_info == 'file_struct':
            self.receiveFilesInfo(client)

    def beginInterface(self):
        while True:
            client, address = self.server_socket.accept()
            choice = self.aes_remote.decrypt_str(client.recv(self.buff).decode())
            print(choice)

            t = threading.Thread(target=self.receiveState, args=(client, choice))
            t.start()


class ItemNode:
    def __init__(self):
        self.name = ''
        self.item_type = ''
        self.path = ''

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setType(self, item_type):
        self.item_type = item_type

    def getType(self):
        return self.item_type


if __name__ == '__main__':
    server_start = Server()
    print('begin connecting...')
    server_start.beginInterface()