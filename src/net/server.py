from __future__ import annotations

import struct
from typing import Protocol, overload

from net.packets import Packet, Ping, packets_by_id
import socket

HEADER_FORMAT = "!ii"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)


class Endpoint:
    socket: socket.socket
    buffer: bytearray
    packets: list[Packet]
    handler: PacketHandler

    def __init__(self):
        self.buffer = bytearray()

    def send(self, packet: Packet):
        data = packet.encode()
        header = struct.pack(HEADER_FORMAT, packet.id, len(data))
        self.socket.send(header + data)

    def receive(self):
        while True:
            new_data = self.socket.recv(100)
            if len(new_data) == 0:
                break
            self.buffer = self.buffer + new_data
        while len(self.buffer) >= HEADER_SIZE:
            (id, size) = struct.unpack_from(HEADER_FORMAT, self.buffer, 0)
            if len(self.buffer) >= HEADER_SIZE + size:
                packet_data = self.buffer[HEADER_SIZE : HEADER_SIZE + size]
                packet = packets_by_id[id].decode(packet_data)
                self.packets.append(packet)
                self.buffer = self.buffer[HEADER_SIZE + size :]
            else:
                break

    """
    Receive and unpack as many packets as possible,
    dispatching them all to the handler.
    """

    def update(self):
        self.receive()
        for packet in self.packets:
            self.handler.handle(packet)
        self.packets.clear()


class PacketHandler(Protocol):
    def handle(self, packet: Packet):
        ...


class Server(PacketHandler):
    @overload
    def handle(ping: Ping):
        pass

    @overload
    def handle(self, packet: Packet):
        raise Exception(f"Unexpected packet type: {packet.__class__.__name__}")
