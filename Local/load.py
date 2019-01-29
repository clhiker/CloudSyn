import Encryptor
import os
import struct
import time


class Load:
    def __init__(self, buff):

        self.buff = buff
        self.client = None

        # 初始化加密器
        self.encryptor_generator = Encryptor.AES_MD5()

    def setClient(self, client):
        self.client = client

    def upload(self, file_path):
        file_length = os.path.getsize(file_path)

        spilt_num = file_length // self.buff
        end_length = file_length - spilt_num * self.buff
        hash_code = self.encryptor_generator.getMd5(file_path)

        # self.client.send(self.encryptor_generator.encrypt_str(str(spilt_num)).encode())
        # time.sleep(0.005)
        # self.client.send(self.encryptor_generator.encrypt_str(str(end_length)).encode())
        # time.sleep(0.005)
        # self.client.send(self.encryptor_generator.encrypt_str(hash_code).encode())
        # time.sleep(0.005)

        file_info = struct.pack('ii32s', spilt_num, end_length, hash_code.encode())
        self.client.send(self.encryptor_generator.encrypt_bin(file_info))
        time.sleep(0.005)

        if file_length != 0:
            try:
                with open(file_path, 'rb') as f:
                    while True:
                        line = f.read(self.buff)
                        if not line:
                            break
                        encrypt_line = self.encryptor_generator.encrypt_bin(line)
                        self.client.send(encrypt_line)

            except IOError as error:
                print('upload error:' + str(error))

    def download(self, file_path):

        if os.path.exists(file_path):
            os.remove(file_path)

        file_info = self.encryptor_generator.decrypt_bin(self.client.recv(self.buff))
        (spilt_num, end_length, hash_code) = struct.unpack('ii32s', file_info)
        remote_hash_code = hash_code.decode()

        # spilt_num = int(self.encryptor_generator.decrypt_str(self.client.recv(self.buff).decode()))
        # end_length = int(self.encryptor_generator.decrypt_str(self.client.recv(self.buff).decode()))
        # remote_hash_code = self.encryptor_generator.decrypt_str(self.client.recv(self.buff).decode())

        if spilt_num == 0 and end_length == 0:
            with open(file_path, 'ab') as f:
                f.write(b'')
                return

        line = b''
        count = 0
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        block = self.buff + 16

        while True:
            receicve = self.client.recv(block)
            line += receicve
            spilt_line = line[:block]
            line = line[block:]
            decrypt_line = self.encryptor_generator.decrypt_bin(spilt_line)

            try:
                if count == spilt_num:
                    decrypt_line = decrypt_line[:end_length]
                    with open(file_path, 'ab') as f:
                        f.write(decrypt_line)
                    return
                else:
                    with open(file_path, 'ab') as f:
                        f.write(decrypt_line)
            except IOError as error:
                print('download error:' + str(error))
            count += 1

        # local_hash_code = self.encryptor_generator.getMd5(file_path)
