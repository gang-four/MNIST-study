import socket
import struct
import time
import sys
from google.protobuf import json_format
from google.protobuf.internal import encoder
import test_pb2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 10000))
# 为 all_person 填充数据
p1 = test_pb2.Person();
p1.id = 1
p1.name = 'xieyanke'
p1.email = 'liubaochuan@qq.com'
p1.friends = '2321321,21321,3213'

# p2 = test_pb2.Person
# p2.id = 2
# p2.name = 'pythoner'
# p2.email ='123231312@qq.com'
# p2.friends ='2321321,21321,3213'

# print(p1.name)
# # 对数据进行序列化
data = p1.SerializeToString()
# print(data)
print(data.__len__())
headPack1 = struct.pack("i", data.__len__())
print(headPack1)
sendData = headPack1+data
print(sendData)

delimiter = encoder._VarintBytes(len(data))
sendData2 = delimiter+data
print(sendData2)
#
# # 从二进制反序列化
# person1 = test_pb2.Person()
# person1.ParseFromString(data)

# 转换成字典
# print(json_format.MessageToDict(p1, True))


# 从json数据反序列化
# person2 = test_pb2.Person()
# json_format.Parse(json_format.MessageToJson(p1, True), person2)
# print(person2)

for i in range(50):
    time.sleep(1)
    s.send(sendData2)
