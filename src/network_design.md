Each packet has a packet ID and then a fixed number of bytes following it.
Some packet IDs can be variable length and include prefixed length.

Each packet implements its own deserialization.
Deserialize can return True/False if deserialization is complete.
If False, networking layer will wait for more data, append, try again.
This enables packets to have variable length.

## Sequence numbers

Each frame of the game has a sequence number.
These go up from 0 to 999999, then restarting at 0
Aka 1e6, or 1,000,000 is equivalent to 0
(if seq_num == 1e6: seq_num = 0)

This limit is arbitrary, but chosen to meet these constraints:

- Is small enough that simple modulo operation is enough to implement looping back to 0.
  - Python ints go from -2147483648 to 2147483647
  - 2x 1e6 is way less than max int.  We can also go into the negative no problem; we are using signed ints.
- Is large enough that one client will never lag so bad that it accidentally loops around back to zero, "time-travelling" or losing time.
  - At 60 ticks per second, 1e6 / 60 / 60 / 60 = 4.6 hours

## Packet wrapper

Each packet has this structure:

- packet_id
- packet_length
- packet_contents

## SendToAllClients

Requests that server sends a packet to all clients (including this one)
In practice, this is how most messages get to a client: the "Player 1" client
sends this to the server.

- packet_id
- packet_contents

## SetInputDelay

Sent from player 1 to server.
Set tick delay.
Example:
If set to 6, then inputs sent on sequence number 1 will be received by clients for sequence number 7.
This means inputs pressed on frame 1 will be round-tripped to the server and apply to simulation frame 7.
This is a frame delay of 6, or 1/10 sec. *Theoretically* sustainable if player pings remain reliably
below 100ms.

## Ping

Sent from client to server as soon as it connects and every time it gets a pong.
Used for ping calculations.

- last_received_server_time
- current_client_time

## Pong

Sent from server to client as soon as it gets a ping.
Used for ping calculations.

- current_server_time
- last_received_client_time
- ping - rolling average of ping according to the server

## RequestPlayerId

Sent from client to server to request that a player ID (0-4) reside on this
client.

## AssignPlayerId

Sent from server to client giving a player ID (0-4) to a client.

## SetSeedPacket

Resets the seed on all clients to be the same thing.

- seed

## PlayerInput

Input for a single player, sent from player to server

- tick_number

## DoSequenceNumberShifts

Request from player 1 to server to send everyone a sequence shift command.

## ShiftSequenceNumbers

Request from server to client to offset its sequence numbers by a given amount.
Each client is instructed to shift a different amount, intending to align them
with each other.

## SetSequenceNumber

Temp for prototyping: reset a client's sequence number to a given value.
Easy way for server to reset everyone to roughly the same reference time.

## AllInputs

Inputs for 4x players for a given tick

- tick_number
- PlayerInputState
- PlayerInputState
- PlayerInputState
- PlayerInputState
