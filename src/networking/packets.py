from __future__ import annotations

import struct
from typing import ClassVar, Type, TypeVar

AnyPacket = TypeVar("AnyPacket", bound="Packet")


class Packet:
    id: ClassVar[int]

    @classmethod
    def decode(cls: type[AnyPacket], bytes: bytearray) -> AnyPacket:
        ...

    def encode(self) -> bytearray:
        ...


packets_by_id = dict[int, Type[Packet]]()
next_id = 0


def set_packet_id(cls: AnyPacket) -> AnyPacket:
    global next_id
    cls.id = next_id
    packets_by_id[next_id] = cls
    next_id += 1
    return cls


@set_packet_id
class Ping(Packet):
    last_received_server_time_ns: int
    current_client_time_ns: int
    ping_according_to_client_ms: int

    format = "!qqi"

    @classmethod
    def decode(cls, bytes):
        p = cls()
        (
            p.last_received_server_time_ns,
            p.current_client_time_ns,
            p.ping_according_to_client_ms,
        ) = struct.unpack(cls.format, bytes)
        return p

    def encode(self):
        return struct.pack(
            self.format,
            self.last_received_server_time_ns,
            self.current_client_time_ns,
            self.ping_according_to_client_ms,
        )


@set_packet_id
class Pong(Packet):
    current_server_time_ns: int
    last_received_client_time_ns: int
    ping_according_to_server_ms: int

    format = "!qqi"

    @classmethod
    def decode(cls, bytes):
        p = cls()
        (
            p.current_server_time_ns,
            p.last_received_client_time_ns,
            p.ping_according_to_server_ms,
        ) = struct.unpack(cls.format, bytes)
        return p

    def encode(self):
        return struct.pack(
            self.format,
            self.current_server_time_ns,
            self.last_received_client_time_ns,
            self.ping_according_to_server_ms,
        )


@set_packet_id
class SendToAllClients(Packet):
    packet_id: int
    packet_contents: bytearray

    packet_id_format = "!i"
    id_length = struct.calcsize(packet_id_format)

    @classmethod
    def decode(cls, bytes):
        p = cls()
        (p.packet_id) = struct.unpack(cls.packet_id_format, bytes)
        p.packet_contents = bytes[cls.id_length :]
        return p

    def encode(self):
        return struct.pack(self.packet_id_format, self.packet_id) + self.packet_contents


@set_packet_id
class SetInputDelay(Packet):
    delay: int

    format = "!i"

    @classmethod
    def decode(cls, bytes):
        p = cls()
        (p.delay) = struct.unpack(cls.format, bytes)
        return p

    def encode(self):
        return struct.pack(self.format, self.delay)
