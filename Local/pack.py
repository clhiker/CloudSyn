import struct
st = "blabasdf"
len_str = str(len(st)) + 's'
print(len_str)
s = struct.Struct(len_str)
packed_data = s.pack(st.encode('utf-8'))

us = struct.Struct(len_str)
unpack_data = us.unpack(packed_data)
print(type(unpack_data))
print(type(unpack_data[0]))
print(unpack_data[0])