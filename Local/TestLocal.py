import socket
import configparser
import aes
import load

class Local:
    def __init__(self):
        self.address = ()
        self.local_path = ''
        self.home_path = ''
        self.buff = 1024
        self.block_size = 1024
        self.getConfig()
        # 连接选项
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client_socket.connect(self.address)

        self.load_generator = load.Load(self.buff)
        self.load_generator.setClient(self.client_socket)

    def getConfig(self):
        config = configparser.ConfigParser()
        config.read('local.ini')
        ip = config.get('address', 'ip')
        port = int(config.get('address', 'port'))
        self.address = (ip, port)
        self.local_path = config.get('path', 'store_path')
        self.home_path = config.get('path', 'home_path')

        self.buff = int(config.get('spilt', 'buff'))
        self.block_size = int(config.get('spilt', 'block_size'))

    def up(self):
        self.load_generator.upload('/home/jerry/Test/Local/cmake-build-debug/CMakeFiles/mytest.dir/main2.cpp.o')


if __name__ == '__main__':
    client = Local()
    client.up()