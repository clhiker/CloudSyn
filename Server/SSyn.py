# -*- coding: utf-8 -*-
import socket
import time
import configparser
import threading
import os
import base64
from Crypto.Cipher import AES

class Server:

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 读取配置文件
        self.readConfig()                
        # 绑定地址
        self.server_socket.bind(self.address)
        # 最多三台设备
        self.server_socket.listen(int(self.max_supported_devices))

        self.aes = AESCrypto()


    # 读取配置信息
    def readConfig(self):
        config = configparser.ConfigParser()
        config.read('remote.ini')
        ip = config.get('address', 'ip')
        port = config.get('address', 'port')
        
        self.address = (ip, int(port))
        self.max_supported_devices = config.get('config', 'max_supported_devices')

        self.buff = int(config.get('config', 'buff'))
        
        self.home_path = config.get('path', 'home_path')


    def receiveFilesInfo(self, client):

        pass



    def receiveState(self, client, receive_info):
        # 检查连接状态
        # 注册
        if receive_info == 'file_struct':
            self.receiveFilesInfo(client)

        # 登录
        if receive_info == 'check_for_username_and_password':
            self.checkForUsernameAndPassword(client)
        # 上传文件
        if receive_info == 'upload':
            self.uploadServer(client)
        # 获取文件路径结构
        if receive_info == 'ask_for_file':
            self.getFilePathStruct(client)
        if receive_info == 'delete_dir':
            self.deleteDirServer(client)
        if receive_info == 'delete_file':
            self.deleteFileServer(client)
        if receive_info == 'home_path':
            self.sendRootFileServer(client)
        # 下载文件
        if receive_info == 'download':
            self.downloadServer(client)
        if receive_info == 'cancel':
            self.deleteFileServer(client)
        if receive_info == 'get_files_list':
            self.sendFilesList(client)
        if receive_info == 'heart_beat':
            print(receive_info)
            self.life(client)

    def beginInterface(self):
        while True:
            client, address = self.server_socket.accept()
            choice = self.aes.decrypt_str(client.recv(self.buff).decode())
            print(choice)

            t = threading.Thread(target=self.receiveState, args=(client, choice))
            t.start()


class AESCrypto:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('remote.ini')
        self.key = config.get('crypto', 'key')


    def add_to_16(self, value):
        while len(value) % 16 != 0:
            value += '\0'
        return str.encode(value)  # 返回bytes

    #英文字符串加密方法
    def encrypt_str(self, str_text):
        # 初始化加密器
        aes = AES.new(self.add_to_16(self.key), AES.MODE_ECB)
        #先进行aes加密
        encrypt_aes = aes.encrypt(self.add_to_16(str_text))
        #用base64转成字符串形式
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
        return encrypted_text

    #英文字符串解密方法
    def decrypt_str(self, cipher_text):
        # 初始化加密器
        aes = AES.new(self.add_to_16(self.key), AES.MODE_ECB)
        #优先逆向解密base64成bytes
        base64_decrypted = base64.decodebytes(cipher_text.encode(encoding='utf-8'))
        #执行解密密并转码返回str
        decrypted_text = str(aes.decrypt(base64_decrypted),encoding='utf-8').replace('\0','')
        return decrypted_text

if __name__ == '__main__':
    server_start = Server()
    print('begin connecting...')
    server_start.beginInterface()