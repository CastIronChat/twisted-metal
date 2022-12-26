from __future__ import annotations

import time

from networking.common import Endpoint, PacketHandler
from networking.packets import AssignPlayerId, Broadcast, Packet, Ping, Pong
from networking.ping_average import PingAverage


class Server(PacketHandler):

    endpoint: Endpoint
    last_received_client_time_ns: int
    other_handlers: list[Server]

    def __init__(self):
        self.last_received_client_time_ns = 0
        self.ping_average = PingAverage()

    def handle(self, packet: Packet):
        if isinstance(packet, Ping):
            self.handle_ping(packet)
        elif isinstance(packet, Broadcast):
            self.handle_broadcast(packet)
        else:
            raise Exception(f"Unexpected packet type: {packet.__class__.__name__}")

    def handle_ping(self, ping: Ping):
        pong = Pong()
        self.ping_average.log_data_point(
            ping.current_client_time_ns - self.last_received_client_time_ns
        )
        self.last_received_client_time_ns = ping.current_client_time_ns
        pong.last_received_client_time_ns = ping.current_client_time_ns
        pong.current_server_time_ns = time.perf_counter_ns()
        pong.ping_according_to_server_ms = self.ping_average.average_ms
        self.endpoint.queue(pong)

    def send_player_id(self, id: int):
        player_id = AssignPlayerId()
        player_id.player_id = id
        self.endpoint.queue(player_id)

    def handle_broadcast(self, broadcast: Broadcast):
        for other_handler in self.other_handlers:
            other_handler.endpoint.queue(broadcast.decode_wrapped_packet())
