# Goal

minimum work to prove determinism

## Game changes to make it deterministic

replace random calls

Sort arrays coming out of collision detection?

## Networking impl

Stub out server
Write abstract packet class
Write concrete packet classes for sequence syncing

Write streaming packet receiver

- breaks up packets
- invokes handler with each packet

## First-pass gameplay logic

Ignore sequence numbers

## First-pass client

Track current sequence number.
Track received player inputs.
Store desired input delay.
