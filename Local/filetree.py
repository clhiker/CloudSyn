import configparser
import os
import hashlib
import io

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
class FileTree:
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
                    f.write('\n')
                    f.write(item.getMd5())
                    f.write('\n')
        except:
            print('文件打开失败')