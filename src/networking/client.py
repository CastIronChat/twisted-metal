from __future__ import annotations

import time

from networking.common import Endpoint
from networking.packets import Packet, Ping, Pong
from networking.ping_average import PingAverage
from networking.server import PacketHandler


class Client(PacketHandler):

    endpoint: Endpoint

    def __init__(self) -> None:
        self.ping_average = PingAverage()
        self.last_received_server_time_ns = 0

    def handle(self, packet: Packet):
        if isinstance(packet, Pong):
            self.handle_pong(packet)
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
        self.endpoint.send(ping)
