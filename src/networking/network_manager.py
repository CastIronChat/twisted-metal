from __future__ import annotations

import socket
from typing import TYPE_CHECKING

import server_config
from constants import FRAMES_OF_INPUT_DELAY
from global_input import GlobalInput
from networking.client import Client
from networking.common import Endpoint
from networking.packets import Broadcast, NetworkUnlock, PlayerInputPacket

if TYPE_CHECKING:
    from player import Player
    from player_manager import PlayerManager

from player_input import EMPTY_INPUT_SNAPSHOT, PlayerInputSnapshot

MAX_SEQ_NUMBER = 1000000  # 1e6
"""
Each simulated tick of the game is assigned a sequence number.
Networked player inputs are each tied to a given sequence number.
"""


def increment_tick(tick: int):
    return (tick + 1) % MAX_SEQ_NUMBER


class NetworkManager:
    def __init__(
        self, player_manager: PlayerManager, global_input: GlobalInput
    ) -> None:
        self.global_input = global_input
        self.local_player_ids = []
        self.player_net_states = [
            PlayerNetState(player) for player in player_manager.players
        ]
        # Input delay of 6 ticks.  Capture inputs for tick 6 while simulating tick 0, hoping that we've received those
        # inputs from all peers.  If we haven't, we'll have to pause a frame.
        self.next_simulate_tick = 0
        self.next_input_tick = FRAMES_OF_INPUT_DELAY
        self.next_unsent_input_tick = FRAMES_OF_INPUT_DELAY
        self.unlocked = False
        # Fill the input buffers with empty inputs, but the first input tick *must* still be sent over network, and the
        # game will wait for it
        for state in self.player_net_states:
            for i in range(0, FRAMES_OF_INPUT_DELAY):
                state.buffered_inputs[i] = EMPTY_INPUT_SNAPSHOT

    def connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        s.connect((server_config.ip, server_config.port))
        s.setblocking(False)

        ep = Endpoint()
        client_ep = Client()
        ep.socket = s
        ep.handler = client_ep
        client_ep.endpoint = ep
        client_ep.network_manager = self

        client_ep.send_ping(current_server_time_ns=0)

        self.client_ep = client_ep

    def update(self):

        if self.global_input.network_unlock.pressed:
            packet = NetworkUnlock()
            packet.input_delay = FRAMES_OF_INPUT_DELAY
            self.client_ep.endpoint.queue(Broadcast.from_packet(packet))
            print("sending unlock broadcast")

        input_tick = self.next_input_tick
        simulate_tick = self.next_simulate_tick

        # pull data from the TCP sockets, execute incoming packet handlers
        self.client_ep.endpoint.update()

        # check that we have all necessary player inputs for this tick
        can_simulate_tick = True
        for player_net_state in self.player_net_states:
            if not (simulate_tick in player_net_state.buffered_inputs):
                can_simulate_tick = False
                break

        # Send inputs
        if self.unlocked:
            if self.next_unsent_input_tick == input_tick:
                for player_net_state in self.player_net_states:
                    if player_net_state.is_local:
                        input_snapshot = player_net_state.buffered_inputs[
                            input_tick
                        ] = player_net_state.player.input.capture_physical_inputs()
                        self.send_player_input(
                            player_net_state.player.player_index,
                            input_tick,
                            input_snapshot,
                        )
                self.next_unsent_input_tick = increment_tick(
                    self.next_unsent_input_tick
                )
                print(f"Sent input for tick {input_tick}")

            if can_simulate_tick:
                # Ticks only advance once we've received all inputs
                self.next_input_tick = increment_tick(self.next_input_tick)
                self.next_simulate_tick = increment_tick(self.next_simulate_tick)

                for player_net_state in self.player_net_states:
                    injected_input = player_net_state.buffered_inputs.pop(
                        simulate_tick, EMPTY_INPUT_SNAPSHOT
                    )
                    player_net_state.player.input.update_from_snapshot(injected_input)

                print(f"simulating with received input for tick {simulate_tick}")
            else:
                # print(f"Waiting for inputs to be available for tick {simulate_tick}")
                pass

        self.client_ep.endpoint.flush_send_queue()

        return can_simulate_tick

    def send_player_input(
        self, player_id: int, tick: int, input_snapshot: PlayerInputSnapshot
    ):
        player_input_packet = PlayerInputPacket()
        player_input_packet.player_id = player_id
        player_input_packet.tick = tick
        player_input_packet.snapshot = input_snapshot
        self.client_ep.endpoint.queue(Broadcast.from_packet(player_input_packet))


class PlayerNetState:
    def __init__(self, player: Player) -> None:
        self.player = player
        # TODO allow non-local players
        self.is_local = False

        self.buffered_inputs: dict[int, PlayerInputSnapshot] = dict()
