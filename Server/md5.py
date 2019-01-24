#!/usr/bin/python
#encoding=utf-8
import io
import sys
import hashlib
import string
def md5(filename):
    m = hashlib.md5()
    file = io.FileIO(filename, 'r')
    bytes = file.read(1024)
    while (bytes != b''):
        m.update(bytes)
        bytes = file.read(1024)
    file.close()
    # md5value = ""
    md5value = m.hexdigest()
    print(md5value)

if __name__ == '__main__':
    md5('/home/clhiker/test.zip')