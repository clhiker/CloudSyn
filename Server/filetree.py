
import HashCode
import os


class FileTree:
    def __init__(self):
        self.store_path = ''
        self.home_path = ''
        self.download_list = []
        self.hash_generator = HashCode.MD5()

    def clearDownloadList(self):
        self.download_list = []

    def setStorePath(self, store_path):
        self.store_path = store_path

    def setHomePath(self, home_path):
        self.home_path = home_path

    def getDownLoadList(self):
        return self.download_list

    # 检查文件目录结构信息
    def readFileStruct(self):
        count = 0
        part_path = ''
        real_path = ''
        with open(self.store_path, 'r') as f:
            for line in f:
                if count == 0:
                    part_path = line[:line.rfind('\n')]
                    real_path = self.home_path + part_path

                if count == 1:
                    item_type = line[:line.rfind('\n')]

                    if item_type == 'dir':
                        self.checkDir(real_path)
                    else:
                        self.checkFile(real_path, part_path, item_type)

                    count = -1

                count += 1

    def storeFilesRemote(self):
        if os.path.exists(self.store_path):
            os.remove(self.store_path)
        try:
            with open(self.store_path, 'w') as f:
                for item in self.download_list:
                    f.write(item)
                    f.write('\n')
        except IOError:
            print('文件打开失败')

    def checkFile(self, real_path, part_path, md5):
        if not os.path.exists(real_path):
            self.download_list.append(part_path)

        else:
            self.hash_generator.setMd5(real_path)
            if self.hash_generator.getMd5() != md5:
                self.download_list.append(part_path)

    def checkDir(self, real_path):
        if not os.path.exists(real_path):
            os.mkdir(real_path)



















