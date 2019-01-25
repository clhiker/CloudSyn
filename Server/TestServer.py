import socket
import configparser
import aes
import load


class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = ()
        self.max_supported_devices = 3
        self.buff = 1024
        self.home_path = ''
        self.store_path = ''
        self.client = None

        # 读取配置文件
        self.readConfig()

        # 绑定地址
        self.server_socket.bind(self.address)
        # 最多三台设备
        self.server_socket.listen(int(self.max_supported_devices))

        self.aes_remote = aes.AESCrypto()

        self.download_list = []

        self.load_gerenator = load.Load(self.buff)

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

    def down(self):
        while True:
            self.client, address = self.server_socket.accept()
            self.load_gerenator.setClient(self.client)
            self.load_gerenator.download('/home/jerry/Test/Remote/cmake-build-debug/CMakeFiles/mytest.dir/main2.cpp.o')


if __name__ == '__main__':
    server = Server()
    server.down()

