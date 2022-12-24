from __future__ import annotations

from typing import overload

from net.packets import Packet, Pong

from net.server import PacketHandler


class Client(PacketHandler):
    @overload
    def handle(self, ping: Pong):
        pass

    @overload
    def handle(self, packet: Packet):
        raise Exception(f"Unexpected packet type: {packet.__class__.__name__}")
