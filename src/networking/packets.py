from __future__ import annotations

import struct
from typing import ClassVar, Type, TypeVar

from player_input import PlayerInputSnapshot

AnyPacket = TypeVar("AnyPacket", bound="Packet")
AnyPacketSubclass = TypeVar("AnyPacketSubclass", bound="Type[Packet]")


class Packet:
    packet_type_id: ClassVar[int]

    @classmethod
    def decode(cls: type[AnyPacket], bytes: bytes) -> AnyPacket:
        ...

    def encode(self) -> bytes:
        ...


packets_by_id = dict[int, Type[Packet]]()
next_id = 0


def assign_packet_id(cls: AnyPacketSubclass) -> AnyPacketSubclass:
    global next_id
    cls.packet_type_id = next_id
    packets_by_id[next_id] = cls
    next_id += 1
    return cls


@assign_packet_id
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


@assign_packet_id
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


@assign_packet_id
class Broadcast(Packet):
    wrapped_packet_type_id: int
    packet_contents: bytes

    _packet_id_format = "!i"
    _id_length = struct.calcsize(_packet_id_format)

    @classmethod
    def from_packet(cls, packet: Packet) -> Broadcast:
        broadcast = Broadcast()
        broadcast.wrapped_packet_type_id = packet.packet_type_id
        broadcast.packet_contents = packet.encode()
        return broadcast

    @classmethod
    def decode(cls, bytes):
        p = cls()
        (p.wrapped_packet_type_id,) = struct.unpack(
            cls._packet_id_format, bytes[: cls._id_length]
        )
        p.packet_contents = bytes[cls._id_length :]
        return p

    def encode(self):
        return (
            struct.pack(self._packet_id_format, self.wrapped_packet_type_id)
            + self.packet_contents
        )

    def decode_wrapped_packet(self):
        return packets_by_id[self.wrapped_packet_type_id].decode(self.packet_contents)


@assign_packet_id
class SetInputDelay(Packet):
    delay: int

    format = "!i"

    @classmethod
    def decode(cls, bytes):
        p = cls()
        (p.delay,) = struct.unpack(cls.format, bytes)
        return p

    def encode(self):
        return struct.pack(self.format, self.delay)


@assign_packet_id
class AssignPlayerId(Packet):
    player_id: int

    format = "!i"

    @classmethod
    def decode(cls, bytes):
        p = cls()
        (p.player_id,) = struct.unpack(cls.format, bytes)
        return p

    def encode(self):
        return struct.pack(self.format, self.player_id)


@assign_packet_id
class PlayerInputPacket(Packet):
    player_id: int
    tick: int
    snapshot: PlayerInputSnapshot

    format = "!iiffffff????????"

    @classmethod
    def decode(cls, bytes):
        p = cls()
        s = p.snapshot = PlayerInputSnapshot()
        (
            p.player_id,
            p.tick,
            s.x_axis,
            s.y_axis,
            s.rx_axis,
            s.ry_axis,
            s.accelerate_axis,
            s.brake_axis,
            s.primary_fire_button,
            s.secondary_fire_button,
            s.swap_weapons_button,
            s.reload_button,
            s.debug_1,
            s.debug_2,
            s.debug_3,
            s.debug_4,
        ) = struct.unpack(cls.format, bytes)
        return p

    def encode(self):
        s = self.snapshot
        return struct.pack(
            self.format,
            self.player_id,
            self.tick,
            s.x_axis,
            s.y_axis,
            s.rx_axis,
            s.ry_axis,
            s.accelerate_axis,
            s.brake_axis,
            s.primary_fire_button,
            s.secondary_fire_button,
            s.swap_weapons_button,
            s.reload_button,
            s.debug_1,
            s.debug_2,
            s.debug_3,
            s.debug_4,
        )


@assign_packet_id
class NetworkUnlock(Packet):
    input_delay: int

    format = "!i"

    @classmethod
    def decode(cls, bytes):
        p = cls()
        (p.input_delay,) = struct.unpack(cls.format, bytes)
        return p

    def encode(self) -> bytes:
        return struct.pack(self.format, self.input_delay)
