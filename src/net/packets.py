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


def set_packet_id(cls: Packet):
    global next_id
    cls.id = next_id
    packets_by_id[next_id] = cls
    next_id += 1


@set_packet_id
class Ping(Packet):
    last_received_server_time: int
    current_client_time: int

    format = "!ii"

    @classmethod
    def decode(cls, bytes):
        p = cls()
        (p.last_received_server_time, p.current_client_time) = struct.unpack(
            cls.format, bytes
        )
        return p

    def encode(self):
        return struct.pack(
            self.format, self.last_received_server_time, self.current_client_time
        )


@set_packet_id
class Pong(Packet):
    current_server_time: int
    last_received_client_time: int

    format = "!ii"

    @classmethod
    def decode(cls, bytes):
        p = cls()
        (p.current_server_time, p.last_received_client_time) = struct.unpack(
            cls.format, bytes
        )
        return p

    def encode(self):
        return struct.pack(
            self.format, self.current_server_time, self.last_received_client_time
        )
