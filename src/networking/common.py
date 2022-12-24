from __future__ import annotations

import socket
import struct
from typing import Protocol

from networking.packets import Packet, packets_by_id

PACKET_HEADER_FORMAT = "!ii"
PACKET_HEADER_SIZE = struct.calcsize(PACKET_HEADER_FORMAT)
RECEIVE_CHUNK_SIZE = 1024


class Endpoint:
    socket: socket.socket
    handler: PacketHandler

    def __init__(self):
        self.buffer = bytearray()
        self.packets: list[Packet] = []
        self.buffer: bytearray = b""

    def send(self, packet: Packet):
        data = packet.encode()
        header = struct.pack(PACKET_HEADER_FORMAT, packet.id, len(data))
        self.socket.send(header + data)

    def receive(self):
        while True:
            try:
                new_data = self.socket.recv(RECEIVE_CHUNK_SIZE)
            except socket.error as e:
                new_data = b""
            if len(new_data) == 0:
                break
            self.buffer = self.buffer + new_data
        while len(self.buffer) >= PACKET_HEADER_SIZE:
            (id, size) = struct.unpack_from(PACKET_HEADER_FORMAT, self.buffer, 0)
            if len(self.buffer) >= PACKET_HEADER_SIZE + size:
                packet_data = self.buffer[
                    PACKET_HEADER_SIZE : PACKET_HEADER_SIZE + size
                ]
                packet = packets_by_id[id].decode(packet_data)
                self.packets.append(packet)
                self.buffer = self.buffer[PACKET_HEADER_SIZE + size :]
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
    def handle(self, packet: Packet) -> None:
        ...
