`PlayerInput`:
    generic interface
    gameplay is coded against this

`PlayerInputSnapshot`:
    snapshot of inputs
    can be captured from physical controller
    can be injected into the simulation each frame
    can be marshalled to/from packet

When networked:
    at start of frame
    the network controller calls `PlayerInput.capture` on local players
    sends it on the network
    the network controller then calls `PlayerInput.inject()` on all players
    based on received `PlayerInput`
    If it does not have enough data, it ends the `update()`
