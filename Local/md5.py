#!/usr/bin/python
# encoding=utf-8
import io
import hashlib


class MD5:
    def __init__(self):
        self.filename = ''
        self.md5 = ''

    def setFileName(self, filename):
        self.filename = filename

    def getFileName(self):
        return self.filename

    def setMd5(self, filename):
        m = hashlib.md5()
        file = io.FileIO(filename, 'r')
        block = file.read(1024)
        while block != b'':
            m.update(block)
            block = file.read(1024)
        file.close()
        md5value = m.hexdigest()
        self.md5 = md5value

    def getMd5(self):
        return self.md5

    

if __name__ == '__main__':
    md5('/home/clhiker/test.zip')