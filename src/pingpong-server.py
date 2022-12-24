from __future__ import annotations

import socket
import struct

fmt = "!ffff??????????"
pack_length = struct.calcsize(fmt)

# Server

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
serv.setblocking(True)
# serv.bind((socket.gethostname(), 5500))
serv.bind(("127.0.0.1", 5500))
serv.listen(1)
while True:
    # accept connections from outside
    (clientsocket, address) = serv.accept()
    clientsocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
    clientsocket.setblocking(True)
    while True:
        r = clientsocket.recv(pack_length, socket.MSG_WAITALL)
        print(pack_length, len(r))
        unpacked = struct.unpack(fmt, r)
        clientsocket.send(r)
        print(unpacked)
