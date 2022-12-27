from __future__ import annotations

import time
from typing import TYPE_CHECKING

from networking.common import Endpoint

if TYPE_CHECKING:
    from networking.network_manager import NetworkManager

from networking.packets import (
    AssignPlayerId,
    NetworkUnlock,
    Packet,
    Ping,
    PlayerInputPacket,
    Pong,
)
from networking.ping_average import PingAverage
from networking.server import PacketHandler


class Client(PacketHandler):

    endpoint: Endpoint
    network_manager: NetworkManager

    def __init__(self) -> None:
        self.ping_average = PingAverage()
        self.last_received_server_time_ns = 0

    def handle(self, packet: Packet):
        if isinstance(packet, Pong):
            self.handle_pong(packet)
        elif isinstance(packet, AssignPlayerId):
            self.handle_assign_player_id(packet)
        elif isinstance(packet, PlayerInputPacket):
            self.handle_player_input(packet)
        elif isinstance(packet, NetworkUnlock):
            self.handle_network_unlock(packet)
        else:
            raise Exception(f"Unexpected packet type: {packet.__class__.__name__}")

    def handle_pong(self, pong: Pong):
        self.ping_average.log_data_point(
            pong.current_server_time_ns - self.last_received_server_time_ns
        )
        self.last_received_server_time_ns = pong.current_server_time_ns
        self.send_ping(pong.current_server_time_ns)
        print(
            f"Average ping: server calculated: {pong.ping_according_to_server_ms}ms, client calculated: {self.ping_average.average_ms}ms"
        )

    def send_ping(self, current_server_time_ns: int):
        ping = Ping()
        ping.last_received_server_time_ns = current_server_time_ns
        ping.current_client_time_ns = time.perf_counter_ns()
        ping.last_received_server_time_ns = current_server_time_ns
        ping.ping_according_to_client_ms = self.ping_average.average_ms
        self.endpoint.queue(ping)

    def handle_assign_player_id(self, assign_player_id: AssignPlayerId):
        print(f"Received player assignment to index {assign_player_id.player_id}")
        # player = cast(Player, self.player_manager.players[assign_player_id.player_id])
        self.network_manager.local_player_ids.append(assign_player_id.player_id)
        self.network_manager.player_net_states[
            assign_player_id.player_id
        ].is_local = True

    def handle_player_input(self, packet: PlayerInputPacket):
        print(f"Received input for player {packet.player_id} on tick {packet.tick}")
        self.network_manager.player_net_states[packet.player_id].buffered_inputs[
            packet.tick
        ] = packet.snapshot

    def handle_network_unlock(self, packet: NetworkUnlock):
        print("server told me to unlock")
        self.network_manager.unlocked = True
