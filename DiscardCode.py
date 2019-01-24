
# Local

# def spiltFile(self):
#     self.client_socket.send(self.aes_local.encrypt_str('file_struct').encode())
#     time.sleep(0.005)
#
#     file_length = os.path.getsize(self.local_info)
#     spilt_num = file_length // self.buff
#     end_length = file_length - spilt_num * self.buff
#     self.client_socket.send(str(spilt_num).encode())
#     time.sleep(0.005)
#
#     with open(self.local_info, 'rb') as f:
#         while True:
#             line = f.read(self.buff)
#             if not line:
#                 break
#             encrypt_line = self.aes_local.encrypt_bin(line)
#             packed_data = struct.pack(str(self.buff) + 's', encrypt_line)
#             self.client_socket.send(packed_data)
#     time.sleep(0.003)
#
#     self.client_socket.send(str(end_length).encode())

# 每次加密10M文件，占用10内存

# def spiltFile(self):
#     self.client_socket.send(self.aes_local.encrypt_str('file_struct').encode())
#     time.sleep(0.005)
#
#     file_length = os.path.getsize(self.local_info)
#     spilt_num = file_length // self.block_size
#     end_length = file_length - spilt_num * self.block_size
#
#     self.client_socket.send(str(self.block_size).encode())
#     time.sleep(0.005)
#
#     count = 0
#     with open(self.local_info, 'rb') as f:
#         while True:
#             if count == spilt_num:
#                 file_block = f.read(end_length)
#             else:
#                 file_block = f.read(self.block_size)
#
#             if not file_block:
#                 break
#             encrypt_block = self.aes_local.encrypt_bin(file_block)
#             self.client_socket.send(encrypt_block)
#             count += 1
#             print(count)
#             time.sleep(0.003)
#
#     # time.sleep(0.003)
#     #
#     # self.client_socket.send(str(end_length).encode())
#
# def spiltFile(self):
#     self.client_socket.send(self.aes_local.encrypt_str('file_struct').encode())
#     time.sleep(0.005)
#
#     file_length = os.path.getsize(self.local_info)
#     spilt_num = file_length // self.block_size
#     end_length = file_length - spilt_num * self.block_size
#
#     self.client_socket.send(str(self.block_size).encode())
#     time.sleep(0.005)
#
#     count = 0
#     with open(self.local_info, 'rb') as f:
#         while True:
#             if count == spilt_num:
#                 file_block = f.read(end_length)
#             else:
#                 file_block = f.read(self.block_size)
#
#             if not file_block:
#                 break
#             encrypt_block = self.aes_local.encrypt_bin(file_block)
#             self.client_socket.send(encrypt_block)
#             count += 1
#             print(count)
#             time.sleep(0.003)

# self.client_socket.send(self.aes_local.encrypt_str(str(spilt_num)).encode())
# time.sleep(0.005)
# self.client_socket.send(self.aes_local.encrypt_str(str(end_length)).encode())
# time.sleep(0.005)












# Server
#
#         # receive = client.recv(self.buff)
#         # if receive == b'':
#         #     break
#         # data = self.aes_remote.decrypt_bin(receive)
#         # if not data:
#         #     break
#         # try:
#         #     with open(self.store_path, 'ab') as f:
#         #         # print(data)
#         #         f.write(data)
#         #
#         # except IOError as error:
#         #     print('File error:' + str(error))
#
#         receive = client.recv(self.buff)
#         if receive == b'':
#             break
#
#         data = struct.unpack(str(self.buff) + 's', receive)[0]
#         de_data = self.aes_remote.decrypt_bin(data)
#
#         if count == spilt_num:
#             end_length = int(client.recv(self.buff).decode())
#             de_data = de_data[:end_length]
#
#         if not receive:
#             break
#         try:
#             with open(self.store_path, 'ab') as f:
#                 f.write(de_data)
#
#         except IOError as error:
#             print('File error:' + str(error))
#
#         count += 1

# def receiveFilesInfo(self, client):
#
#     if os.path.exists(self.store_path):
#         os.remove(self.store_path)
#
#     block_size = int(client.recv(self.buff).decode())
#     print(block_size)
#
#     file_line = b''
#
#     count = 0
#     while True:
#         file_line += client.recv(self.buff)
#
#         if len(file_line) == block_size:
#             decrypt_data = self.aes_remote.decrypt_bin(file_line)
#             file_line = b''
#             try:
#                 with open(self.store_path, 'ab') as f:
#                     f.write(decrypt_data)
#
#             except IOError as error:
#                 print('File error:' + str(error))
#             count += 1
#
#         if not file_line:
#             break
#
#     print(file_line)
#     decrypt_data = self.aes_remote.decrypt_bin(file_line)
#     try:
#         with open(self.store_path, 'ab') as f:
#             f.write(decrypt_data)
#
#     except IOError as error:
#         print('File error:' + str(error))