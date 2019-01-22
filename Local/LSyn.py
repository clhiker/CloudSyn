#!/usr/bin/python
#encoding=utf-8

import os
import io
import hashlib
import socket
import configparser
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

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

# 广度优先
class FilesTree:
    def __init__(self):
        self.home_path = '/home/clhiker/Test'
        self.home_node = FileNode()
        self.home_node.setPath(self.home_path)
        self.home_node.setNode()
        # 返回一个广度优先遍历的列表
        self.node_tree = []
        self.setTree(self.home_path)


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

    def packTree(self):
        pass

    def display(self):
        for item in self.node_tree:
            print(item.getName(), end='\t')
            print(item.getMd5())


class Client:
    def __init__(self):
        # 连接选项
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        config = configparser.ConfigParser()
        config.read('local.ini')
        ip = config.get('address', 'ip')
        port = int(config.get('address', 'port'))
        address = (ip, port)
        self.client_socket.connect(address)
        self.load_process = 0

        self.stop_button = False
        self.cancel_button = False

        self.remote_file_size = 0

    def packFiles(self):
        pass


if __name__ == '__main__':
    file_tree = FilesTree()
    file_tree.display()