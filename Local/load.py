import HashCode
import aes
import os
import struct
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

        file_info = struct.pack('ii32s', spilt_num, end_length, hash_code.encode())
        self.client.send(self.aes_generator.encrypt_bin(file_info))
        time.sleep(0.005)

        with open(file_path, 'rb') as f:
            while True:
                line = f.read(self.buff)
                if not line:
                    break
                encrypt_line = self.aes_generator.encrypt_bin(line)
                self.client.send(encrypt_line)
                # print('我也许卡死了')

        # print('我走到这里')

    def download(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)

        file_info = self.aes_generator.decrypt_bin(self.client.recv(self.buff))
        (spilt_num, end_length, hash_code) = struct.unpack('ii32s', file_info)
        remote_hash_code = hash_code.decode()

        line = b''
        count = 0
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        block = self.buff + 16

        while True:
            line += self.client.recv(block)
            spilt_line = line[:block]
            line = line[block:]
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
                print('File error:' + str(error))
            count += 1

        local_hash_code = self.hash_generator.getHash(file_path)
        # if local_hash_code != remote_hash_code:
        #     self.download(file_path)
