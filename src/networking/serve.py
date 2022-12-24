from __future__ import annotations

import select
import socket
import sys
import time

import server_config
from networking.common import Endpoint
from networking.server import Server

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
serv.bind((server_config.bind_ip, server_config.port))
serv.listen(4)
endpoints: list[Endpoint] = []
all_sockets: list[socket.socket] = []

print("Server is up")

while True:
    # sys.stdout.flush()
    all_sockets = [serv] + [ep.socket for ep in endpoints]
    (readable, writable, exceptioned) = select.select(
        all_sockets, all_sockets, all_sockets
    )

    if serv in readable:
        # accept connections from outside
        print("Received connection")
        (clientsocket, address) = serv.accept()
        clientsocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        clientsocket.setblocking(False)
        ep = Endpoint()
        server_ep = Server()
        ep.socket = clientsocket
        ep.handler = server_ep
        server_ep.endpoint = ep
        endpoints.append(ep)
        server_ep.send_player_id(len(endpoints) - 1)

    for ep in endpoints:
        ep.update()
