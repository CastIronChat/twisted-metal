from __future__ import annotations

import socket
import struct
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# east coast
# s.connect(("18.234.154.35", 5500))
# west coast
s.connect(("35.91.145.92", 5500))
# localhost
# s.connect(("127.0.0.1", 5500))
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
s.setblocking(True)
i = 0.0
fmt = "!ffff??????????"
pack_length = struct.calcsize(fmt)
while True:
    # time.sleep(0.5)
    # print("sending")
    start = time.perf_counter_ns()
    b = True
    s.send(struct.pack(fmt, i, i, i, i, b, b, b, b, b, b, b, b, b, b))
    r = s.recv(pack_length, socket.MSG_WAITALL)
    unpacked = struct.unpack(fmt, r)
    end = time.perf_counter_ns()
    # print((end - start) / 1e6, unpacked)
    print((end - start) / 1e6, "ms")
    i += 0.1
