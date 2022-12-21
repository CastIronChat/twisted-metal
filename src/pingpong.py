import socket
import time
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('18.234.154.35', 5500))
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
s.setblocking(True)
i = 0.0
while True:
    start = time.perf_counter_ns()
    print('sending')
    s.send(struct.pack('f', i))
    r = s.recv(4, socket.MSG_WAITALL)
    f, = struct.unpack('f', r)
    end = time.perf_counter_ns()
    print(f, (end - start) / 1e6)
    i += 0.1

# Server

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((socket.gethostname(), 80))
serv.listen(1)
while True:
    # accept connections from outside
    (clientsocket, address) = serv.accept()
    while True:
        r = clientsocket.recv(1)
        clientsocket.write(r)
        print(r)
