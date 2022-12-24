from __future__ import annotations

import select
import socket
import time

import server_config
from networking.client import Client
from networking.common import Endpoint

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
s.connect((server_config.ip, server_config.port))
s.setblocking(False)

ep = Endpoint()
client_ep = Client()
ep.socket = s
ep.handler = client_ep
client_ep.endpoint = ep

client_ep.send_ping(current_server_time_ns=0)
while True:
    (readable, writable, exceptioned) = select.select([ep.socket], [], [])
    ep.update()
