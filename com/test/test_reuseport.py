import socket
import time
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for i in range(50):
    time.sleep(1)
    s.connect(('127.0.0.1', 12355))
    s.send("aoeu".encode('utf-8'))