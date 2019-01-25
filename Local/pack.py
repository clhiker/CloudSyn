import struct
# st = "blabasdf"
# len_str = str(len(st)) + 's'
# print(len_str)
# s = struct.Struct(len_str)
# packed_data = s.pack(st.encode('utf-8'))
#
# us = struct.Struct(len_str)
# unpack_data = us.unpack(packed_data)
# print(type(unpack_data))
# print(type(unpack_data[0]))
# print(unpack_data[0])

a = 1
b = 2
c = 'afsd'
pack = struct.pack('ii4s', a,b,c.encode())
(a,b,c) = struct.unpack('ii4s', pack)
c = c.decode()
print(c)

#
# i = b'dn'
# length = len(i)
# pack_data = struct.pack(str(length) + 'si',i,length)
# unpack_data = struct.unpack(str(length) + 'si', pack_data)
# print(unpack_data)