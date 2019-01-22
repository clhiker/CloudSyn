#!/usr/bin/python
#encoding=utf-8

import os
import io
import hashlib
import socket
import configparser
from Crypto.Cipher import AES
# from binascii import b2a_hex, a2b_hex
import base64
import struct

# 节点基类
class Node:
    def __init__(self):
        self.name = ''
        self.father = ''
        self.son = []

    def setName(self, name):
        self.name = name
    def getName(self):
        return self.name
    def setFather(self,father):
        self.father = father
    def getFather(self):
        return self.father
    def setSon(self, son):
        self.son = son
    def getSon(self):
        return self.son

# 节点类
class FileNode(Node):
    def __init__(self):
        super(FileNode, self).__init__()
        self.path = ''
        self.md5 = ''

    def setPath(self, path):
        self.path = path


    def setNode(self):
        self.name = self.path[self.path.rfind('/') + 1:]
        # 文件
        if not os.path.isdir(self.path):
            self.setMd5(self.path)
        # 文件夹
        else:
            self.md5 = 'dir'


    def setMd5(self, path):
        m = hashlib.md5()
        try:
            file = io.FileIO(path, 'r')
            bytes = file.read(1024)
            while (bytes != b''):
                m.update(bytes)
                bytes = file.read(1024)
            file.close()
            self.md5 = m.hexdigest()
        except:
            print('没有后缀名')

    def getMd5(self):
        return self.md5


# 深度优先文件树
class FilesTree:
    def __init__(self):

        self.home_path = ''
        self.local_info = ''
        self.getConfig()

        self.home_node = FileNode()
        self.home_node.setPath(self.home_path)
        self.home_node.setNode()

        # 返回一个广度优先遍历的列表
        self.node_tree = []
        self.setTree(self.home_path)

    def getConfig(self):
        config = configparser.ConfigParser()
        config.read('local.ini')
        self.home_path = config.get('path', 'home_path')
        self.local_info = config.get('path', 'store_path')

    # 构建树
    def setTree(self, up_path):
        files_list = os.listdir(up_path)
        for item in files_list:
            path = up_path + os.sep + item
            if os.path.isdir(path):
                dir_node = FileNode()
                dir_node.setPath(path)
                dir_node.setNode()
                self.node_tree.append(dir_node)
                self.setTree(path)
            else:
                file_node = FileNode()
                file_node.setPath(path)
                file_node.setNode()
                self.node_tree.append(file_node)

    def getNodeTree(self):
        return self.node_tree

    def storeFilesLocal(self):
        try:
            with open(self.local_info, 'w') as f:
                for item in self.node_tree:
                    f.write(item.getName())
                    f.write('\t')
                    f.write(item.getMd5())
                    f.write('\n')
        except:
            print('文件打开失败')


# 客户端
class Client:
    def __init__(self):
        self.getConfig()
        # 连接选项
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client_socket.connect(self.address)

        self.aes = AESCrypto()
        self.file_tree = FilesTree()

    def getConfig(self):
        config = configparser.ConfigParser()
        config.read('local.ini')
        ip = config.get('address', 'ip')
        port = int(config.get('address', 'port'))
        self.address = (ip, port)

    def send_files_info(self):
        self.client_socket.send(self.aes.encrypt_str('file_struct').encode())

        for item in self.file_tree.getNodeTree():
            name_len = len(self.aes.encrypt_str(item.getName()))
            info = struct.pack(str(name_len) + ''
            self.client_socket.send().encode())


    def packFiles(self):
        pass


class AESCrypto:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('local.ini')
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
    client = Client()
    client.send_files_info()