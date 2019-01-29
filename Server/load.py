import HashCode
import aes
import os
# import struct
import time


class Load:
    def __init__(self, buff):

        self.buff = buff
        self.client = None

        self.aes_generator = aes.AESCrypto()
        self.hash_generator = HashCode.MD5()

    def setClient(self, client):
        self.client = client

    def upload(self, file_path):
        file_length = os.path.getsize(file_path)

        spilt_num = file_length // self.buff
        end_length = file_length - spilt_num * self.buff
        hash_code = self.hash_generator.getHash(file_path)

        self.client.send(self.aes_generator.encrypt_str(str(spilt_num)).encode())
        time.sleep(0.005)
        self.client.send(self.aes_generator.encrypt_str(str(end_length)).encode())
        time.sleep(0.005)
        self.client.send(self.aes_generator.encrypt_str(hash_code).encode())
        time.sleep(0.005)

        # file_info = struct.pack('ii32s', spilt_num, end_length, hash_code.encode())
        # self.client.send(self.aes_generator.encrypt_bin(file_info))
        # time.sleep(0.005)
        print(spilt_num)
        print(end_length)
        print(hash_code)

        try:
            with open(file_path, 'rb') as f:
                while True:
                    line = f.read(self.buff)
                    if not line:
                        break
                    encrypt_line = self.aes_generator.encrypt_bin(line)
                    self.client.send(encrypt_line)

        except IOError as error:
            print('upload error:' + str(error))

    #  print('我跳出了')

    def download(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

        # file_info = self.aes_generator.decrypt_bin(self.client.recv(self.buff))
        # (spilt_num, end_length, hash_code) = struct.unpack('ii32s', file_info)
        # remote_hash_code = hash_code.decode()
        spilt_num = int(self.aes_generator.decrypt_str(self.client.recv(self.buff).decode()))
        end_length = int(self.aes_generator.decrypt_str(self.client.recv(self.buff).decode()))
        remote_hash_code = self.aes_generator.decrypt_str(self.client.recv(self.buff).decode())

        print(spilt_num)
        print(end_length)
        print(remote_hash_code)

        line = b''
        count = 0
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        block = self.buff + 16

        while True:
            line += self.client.recv(block)
            spilt_line = line[:block]
            line = line[block:]
            if not spilt_line:
                break
            decrypt_line = self.aes_generator.decrypt_bin(spilt_line)

            try:
                if count == spilt_num:
                    decrypt_line = decrypt_line[:end_length]
                    with open(file_path, 'ab') as f:
                        f.write(decrypt_line)
                    break
                else:
                    with open(file_path, 'ab') as f:
                        f.write(decrypt_line)
            except IOError as error:
                print('download error:' + str(error))
            count += 1

        local_hash_code = self.hash_generator.getHash(file_path)
