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
        # 读取配置文件
        self.readConfig()                
        # 绑定地址
        self.server_socket.bind(self.address)
        # 最多三台设备
        self.server_socket.listen(int(self.max_supported_devices))

        self.aes_remote = aes.AESCrypto()


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

        if os.path.exists(self.store_path):
            os.remove(self.store_path)

        spilt_num = int(client.recv(self.buff).decode())
        count = 0
        while True:
            # data = client.recv(self.buff)
            # if data != None:
            #     test = self.aes_remote.decrypt_bin(data)
            # print(test)
            # if not data:
            #     break


            # receive = client.recv(self.buff)
            # if receive == b'':
            #     break
            # data = self.aes_remote.decrypt_bin(receive)
            # if not data:
            #     break
            # try:
            #     with open(self.store_path, 'ab') as f:
            #         # print(data)
            #         f.write(data)
            #
            # except IOError as error:
            #     print('File error:' + str(error))

            receive = client.recv(self.buff)
            if receive == b'':
                break

            data = struct.unpack(str(self.buff) + 's', receive)[0]
            de_data = self.aes_remote.decrypt_bin(data)

            if count == spilt_num:
                end_length = int(client.recv(self.buff).decode())
                de_data = de_data[:end_length]

            if not receive:
                break
            try:
                with open(self.store_path, 'ab') as f:
                    f.write(de_data)

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

if __name__ == '__main__':
    server_start = Server()
    print('begin connecting...')
    server_start.beginInterface()